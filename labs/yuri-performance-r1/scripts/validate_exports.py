"""Validate GLB content and sampled curves, not just file existence."""
from pathlib import Path
import json, struct, math, hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'local/output'

def read_glb(p):
    raw=p.read_bytes()
    magic,version,length=struct.unpack_from('<4sII',raw)
    assert magic==b'glTF' and version==2 and length==len(raw)
    offset=12;doc=None;binary=b''
    while offset<len(raw):
        n,kind=struct.unpack_from('<II',raw,offset);offset+=8
        block=raw[offset:offset+n];offset+=n
        if kind==0x4E4F534A:doc=json.loads(block)
        elif kind==0x004E4942:binary=block
    assert doc is not None
    return doc,binary,raw

def floats(doc,binary,index):
    a=doc['accessors'][index];v=doc['bufferViews'][a['bufferView']]
    assert a['componentType']==5126 and 'sparse' not in a
    k={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
    start=v.get('byteOffset',0)+a.get('byteOffset',0)
    stride=v.get('byteStride',4*k)
    result=[struct.unpack_from('<'+'f'*k,binary,start+i*stride) for i in range(a['count'])]
    assert all(math.isfinite(x) for row in result for x in row)
    return result

def main():
    catalog=json.loads((ROOT/'catalog/motions.json').read_text(encoding='utf-8'))
    assert len(catalog['items'])==48 and len({x['id'] for x in catalog['items']})==48
    assert catalog['completed_production_count']==0
    results=[]
    for name in catalog['proxy_seeds']:
        path=OUT/(name+'__proxy.glb');doc,binary,raw=read_glb(path)
        channels=[]
        for a in doc['animations']:
            for c in a['channels']:
                s=a['samplers'][c['sampler']]
                times=[x[0] for x in floats(doc,binary,s['input'])]
                values=floats(doc,binary,s['output'])
                assert all(b>=a for a,b in zip(times,times[1:]))
                assert abs(min(times))<1e-5, (name,min(times))
                assert abs(max(times)-95/24)<1e-4, (name,max(times))
                assert s.get('interpolation','LINEAR') in ['LINEAR','STEP']
                n=len(values)//len(times)
                assert n>=1 and n*len(times)==len(values)
                first=values[:n];last=values[-n:]
                delta=max(abs(x-y) for u,v in zip(first,last) for x,y in zip(u,v))
                assert delta<1e-4, (name,c['target'],delta)
                varying=any(values[i:i+n]!=first for i in range(0,len(values),n))
                channels.append({'path':c['target']['path'],'node':c['target'].get('node'),'samples':len(times),'varies':varying,'neutral_return_delta':delta})
        assert any(x['path']=='rotation' and x['varies'] for x in channels)
        assert any(x['path']=='weights' and x['varies'] for x in channels)
        results.append({'id':name,'status':'GLB_SAMPLED_CURVES_PASS','sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'duration_seconds':95/24,'skin_count':len(doc['skins']),'channel_count':len(channels),'varying_rotation_channels':sum(x['path']=='rotation' and x['varies'] for x in channels),'varying_weight_channels':sum(x['path']=='weights' and x['varies'] for x in channels),'finite_values':True,'timestamps_monotonic':True,'starts_at_zero':True,'neutral_return_pass':True,'actual_yuri_retarget_tested':False})
    result={'status':'PASS','catalog_count':48,'production_approved_count':0,'proxy_clip_count':3,'tests':['unique_catalog_ids','GLB_header_and_length','finite_sample_values','monotonic_timestamps','per_clip_zero_start','per_clip_duration','rotation_curves_vary','morph_curves_vary','first_last_neutral_equivalence'],'results':results}
    (ROOT/'evidence/export_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
if __name__=='__main__':main()
