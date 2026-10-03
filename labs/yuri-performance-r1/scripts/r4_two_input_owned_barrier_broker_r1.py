"""Fixed config broker. --helper-preflight allowed; --native requires NEW exact approval.
Changed hypothesis: query BOTH original handle and explicit LIMITED_QUERY handle
at cooperative BEFORE/AFTER live barriers, never during native interpreter teardown.
"""
import argparse,ctypes as c,hashlib,json,os,subprocess,time,traceback
from pathlib import Path

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
    with Path(p).open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
def run(config_path,helper,approval_path=None):
    import _winapi,msvcrt
    assert os.name=='nt' and c.sizeof(c.c_void_p)==8
    cfg=json.loads(config_path.read_bytes());assert cfg['broker_sha256']==sha(__file__)
    before={p:sha(p) for p in cfg['pinned_files']};assert before==cfg['pinned_files']
    route=cfg['helper'] if helper else cfg['native']
    if not helper:
        assert Path(approval_path).resolve()==Path(route['approval_path']).resolve()
        approval=json.loads(Path(approval_path).read_bytes())
        assert approval['new_exact_packet_authorized'] is True and approval['historical_sampler_approval_reused'] is False
        assert approval['config_sha256']==sha(config_path) and approval['broker_sha256']==sha(__file__)
        assert approval['collector_sha256']==cfg['collector_sha256'] and approval['argv']==route['argv']
        assert approval['preflight_result_sha256']==sha(cfg['helper']['result_path'])
        assert json.loads(Path(cfg['helper']['result_path']).read_bytes())['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN'
    gates=Path(route['gates']);out=Path(route['result_path']);assert not gates.exists() and not out.exists()
    gates.mkdir();assert sha(route['argv'][0])==route['executable_sha256']
    k=c.WinDLL('kernel32',use_last_error=True);H=c.c_void_p;U=c.c_uint32;S=c.c_size_t;L=c.c_uint64
    def bind(n,a,r):f=getattr(k,n);f.argtypes=a;f.restype=r;return f
    class Basic(c.Structure):_fields_=[('ProcessTime',c.c_int64),('JobTime',c.c_int64),('Flags',U),('MinWS',S),('MaxWS',S),('ActiveLimit',U),('Affinity',S),('Priority',U),('Scheduling',U)]
    class IO(c.Structure):_fields_=[(n,L) for n in ['ReadOps','WriteOps','OtherOps','ReadBytes','WriteBytes','OtherBytes']]
    class Extended(c.Structure):_fields_=[('Basic',Basic),('IO',IO),('ProcessMem',S),('JobMem',S),('PeakProcessMem',S),('PeakJobMem',S)]
    class Accounting(c.Structure):_fields_=[('User',c.c_int64),('Kernel',c.c_int64),('PeriodUser',c.c_int64),('PeriodKernel',c.c_int64),('Faults',U),('Processes',U),('Active',U),('Terminated',U)]
    class Pids(c.Structure):_fields_=[('Assigned',U),('Count',U),('Pids',S*16)]
    class FT(c.Structure):_fields_=[('Low',U),('High',U)]
    class PE(c.Structure):_fields_=[('size',U),('usage',U),('pid',U),('heap',S),('module',U),('threads',U),('parent',U),('priority',c.c_long),('flags',U),('exe',c.c_wchar*260)]
    assert (c.sizeof(Extended),c.sizeof(Accounting),Pids.Pids.offset)==(144,48,8)
    create=bind('CreateJobObjectW',[H,c.c_wchar_p],H);close=bind('CloseHandle',[H],c.c_int)
    setinfo=bind('SetInformationJobObject',[H,c.c_int,H,U],c.c_int);query=bind('QueryInformationJobObject',[H,c.c_int,H,U,H],c.c_int)
    assign=bind('AssignProcessToJobObject',[H,H],c.c_int);resume=bind('ResumeThread',[H],U)
    terminate=bind('TerminateJobObject',[H,U],c.c_int);getpid=bind('GetProcessId',[H],U)
    times=bind('GetProcessTimes',[H,H,H,H,H],c.c_int);image=bind('QueryFullProcessImageNameW',[H,U,c.POINTER(c.c_wchar),c.POINTER(U)],c.c_int)
    openprocess=bind('OpenProcess',[U,c.c_int,U],H);injob=bind('IsProcessInJob',[H,H,c.POINTER(c.c_int)],c.c_int)
    snap=bind('CreateToolhelp32Snapshot',[U,U],H);first=bind('Process32FirstW',[H,c.POINTER(PE)],c.c_int);nextp=bind('Process32NextW',[H,c.POINTER(PE)],c.c_int)
    def parent(pid):
        s=snap(2,0);assert s and s!=H(-1).value
        try:
            pe=PE();pe.size=c.sizeof(pe);ok=first(s,c.byref(pe))
            while ok:
                if pe.pid==pid:return pe.parent
                ok=nextp(s,c.byref(pe))
            raise RuntimeError('Owned child absent from OS parent snapshot')
        finally:assert close(s)
    job=create(None,None);assert job
    process=thread=qhandle=None;assigned=False;row={'guard_status':'FAIL','route':'HELPER_PREFLIGHT' if helper else 'NATIVE','native_Blender_launched':not helper,
        'changed_hypothesis':'Cooperative initial and postpayload preexit barriers plus new LIMITED_QUERY handle; both original/limited queries strict; no teardown race or query-error waiver',
        'broker_sha256':sha(__file__),'config_sha256':sha(config_path),'argv':route['argv'],'inputs_before':before,'cleanup_errors':[]}
    start=time.monotonic();limits=cfg['limits'];watch=30 if helper else limits['wall_seconds']
    def terminal():return _winapi.WaitForSingleObject(process,0)==_winapi.WAIT_OBJECT_0
    def jobinfo():
        a=Accounting();ps=Pids();assert query(job,1,c.byref(a),c.sizeof(a),None);assert query(job,3,c.byref(ps),c.sizeof(ps),None)
        return {'active':a.Active,'total':a.Processes,'limit_terminated':a.Terminated,'pids':list(ps.Pids[:ps.Count])}
    def identity(label):
        assert not terminal(),label+' requires live owned process'
        result={'phase':label,'owned_pid':pid,'owned_process_handle':int(process),'limited_query_handle':int(qhandle)}
        for name,handle in [('original',process),('limited',qhandle)]:
            assert getpid(H(handle))==pid
            f=[FT() for _ in range(4)];assert times(H(handle),*[c.byref(x) for x in f])
            creation=(f[0].High<<32)|f[0].Low
            buf=c.create_unicode_buffer(32768);length=U(len(buf));c.set_last_error(0)
            ok=image(H(handle),0,buf,c.byref(length));err=c.get_last_error()
            result[name]={'QueryFullProcessImageName_success':bool(ok),'error':err,'image':buf.value,'creation_FILETIME':creation}
            row[label]=result # retain partial evidence before failing
            assert ok,('Strict live image query failure',label,name,err)
            assert Path(buf.value).resolve()==Path(route['argv'][0]).resolve()
            assert creation==row['creation_FILETIME']
        assert not terminal()
        belongs=c.c_int();assert injob(H(process),job,c.byref(belongs)) and belongs.value
        j=jobinfo();result['job']=j;assert j=={'active':1,'total':1,'limit_terminated':0,'pids':[pid]}
        result.update(parent_pid=parent(pid),job=j,owned_handle_signaled=False)
        assert result['parent_pid']==os.getpid()
        return result
    def wait_gate(name):
        while not (gates/name).exists():
            assert not terminal(),'Owned child exited before live barrier'
            assert time.monotonic()-start<watch,'WATCHDOG'
            total=sum(p.stat().st_size for p in gates.rglob('*') if p.is_file())
            capture=Path(cfg['native']['capture_output'])
            if not helper and capture.exists():total+=sum(p.stat().st_size for p in capture.rglob('*') if p.is_file())
            assert total<limits['output_bytes'],'COMBINED_OUTPUT_CAP'
            _winapi.WaitForSingleObject(process,20)
        v=json.loads((gates/name).read_bytes());assert v['pid']==pid
        return v
    try:
        limit=Extended();limit.Basic.Flags=0x2000|0x100|0x200|0x8|0x10;limit.Basic.ActiveLimit=1;limit.Basic.Affinity=3
        limit.ProcessMem=limit.JobMem=limits['memory_bytes'];assert setinfo(job,9,c.byref(limit),c.sizeof(limit))
        rb=Extended();assert query(job,9,c.byref(rb),c.sizeof(rb),None)
        row['native_job_limit_readback']={'flags':rb.Basic.Flags,'active':rb.Basic.ActiveLimit,'affinity':rb.Basic.Affinity,'process_memory':rb.ProcessMem,'job_memory':rb.JobMem}
        assert row['native_job_limit_readback']=={'flags':limit.Basic.Flags,'active':1,'affinity':3,'process_memory':limits['memory_bytes'],'job_memory':limits['memory_bytes']}
        row['job_before_create']=jobinfo()
        with (gates/'owned.log').open('xb') as log,open(os.devnull,'rb') as null:
            lh=msvcrt.get_osfhandle(log.fileno());nh=msvcrt.get_osfhandle(null.fileno())
            for handle in [lh,nh]:os.set_handle_inheritable(handle,True)
            si=subprocess.STARTUPINFO();si.dwFlags=0x100|1;si.wShowWindow=0;si.hStdOutput=si.hStdError=lh;si.hStdInput=nh
            si.lpAttributeList={'handle_list':[lh,nh]}
            row['creation_flags']=limits['creation_flags']
            assert limits['creation_flags']==0x8000c # DETACHED_PROCESS|SUSPENDED|EXTENDED_STARTUPINFO, no implicit console
            try:process,thread,pid,tid=_winapi.CreateProcess(route['argv'][0],route.get('command_line',subprocess.list2cmdline(route['argv'])),None,None,True,limits['creation_flags'],None,str(gates),si)
            finally:
                for handle in [lh,nh]:os.set_handle_inheritable(handle,False)
            row.update(pid=pid,parent_pid=os.getpid(),process_handle=int(process),thread_id=tid)
            row['job_before_assign']=jobinfo()
            ft=[FT() for _ in range(4)];assert times(H(process),*[c.byref(x) for x in ft]);row['creation_FILETIME']=(ft[0].High<<32)|ft[0].Low
            if not assign(job,H(process)):
                _winapi.TerminateProcess(process,87);raise c.WinError(c.get_last_error())
            assigned=True;row['job_after_assign_before_resume']=jobinfo()
            write(gates/'OWNED_PID.json',{'pid':pid})
            (gates/'OWNED_PID.txt').write_text(str(pid),encoding='ascii')
            assert resume(H(thread))!=0xffffffff
            qhandle=openprocess(0x1000|0x100000,False,pid);assert qhandle
            row['initial_barrier']=wait_gate('INITIAL_READY.json');b=identity('BEFORE')
            write(gates/'guard-before.json',{'status':'STRICT_IDENTITY_BEFORE_PASS','owned_pid':pid,'creation_FILETIME':row['creation_FILETIME'],
                'QueryFullProcessImageName_success':True,'job_active_limit':1,'executable_sha256':route['executable_sha256'],'identity':b})
            write(gates/'START_RELEASE.json',{'owned_pid':pid,'strict_BEFORE_pass':True})
            row['payload']=wait_gate('PAYLOAD_DONE.json');identity('AFTER')
            write(gates/'FINAL_RELEASE.json',{'owned_pid':pid,'strict_AFTER_pass':True})
            remaining=max(1,int((watch-(time.monotonic()-start))*1000))
            assert _winapi.WaitForSingleObject(process,remaining)==_winapi.WAIT_OBJECT_0
            row['terminal_owned_handle_signaled']=True;row['terminal_exit_code']=_winapi.GetExitCodeProcess(process)
            assert row['terminal_exit_code']==0 and row['payload']['payload_status']=='PASS'
            deadline=time.monotonic()+3
            while jobinfo()['active'] and time.monotonic()<deadline:time.sleep(.02)
            row['terminal_job']=jobinfo();assert row['terminal_job']=={'active':0,'total':1,'limit_terminated':0,'pids':[]}
            row['combined_payload_output_bytes']=sum(p.stat().st_size for p in gates.rglob('*') if p.is_file())
            capture=Path(cfg['native']['capture_output'])
            if not helper and capture.exists():row['combined_payload_output_bytes']+=sum(p.stat().st_size for p in capture.rglob('*') if p.is_file())
            assert row['combined_payload_output_bytes']<limits['output_bytes']
            assert {p:sha(p) for p in before}==before
            row['guard_status']='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN'
    except BaseException:row['error']=traceback.format_exc()
    finally:
        def safe(name,fn):
            try:row[name]=fn()
            except BaseException:row['cleanup_errors'].append({'operation':name,'error':traceback.format_exc()})
        if process is not None:
            if not terminal():
                safe('cleanup_terminate_owned_only',lambda:bool(terminate(job,90)) if assigned else _winapi.TerminateProcess(process,87))
            safe('cleanup_signaled',lambda:_winapi.WaitForSingleObject(process,3000)==_winapi.WAIT_OBJECT_0)
            safe('cleanup_exit',lambda:_winapi.GetExitCodeProcess(process))
            if assigned:
                def drain():
                    deadline=time.monotonic()+3
                    while jobinfo()['active'] and time.monotonic()<deadline:time.sleep(.02)
                    return True
                safe('cleanup_drain',drain)
                safe('cleanup_job_before_close',jobinfo)
        safe('job_close',lambda:bool(close(job)))
        if qhandle is not None:safe('limited_handle_close',lambda:bool(close(qhandle)))
        if process is not None:safe('owned_handle_close',lambda:_winapi.CloseHandle(process))
        if thread is not None:safe('owned_thread_close',lambda:_winapi.CloseHandle(thread))
        safe('inputs_after',lambda:{p:sha(p) for p in before})
        if row['cleanup_errors'] or not row.get('job_close') or not row.get('cleanup_signaled') or row.get('cleanup_job_before_close',{}).get('active')!=0 or row.get('inputs_after')!=before:row['guard_status']='FAIL'
        row['wall_seconds']=time.monotonic()-start
        write(out,row)
    print(json.dumps({'guard_status':row['guard_status'],'result':str(out),'result_sha256':sha(out),'native_Blender_launched':not helper}))
    return 0 if row['guard_status'].startswith('PASS') else 1
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',type=Path,required=True)
    mode=ap.add_mutually_exclusive_group(required=True);mode.add_argument('--helper-preflight',action='store_true');mode.add_argument('--native',action='store_true')
    ap.add_argument('--new-approval',type=Path);a=ap.parse_args()
    if a.native:assert a.new_approval is not None,'NEW native approval absent; historical approval forbidden'
    return run(a.config,a.helper_preflight,a.new_approval)
if __name__=='__main__':raise SystemExit(main())
