"""Cooperative live identity barriers. Helper preflight is harmless; native needs NEW approval."""
import argparse,json,os,runpy,sys,time,traceback
from pathlib import Path

def write(path,value):
    temp=path.with_suffix('.tmp');assert not path.exists()
    with temp.open('x',encoding='utf8') as f:json.dump(value,f,indent=2)
    temp.rename(path)
def wait(path,seconds=90):
    deadline=time.monotonic()+seconds
    while not path.exists():
        if time.monotonic()>deadline:raise TimeoutError('Owned barrier wait expired')
        time.sleep(.02)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--kind',choices=['helper','native'],required=True)
    ap.add_argument('--gates',required=True);ap.add_argument('--collector');ap.add_argument('--collector-config')
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);g=Path(args.gates)
    assert g.is_dir()
    write(g/'INITIAL_READY.json',{'pid':os.getpid(),'kind':args.kind,'phase':'LIVE_BLOCKED_BEFORE_PAYLOAD'})
    wait(g/'START_RELEASE.json')
    status='PASS';error=None
    try:
        if args.kind=='helper':
            assert args.collector is None and args.collector_config is None
            write(g/'HELPER_PAYLOAD.json',{'pid':os.getpid(),'operation':'Python scalar arithmetic only','result':sum(range(16)),'native_Blender_calls':0})
        else:
            config=json.loads(Path(args.collector_config).read_bytes())
            original=sys.argv[:]
            try:
                sys.argv=[args.collector,'--',*config['collector_argv']]
                runpy.run_path(args.collector,run_name='__main__')
            finally:sys.argv=original
    except BaseException:
        status='FAIL';error=traceback.format_exc()
    write(g/'PAYLOAD_DONE.json',{'pid':os.getpid(),'kind':args.kind,'payload_status':status,'error':error,'phase':'LIVE_BLOCKED_BEFORE_EXIT'})
    # Parent MUST obtain strict AFTER identity while this process waits here.
    wait(g/'FINAL_RELEASE.json')
    return 0 if status=='PASS' else 95
if __name__=='__main__':sys.exit(main())
