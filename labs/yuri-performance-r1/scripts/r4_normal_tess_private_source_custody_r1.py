"""Read two pinned small Git blobs; keep private consumer code outside public Git."""
from pathlib import Path
import subprocess,json,base64,hashlib
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-normal-tess-domain-contract-r1')
assert not OUT.exists();OUT.mkdir()
rows=[]
for name,blob in [('O1SourceBodyTessellation.cs','e778820b3ada85a728957a2bfe2d1214db8b8ade'),('O1SourceCornerNormals.cs','27bbb11451c2a52365ad62ae384fa579e0b8f19a')]:
    q=json.loads(subprocess.check_output(['gh','api','repos/zeroslove-ai/yuri-room-mvp/git/blobs/'+blob]))
    raw=base64.b64decode(q['content'])
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==blob
    with (OUT/name).open('xb') as f:f.write(raw)
    rows.append({'name':name,'gitblob':blob,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'commit':'8bacd64bfb64e327ccbcdfba615cbd05f4c8576d'})
(OUT/'PRIVATE_CONSUMER_SOURCE_CUSTODY.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(json.dumps(rows))
