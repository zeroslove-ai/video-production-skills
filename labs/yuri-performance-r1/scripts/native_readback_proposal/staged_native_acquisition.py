"""Executable acquisition/staging proposal; default dry-run; NO build/capture.
Only execute after human approval of the known7,054,121,984 payload + Git overhead.
No global installation/PATH mutation. Metadata rooted in frozen R1 packet.
"""
from pathlib import Path
import argparse, ctypes, hashlib, json, os, shutil, tarfile, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(r'C:/YuriTransfer/native-cycles-readback-r1')
FROZEN=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-guarded-native-resource-sizing-r1')
GIT=Path(r'C:/Program Files/Git/cmd/git.exe');UNPACK=Path(r'C:/Program Files/7-Zip/7z.exe')
DEPS_COMMIT='60d6e96b917568278d400a4024c98da0fb777338'
ENDPOINT='https://projects.blender.org/blender/lib-windows_x64.git/info/lfs/objects/batch'
def sha(p,kind='sha256'):
    h=hashlib.new(kind)
    with p.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024**2),b''):h.update(chunk)
    return h.hexdigest()
def owned(p):
    assert p.resolve().is_relative_to(ROOT.resolve()), 'outside exact owned root'
    return p
def resources(full=False):
    assert shutil.disk_usage(ROOT).free>=100*1024**3
    # OS-only documented memory status; no GPU/Blender process handle opened.
    class M(ctypes.Structure):
        _fields_=[('length',ctypes.c_uint32),('load',ctypes.c_uint32)]+[(n,ctypes.c_uint64) for n in ('total','available','tp','ap','tv','av','ae')]
    m=M();m.length=ctypes.sizeof(m)
    fn=ctypes.WinDLL('kernel32',use_last_error=True).GlobalMemoryStatusEx
    fn.argtypes=[ctypes.POINTER(M)];fn.restype=ctypes.c_int
    assert fn(ctypes.byref(m)) and m.available>=12*1024**3
    # Conservative budget checked after stages as well as during each stream.
    if full:
        total=sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())
        assert total<=80*1024**3, 'owned workspace disk budget exceeded'
def receipt(name,value):
    p=owned(ROOT/'receipts'/f'{name}-{time.time_ns()}.json');p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(value,indent=2));return p
def quarantine(p,reason):
    p=owned(p);q=owned(ROOT/'quarantine'/f'{p.name}-{time.time_ns()}');q.parent.mkdir(exist_ok=True)
    if p.exists():p.rename(q)
    receipt('quarantine',{'path':str(q),'reason':reason})
def download(url, target, size, expected, algorithm='sha256', extra_headers=None):
    target=owned(target);target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():
        assert target.stat().st_size==size and sha(target,algorithm)==expected,'cached payload mismatch'
        return {'payload':target.name,'bytes':size,'digest':expected,'cache_reused':True}
    part=target.with_name(target.name+'.part');owned(part)
    offset=part.stat().st_size if part.exists() else 0
    if offset>size:quarantine(part,'oversized partial');offset=0
    headers={'User-Agent':'Yuri-Desktop-Approved-Resource-Stager','Accept-Encoding':'identity'}
    headers.update(extra_headers or {})
    if offset:headers['Range']=f'bytes={offset}-'
    # LFS action headers/URLs may contain tokens. Never save/print them.
    try:
        response=urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=60)
        if offset and response.status!=206:
            response.close();quarantine(part,'server ignored range; restart clean')
            return download(url,target,size,expected,algorithm,extra_headers)
        if offset:assert response.headers.get('Content-Range','').startswith(f'bytes {offset}-')
        with response,part.open('ab' if offset else 'wb') as stream:
            while True:
                chunk=response.read(1024**2)
                if not chunk:break
                assert stream.tell()+len(chunk)<=size,'unexpected response length'
                stream.write(chunk)
                # Cheap disk/freeRAM guard per16MiB; full workspace budget perfile.
                if stream.tell()%(16*1024**2)<1024**2:resources()
        if part.stat().st_size!=size:
            receipt('partial-retained',{'payload':target.name,'bytes':part.stat().st_size,'resume':'same identity + Range; final full-file hash mandatory'})
            raise RuntimeError('incomplete payload retained for verified identity resume')
        if sha(part,algorithm)!=expected:
            quarantine(part,'complete digest mismatch');raise RuntimeError('payload digest mismatch')
        assert not target.exists();part.rename(target);resources()
        row={'payload':target.name,'bytes':size,'digest':expected,'algorithm':algorithm,'resumed_from':offset,'local_SHA256':sha(target)}
        receipt('verified-payload',row);return row
    except Exception as error:
        receipt('transfer-failure',{'payload':target.name,'exception_type':type(error).__name__,
            'partial_bytes':part.stat().st_size if part.exists() else 0,'no_auth_headers_or_transient_urls_logged':True})
        raise RuntimeError('owned transfer stage failed; see sanitized receipt') from None
def tool(argv,review,timeout=900):
    from owned_windows_capture_supervisor import run
    env=os.environ.copy();env.update({'GIT_LFS_SKIP_SMUDGE':'1','GIT_TERMINAL_PROMPT':'0'})
    result=run(Path(argv[0]),None,review,timeout=timeout,command_override=argv,
        RAM_cap=8*1024**3,processes=8,affinity=3,environment=env)
    receipt('owned-tool',result);return result
def execute(review):
    assert os.name=='nt' and review['human_large_resource_acquisition_approved'] is True
    assert review['approved_known_payload_bytes']==7054121984 and review['Git_transport_overhead_acknowledged'] is True
    plan=FROZEN/'ACQUISITION_PLAN.json';manifest=FROZEN/'WINDOWS_DEPS_EXACT_PAYLOAD_MANIFEST.json'
    assert sha(plan)==review['acquisition_plan_sha256'] and sha(manifest)==review['Windows_deps_manifest_sha256']
    assert sha(Path(__file__))==review['acquisition_script_sha256']
    for p in (GIT,UNPACK):assert sha(p)==review['allowed_tools'][str(p.resolve())]
    if ROOT.exists():assert ROOT.is_dir() and owned(ROOT)==ROOT
    else:ROOT.mkdir()  # Exact named isolated target; only after approval.
    (ROOT/'capture').mkdir(exist_ok=True);resources(full=True)
    data=json.loads(plan.read_text());deps=json.loads(manifest.read_text())
    assert deps['unique_LFS_payload_bytes']==6574796539
    archive=ROOT/'downloads/blender-5.2.1.tar.xz'
    download(data['source_archive']['url'],archive,93666248,'ff0022afc5b8444db46371c6e07b4dd5','md5')
    source=ROOT/'src';stage=ROOT/'source-extraction'
    if not source.exists():
        assert not stage.exists(),'partial source extraction requires inspection/quarantine, no blind overwrite'
        stage.mkdir()
        with tarfile.open(archive,'r:xz') as tar:tar.extractall(stage,filter='data')
        dirs=list(stage.iterdir());assert len(dirs)==1 and dirs[0].is_dir()
        owned(dirs[0]);owned(source);dirs[0].rename(source)
    # Validate every source file used by the patch against pinned native originals.
    original=json.loads((FROZEN/'NATIVE_V3_REVIEW_RECEIPT.json').read_text())['original_source']
    for name,row in original.items():
        text=(source/name).read_text().encode();assert hashlib.sha256(text).hexdigest()==row['sha256'],name
    receipt('source-staged',{'path':str(source),'release':'5.2.1','pinned_patch_source_files_verified':len(original),'archive_MD5_verified':True,'local_archive_SHA256':sha(archive)})
    installer=ROOT/'downloads/LLVM-20.1.8-win64.exe'
    download(data['LLVM_installer']['url'],installer,385658654,'3197846a2b19063687dd56e93e34cd941e3548d907f23a6131571321bdf9fe7b')
    signature=ROOT/'downloads/LLVM-20.1.8-win64.exe.sig'
    download(data['LLVM_detached_signature']['url'],signature,543,data['LLVM_detached_signature']['published_digest'].split(':')[1])
    compiler=ROOT/'toolchain/llvm20.1.8'
    marker=compiler/'UNPACK_MANIFEST.json'
    if compiler.exists() and not marker.exists():quarantine(compiler,'partial compiler unpack; retry fresh owned tree')
    if not compiler.exists():
        listing=tool([str(UNPACK),'l','-slt',str(installer)],review)
        text=Path(listing['stdout_log']).read_text(errors='replace')
        for line in text.splitlines():
            if line.startswith('Path = '):
                name=line[7:]
                if name==str(installer):continue
                assert not Path(name).is_absolute() and ':' not in name
                assert (compiler/name).resolve().is_relative_to(compiler.resolve())
            assert not line.startswith(('Symbolic Link =','Hard Link =')),'unreviewed link extraction'
        compiler.parent.mkdir(exist_ok=True)
        tool([str(UNPACK),'x','-y','-mmt=2','-o'+str(compiler),str(installer)],review)
        unpacked=[{'path':str(p.relative_to(compiler)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in compiler.rglob('*') if p.is_file()]
        marker.write_text(json.dumps({'installer_SHA256':sha(installer),'files':unpacked},indent=2))
    for row in json.loads(marker.read_text())['files']:
        p=compiler/row['path'];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
    clang=compiler/'bin/clang-cl.exe';assert clang.is_file(),'NSIS extraction shape unsupported; do not execute installer'
    receipt('compiler-unpacked',{'path':str(compiler),'clang_cl_SHA256':sha(clang),'installer_not_executed':True,'global_PATH_registry_install_changes':0,'signature_signer_trust':'NOT_INFERRED_FROM_DIGEST'})
    checkout=ROOT/'deps/windows_x64';checkout.parent.mkdir(exist_ok=True)
    hooks=ROOT/'hooks-none';hooks.mkdir(exist_ok=True)
    prefix=[str(GIT),'-c','credential.helper=','-c','core.autocrlf=false','-c','core.hooksPath='+str(hooks)]
    if not checkout.exists():
        tool(prefix+['init',str(checkout)],review)
        tool(prefix+['-C',str(checkout),'remote','add','origin','https://projects.blender.org/blender/lib-windows_x64.git'],review)
    tool(prefix+['-C',str(checkout),'fetch','--depth','1','origin',DEPS_COMMIT],review,1200)
    tool(prefix+['-C',str(checkout),'-c','filter.lfs.process=','-c','filter.lfs.smudge=','-c','filter.lfs.required=false','checkout','--detach',DEPS_COMMIT],review)
    tool(prefix+['-C',str(checkout),'fsck','--no-reflogs'],review)
    sizes=deps['unique_LFS_size_map'];oids=list(sizes)
    for start in range(0,len(oids),50):
        batch=oids[start:start+50]
        body=json.dumps({'operation':'download','transfers':['basic'],'objects':[{'oid':oid,'size':sizes[oid]} for oid in batch]}).encode()
        request=urllib.request.Request(ENDPOINT,data=body,headers={'Content-Type':'application/vnd.git-lfs+json','Accept':'application/vnd.git-lfs+json'})
        with urllib.request.urlopen(request,timeout=60) as response:answer=json.loads(response.read(1024**2))
        objects=answer['objects'];assert len(objects)==len(batch)
        def fetch(obj):
            oid=obj['oid'];assert oid in batch and obj['size']==sizes[oid] and 'error' not in obj
            action=obj['actions']['download']
            assert action['href'].startswith('https://')
            return download(action['href'],ROOT/'LFS-cache'/oid,sizes[oid],oid,extra_headers=action.get('header'))
        with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(fetch,objects))
    for row in deps['path_manifest']:
        target=checkout/row['path'];assert target.resolve().is_relative_to(checkout.resolve())
        oid=row.get('LFS_oid_sha256')
        if oid:
            cache=ROOT/'LFS-cache'/oid;assert sha(cache)==oid
            if target.exists() and target.stat().st_size==row['logical_bytes'] and sha(target)==oid:continue
            # Smudge only inside the owned pinned checkout, not any source avatar.
            shutil.copyfile(cache,target)
            assert target.stat().st_size==row['logical_bytes'] and sha(target)==oid
        else:
            payload=target.read_bytes();assert len(payload)==row['logical_bytes']
            assert hashlib.sha1(b'blob '+str(len(payload)).encode()+b'\0'+payload).hexdigest()==row['git_blob_sha1']
    resources(full=True)
    receipt('dependency-staged',{'commit':DEPS_COMMIT,'paths_verified':19077,'LFS_objects_verified':1263,
      'unique_LFS_bytes':6574796539,'logical_checkout_bytes':6983719590,'Git_pack_bytes_observed':sum(p.stat().st_size for p in (checkout/'.git/objects').rglob('*') if p.is_file())})
    receipt('acquisition-complete',{'status':'ISOLATED_RESOURCE_STAGE_ONLY_NOT_BUILD_OR_CAPTURE_APPROVAL',
      'known_payload_bytes':7054121984,'installed_Blender_GUI_touched':False,'global_toolchain_install':False,
      'next_gate':'Review staged receipts/configure, then separate owned build; actual capture needs compile/link/guards acceptance'})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');p.add_argument('--approval',type=Path);a=p.parse_args()
    if not a.execute:print(json.dumps({'status':'DRY_ONLY_NO_ROOT_CREATED_NO_NETWORK_NO_SUBPROCESS','known_payload_bytes':7054121984,'extra':'Git pack/protocol unknown','next_command':'python staged_native_acquisition.py --execute --approval <owner-reviewed-acquisition-receipt.json>'}))
    else:
        assert a.approval and a.approval.is_file()
        execute(json.loads(a.approval.read_text()))
