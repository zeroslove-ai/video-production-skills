"""Lossless YRA1 event -> NPZ converter. Raw native events, NOT reconstructed motion.
No Blender import, no network. Missing canonical request arrays remain missing.
"""
import argparse, ast, hashlib, io, json, struct, zipfile
from pathlib import Path

def decode(data):
    assert len(data)<=64*1024*1024 and data[:8]==b'YRA1\x01\0\0\0'
    pos=8; result={}; count=0
    while pos<len(data):
        assert pos+32<=len(data), 'truncated header'
        fields=struct.unpack_from('<5i3I',data,pos); pos+=32
        row,modifier,bone,vertex,entry,length,n,reserved=fields
        assert row in (0,1) and modifier in (-1,0,1) and -1<=bone<57
        assert vertex in (-1,11189,14918,21485,22227,40817) and entry>=-1
        assert reserved==0 and 0<length<=96 and n<=64 and pos+length+4*n<=len(data)
        tag=data[pos:pos+length].decode('utf8');pos+=length
        assert tag.replace('_','').isalnum(), 'unsafe tag'
        payload=data[pos:pos+4*n];pos+=4*n
        key=f'{tag}_{n}'
        contexts,values=result.setdefault(key,([],[]));contexts.append(fields[:5]);values.append(payload)
        count+=1;assert count<=100000
    return result

def npy(dtype,shape,payload):
    assert len(payload)==4*__import__('math').prod(shape)
    header=repr({'descr':dtype,'fortran_order':False,'shape':shape}).encode('ascii')
    pad=(- (10+len(header)+1))%64
    header+=b' '*pad+b'\n'
    return b'\x93NUMPY\x01\0'+struct.pack('<H',len(header))+header+payload

def convert(inputs,output):
    assert not output.exists(),'new immutable output only'
    allrows={}; receipts=[]
    for p in inputs:
        data=p.read_bytes();receipts.append({'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
        for key,(contexts,values) in decode(data).items():
            c,v=allrows.setdefault(key,([],[]));c.extend(contexts);v.extend(values)
    manifest={'classification':'RAW_EVENT_ARRAYS_NOT_LAPTOP_CANONICAL_COMPLETE_CAPTURE','inputs':receipts,'arrays':{},
      'context_columns':['row','modifier','bone','vertex','entry'],
      'coordinates':'per event tag: caller LOCAL = original body local; WORLD = direct source forward transform; co/quat/deform = original armature space',
      'not_claimed':['runtime execution by converter','all57 dq for nondeforming helpers','canonical array completeness','compiled/backend equivalence'],
      'repeated_events':'preserve occurrence order; never choose silently or overwrite duplicates'}
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for key,(contexts,values) in sorted(allrows.items()):
            n=int(key.rsplit('_',1)[1]);count=len(values)
            for name,dtype,shape,payload in ((key,'<f4',(count,n),b''.join(values)),
                (key+'_context','<i4',(count,5),b''.join(struct.pack('<5i',*c) for c in contexts))):
                z.writestr(name+'.npy',npy(dtype,shape,payload))
                manifest['arrays'][name]={'shape':shape,'dtype':dtype,'sha256':hashlib.sha256(payload).hexdigest()}
    manifest['npz_sha256']=hashlib.sha256(output.read_bytes()).hexdigest()
    target=output.with_suffix('.manifest.json');assert not target.exists()
    target.write_text(json.dumps(manifest,indent=2),encoding='utf8')
    return manifest

def selftest():
    # Synthetic format-only bytes, never saved or described as native capture.
    payload=bytes.fromhex('00000080010000000000807f') # -0, smallest positive subnormal, +inf
    record=b'YRA1\x01\0\0\0'+struct.pack('<5i3I',0,0,-1,11189,-1,4,3,0)+b'test'+payload
    assert decode(record)['test_3'][1][0]==payload
    try:decode(record[:-1])
    except AssertionError:pass
    else:raise AssertionError('truncated record accepted')
    stored=npy('<f4',(1,3),payload);assert stored[-12:]==payload
    assert ast.literal_eval(stored[10:10+struct.unpack_from('<H',stored,8)[0]].decode().strip())['descr']=='<f4'
    return {'test':'synthetic format only; signed-zero/subnormal/nonfinite bits preserved; truncated record rejected','status':'PASS','native_capture':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');p.add_argument('--input',type=Path,action='append');p.add_argument('--output',type=Path);a=p.parse_args()
    if a.self_test:print(json.dumps(selftest()))
    else:
        assert a.input and a.output;print(json.dumps(convert(a.input,a.output)))
