"""Read-only on-disk PE/MSF7/PDB public-symbol inventory; no process API.

No Blender launch/attach, build, ctypes, symbol server or memory-layout guesses.
"""
from pathlib import Path
import struct,uuid,hashlib,json,sys
INSTALL=Path(r'C:/Program Files/Blender Foundation/Blender 5.2')
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-actual-cycles-readback-preparation-r1')
OUT.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
class MSF:
 def __init__(self,b):
  self.b=b;assert b[:32]==b'Microsoft C/C++ MSF 7.00\r\n\x1aDS\0\0\0'
  self.bs,_,_,ds,_,mb=struct.unpack_from('<IIIIII',b,32)
  ids=struct.unpack_from('<'+'I'*((ds+self.bs-1)//self.bs),b,mb*self.bs)
  d=b''.join(b[i*self.bs:(i+1)*self.bs] for i in ids)[:ds]
  n=struct.unpack_from('<I',d)[0];sizes=struct.unpack_from('<'+'I'*n,d,4);cur=4+4*n;self.streams=[]
  for size in sizes:
   count=0 if size==0xffffffff else (size+self.bs-1)//self.bs
   blocks=struct.unpack_from('<'+'I'*count,d,cur) if count else [];cur+=4*count
   self.streams.append((size,blocks))
 def read(self,i):
  size,blocks=self.streams[i]
  return b''.join(self.b[k*self.bs:(k+1)*self.bs] for k in blocks)[:size]
exe=(INSTALL/'blender.exe').read_bytes();pdb=(INSTALL/'blender.pdb').read_bytes();msf=MSF(pdb)
pe=struct.unpack_from('<I',exe,0x3c)[0];ns=struct.unpack_from('<H',exe,pe+6)[0]
opt=pe+24;osz=struct.unpack_from('<H',exe,pe+20)[0];assert struct.unpack_from('<H',exe,opt)[0]==0x20b
sections=[]
for i in range(ns):
 o=opt+osz+40*i;vs,va,rs,rp=struct.unpack_from('<IIII',exe,o+8)
 sections.append({'name':exe[o:o+8].rstrip(b'\0').decode(),'virtual_size':vs,'VA':va,'raw_size':rs,'raw_pointer':rp})
def raw_rva(rva):
 for s in sections:
  if s['VA']<=rva<s['VA']+s['raw_size']:return s['raw_pointer']+rva-s['VA']
 raise ValueError(rva)
drva,dsize=struct.unpack_from('<II',exe,opt+112+6*8);rsds=[]
for o in range(raw_rva(drva),raw_rva(drva)+dsize,28):
 typ,n,_,ptr=struct.unpack_from('<IIII',exe,o+12)
 if typ==2 and exe[ptr:ptr+4]==b'RSDS':
  rsds.append({'guid':str(uuid.UUID(bytes_le=exe[ptr+4:ptr+20])),'age':struct.unpack_from('<I',exe,ptr+20)[0],'file_offset':ptr,'embedded_path':exe[ptr+24:ptr+n].split(b'\0')[0].decode()})
info=msf.read(1);guid=str(uuid.UUID(bytes_le=info[12:28]));age=struct.unpack_from('<I',info,8)[0]
assert any(x['guid']==guid and x['age']==age for x in rsds)
dbi=msf.read(3);symbols=msf.read(struct.unpack_from('<H',dbi,20)[0]);cur=0;hits=[];build={};tbb=[]
while cur+4<=len(symbols):
 length,kind=struct.unpack_from('<HH',symbols,cur)
 assert length>=2 and cur+length+2<=len(symbols)
 if kind==0x110e:
  flags,off,seg=struct.unpack_from('<IIH',symbols,cur+4)
  name=symbols[cur+14:cur+length+2].split(b'\0')[0].decode(errors='replace')
  target=any(k in name for k in ('update_tangents@Mesh','MikkMeshWrapper','find@AttributeSet@ccl','device_update@GeometryManager','synchronize@BlenderSession','sync_mesh@BlenderSync','need_attribute@Geometry'))
  if target or name.startswith('build_'):
   s=sections[seg-1];record={'name':name,'section':seg,'section_name':s['name'],'offset':off,'RVA':s['VA']+off,'flags':flags,'within_virtual_and_raw_section':off<s['virtual_size'] and off<s['raw_size']}
   if target:hits.append(record)
   if name.startswith('build_') and name not in ('build_commit_timestamp','build_commit_date','build_commit_time'):
    # buildinfo.c declares these exact public data symbols char[], not guessed layouts.
    p=s['raw_pointer']+off
    build[name]={'value':exe[p:p+8192].split(b'\0')[0].decode(),'RVA':record['RVA']}
   if 'MikkMeshWrapper' in name and '@tbb@@' in name:tbb.append(record)
 cur+=length+2
def type_info(index):
 b=msf.read(index)
 return {'stream_bytes':len(b),'type_index_begin':struct.unpack_from('<I',b,8)[0],'type_index_end':struct.unpack_from('<I',b,12)[0],'type_record_bytes':struct.unpack_from('<I',b,16)[0]}
modi=struct.unpack_from('<I',dbi,24)[0];block=dbi[64:64+modi];cur=0;mods=0;modulehits=[]
while cur+64<=len(block):
 stream=struct.unpack_from('<H',block,cur+34)[0];symbolsize=struct.unpack_from('<I',block,cur+36)[0]
 a=cur+64;end1=block.index(0,a);end2=block.index(0,end1+1)
 module=block[a:end1].decode(errors='replace');obj=block[end1+1:end2].decode(errors='replace');cur=(end2+4)&~3;mods+=1
 text=(module+' '+obj).lower()
 if 'cycles' in text and ('mesh' in text or 'attribute' in text):
  r={'module':module,'object':obj,'stream':stream,'symbol_bytes':symbolsize,'compiler_records':[]}
  if stream!=0xffff:
   data=msf.read(stream);i=4
   while i+4<=min(len(data),symbolsize):
    length,kind=struct.unpack_from('<HH',data,i)
    if length<2 or i+length+2>len(data):break
    if kind==0x113c and length>=24:
     r['compiler_records'].append({'kind':'S_COMPILE3','flags':struct.unpack_from('<I',data,i+4)[0],'machine':struct.unpack_from('<H',data,i+8)[0],'frontend':list(struct.unpack_from('<HHHH',data,i+10)),'backend':list(struct.unpack_from('<HHHH',data,i+18)),'version':data[i+26:i+length+2].split(b'\0')[0].decode(errors='replace')})
    i+=length+2
  modulehits.append(r)
result={'task_id':'ROOT_PM_ACTUAL_CYCLES_READBACK_PREPARATION_R1','method':'File-only validated PE section/RSDS + MSF7 stream1/DBI/S_PUB32/TPI/IPI. No process memory, debugger attach or ctypes.',
 'exe':{'path':str(INSTALL/'blender.exe'),'bytes':len(exe),'sha256':sha(exe),'RSDS':rsds},
 'PDB':{'path':str(INSTALL/'blender.pdb'),'bytes':len(pdb),'sha256':sha(pdb),'GUID':guid,'age':age,'PE_identity_match':True,'DBI_flags':struct.unpack_from('<H',dbi,56)[0]},
 'sections':sections,'public_symbols':hits,'Mikk_TBB_public_symbol_count':len(tbb),'TBB_samples':tbb[:5],'build_global_strings':build,
 'TPI':type_info(2),'IPI':type_info(4),'module_count':mods,'cycles_module_compiler_records':modulehits,
 'native_type_member_layout_ready':False,'safe_host_attribute_observer_ready':False,'actual_buffer':'HOLD'}
(OUT/'PDB_NATIVE_OBSERVER_INVENTORY.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print('PE_PDB_MATCH',guid,age,'PUBLIC_SYMBOLS',len(hits),'TBB_SYMBOLS',len(tbb),'TPI_RECORD_BYTES',result['TPI']['type_record_bytes'],'MODULE_HITS',len(modulehits))
print(json.dumps(modulehits[:10],indent=2))
