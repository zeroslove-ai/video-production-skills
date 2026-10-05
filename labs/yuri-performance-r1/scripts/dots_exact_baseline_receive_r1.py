"""Verify separately returned exact baseline archives; never modify native files."""
import hashlib,json,shutil,zipfile
from pathlib import Path
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
D=Path('C:/Users/JAEWAN/Downloads');O=B/'dots-exact-baseline-inputs-r1';O.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((D/'exact_blender_custody_manifest.json').read_bytes())
for name in ['exact_blender_custody_manifest.json','exact_blender_custody_README.txt']:shutil.copyfile(D/name,O/name)
receipt={'scope':'ROOT_PM_DOTS_EXACT_BASELINE_CUSTODY_COMPARE_R1','assets':[],'native_open_save_render':False}
for a in manifest['assets']:
 folder=O/a['asset_id'];folder.mkdir();parts=[];archive=folder/a['archive']['file_name']
 assert Path(a['archive']['file_name']).name==a['archive']['file_name']
 with archive.open('xb') as out:
  for part in sorted(a['parts'],key=lambda p:p['order']):
   name=part['file_name'];assert Path(name).name==name
   p=D/name;assert p.stat().st_size==part['bytes'] and sha(p)==part['sha256'],name
   shutil.copyfile(p,folder/name)
   with p.open('rb') as inp:shutil.copyfileobj(inp,out)
   parts.append({'name':name,'bytes':p.stat().st_size,'sha256':sha(p),'verified':True})
 assert archive.stat().st_size==a['archive']['bytes'] and sha(archive)==a['archive']['sha256']
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  entries=z.infolist();assert len(entries)==1 and not entries[0].is_dir()
  entry=entries[0];assert Path(entry.filename).name==a['native']['file_name'] and entry.file_size==a['native']['bytes']
  native=folder/a['native']['file_name']
  with z.open(entry) as inp,native.open('xb') as out:shutil.copyfileobj(inp,out)
 assert native.stat().st_size==a['native']['bytes'] and sha(native)==a['native']['sha256']
 receipt['assets'].append({'asset_id':a['asset_id'],'parts':parts,'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,'zip_crc_passed':True,'native':str(native),'native_bytes':native.stat().st_size,'native_sha256':sha(native),'verified':True})
(O/'BASELINE_RECEIVER_RECEIPT_R1.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=True))
