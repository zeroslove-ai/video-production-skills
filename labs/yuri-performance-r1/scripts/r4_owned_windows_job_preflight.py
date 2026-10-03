"""Explicit harmless owned-child preflight; separate from acquisition approval.
Only existing Python313 with a fixed print/sleep command. No GUI/source/DLL attach.
"""
from pathlib import Path
import ctypes as c,hashlib,json,os,subprocess,time
ROOT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-owned-windows-job-preflight-r2')
PYTHON=Path(r'C:/Program Files/Python313/python.exe')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def exercise(name,sleep_time,timeout,expected_exit):
    import _winapi,msvcrt
    assert os.name=='nt' and PYTHON.is_file()
    k=c.WinDLL('kernel32',use_last_error=True);handle=c.c_void_p;u32=c.c_uint32;u64=c.c_uint64;size=c.c_size_t
    class Basic(c.Structure):
        _fields_=[('ProcessTime',c.c_int64),('JobTime',c.c_int64),('Flags',u32),('MinWS',size),
          ('MaxWS',size),('ActiveLimit',u32),('Affinity',size),('Priority',u32),('Scheduling',u32)]
    class IO(c.Structure):_fields_=[(n,u64) for n in ('ReadOps','WriteOps','OtherOps','ReadBytes','WriteBytes','OtherBytes')]
    class Extended(c.Structure):_fields_=[('Basic',Basic),('IO',IO),('ProcessMem',size),('JobMem',size),('PeakProcessMem',size),('PeakJobMem',size)]
    class Accounting(c.Structure):
        _fields_=[('User',c.c_int64),('Kernel',c.c_int64),('PeriodUser',c.c_int64),('PeriodKernel',c.c_int64),
          ('Faults',u32),('Processes',u32),('Active',u32),('Terminated',u32)]
    assert c.sizeof(Extended)==144 and c.sizeof(Accounting)==48
    def bind(name,args,result):
        f=getattr(k,name);f.argtypes=args;f.restype=result;return f
    create=bind('CreateJobObjectW',[handle,c.c_wchar_p],handle)
    setinfo=bind('SetInformationJobObject',[handle,c.c_int,handle,u32],c.c_int)
    assign=bind('AssignProcessToJobObject',[handle,handle],c.c_int)
    query=bind('QueryInformationJobObject',[handle,c.c_int,handle,u32,handle],c.c_int)
    resume=bind('ResumeThread',[handle],u32)
    terminate=bind('TerminateJobObject',[handle,u32],c.c_int)
    close=bind('CloseHandle',[handle],c.c_int)
    job=create(None,None)
    if not job:raise c.WinError(c.get_last_error())
    limits=Extended();limits.Basic.Flags=0x2000|0x100|0x200|0x8|0x10
    limits.Basic.ActiveLimit=1;limits.Basic.Affinity=3
    limits.ProcessMem=limits.JobMem=256*1024**2
    process=thread=None;started=time.monotonic();row={'case':name,'status':'FAIL'}
    with (ROOT/(name+'.log')).open('xb') as log:
        try:
            if not setinfo(job,9,c.byref(limits),c.sizeof(limits)):raise c.WinError(c.get_last_error())
            hlog=msvcrt.get_osfhandle(log.fileno());os.set_handle_inheritable(hlog,True)
            startup=subprocess.STARTUPINFO();startup.dwFlags=0x100|1;startup.wShowWindow=0
            startup.hStdOutput=startup.hStdError=hlog;startup.hStdInput=0
            args=[str(PYTHON),'-c',f"import time;print('HARMLESS_OWNED_CHILD',flush=True);time.sleep({sleep_time})"]
            process,thread,pid,tid=_winapi.CreateProcess(str(PYTHON),subprocess.list2cmdline(args),
                None,None,True,0x4|0x08000000,None,str(ROOT),startup)
            os.set_handle_inheritable(hlog,False)
            if not assign(job,handle(process)):
                _winapi.TerminateProcess(process,87);raise c.WinError(c.get_last_error())
            before=Accounting()
            assert query(job,1,c.byref(before),c.sizeof(before),None) and before.Active==1
            assert resume(handle(thread))!=0xFFFFFFFF
            forced=False
            while _winapi.WaitForSingleObject(process,25)!=_winapi.WAIT_OBJECT_0:
                if time.monotonic()-started>=timeout:
                    assert terminate(job,88);forced=True
                    assert _winapi.WaitForSingleObject(process,3000)==_winapi.WAIT_OBJECT_0
                    break
            exit_code=_winapi.GetExitCodeProcess(process);after=Accounting()
            assert query(job,1,c.byref(after),c.sizeof(after),None)
            immediate_active=after.Active;cleanup_wait_started=time.monotonic()
            while after.Active and time.monotonic()-cleanup_wait_started<1:
                time.sleep(0.025)
                assert query(job,1,c.byref(after),c.sizeof(after),None)
            row.update({'pid':pid,'exit_code_observed':exit_code,'immediate_active_after_wait':immediate_active,
                        'active_after_cleanup_wait':after.Active,'cleanup_wait_seconds':time.monotonic()-cleanup_wait_started})
            assert exit_code==expected_exit and after.Active==0
            assert forced==(name=='timeout')
            row.update({'status':'PASS','pid':pid,'thread_id':tid,'exe_SHA256':sha(PYTHON),
              'created_suspended':True,'assigned_before_resume':True,'active_before_resume':before.Active,
              'exit_code':exit_code,'active_after_exit':after.Active,'timeout_forced':forced,
              'timeout_seconds':timeout,'wall_seconds':time.monotonic()-started,
              'RAM_limit_bytes':256*1024**2,'CPU_affinity_mask':3,'active_process_limit':1,
              'unrelated_process_handles':0,'large_download_approval_flag_used':False})
        finally:
            close(job)  # Kill-on-close contains this owned process alone.
            if process is not None:
                _winapi.WaitForSingleObject(process,3000);_winapi.CloseHandle(process)
            if thread is not None:_winapi.CloseHandle(thread)
            (ROOT/(name+'.json')).write_text(json.dumps(row,indent=2),encoding='utf8')
    return row
def main():
    assert not ROOT.exists(),'do not repeat/overwrite an actual preflight'
    ROOT.mkdir()
    rows=[exercise('success',0.05,3,0),exercise('timeout',10,0.3,88)]
    result={'review_mode':'HARMLESS_OWNED_CHILD_PREFLIGHT_ONLY','status':'PASS_SUCCESS_AND_TIMEOUT_OWNED_JOB',
      'cases':rows,'source':{'script':str(Path(__file__)),'SHA256':sha(Path(__file__))},
      'download_build_Blender_GPU_native_capture_jobs':0,
      'actual_acquisition_supervisor_capture_pipeline':'UNRUN; this preflight validates SDK job allocation/assignment/cleanup only',
      'memory_limit_enforcement_child_spawn_limits_negative_tests':'NOT_RUN_NOT_CLAIMED'}
    (ROOT/'OWNED_WINDOWS_JOB_PREFLIGHT_MANIFEST.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps({'status':result['status'],'PIDs':[r['pid'] for r in rows],'active_after':[r['active_after_exit'] for r in rows]}))
if __name__=='__main__':
    import sys
    if sys.argv[1:]!=['--run-owned-child-preflight']:print('DRY_DEFAULT_NO_PROCESS: opt into fixed harmless owned child preflight only')
    else:main()
