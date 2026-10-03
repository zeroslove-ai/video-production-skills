"""Additive fixed-purpose Job guard. Default dry; Blender needs frozen PM review.
No acquisition/native/build route or arbitrary command override. Network isolation
is not supplied by Windows Job: fixed scripts contain no network operations.
"""
from pathlib import Path
import ctypes as c,hashlib,json,os,shutil,subprocess,sys,time
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-readonly-recipe-guard-r1-final'
LAB=Path(r'C:/Users/JAEWAN/projects/yuri-motion-previs-lab-r1/labs/yuri-performance-r1')
SOURCE=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
ACTION=BASE/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
RECIPE=BASE/'o1-native-armature-full-recipe-custody-r1/SourceBodyArmatureInput_0cd0bdd7_EXACT.json'
VERIFIER=LAB/'scripts/r4_readonly_recipe_verifier_r1.py'
PYTHON=Path(r'C:/Program Files/Python313/python.exe')
BLENDER=Path(r'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe')
PYTHON_SHA='d87063e5597f257004c731b66c59c56c91038861c6877b1a3dca6b8c4e919125'
BLENDER_SHA='284f4041f98e113f3dc10654a7193ffaaa9bfdfec8b87fa116620a48b5f6d4cb'
EXPECTED={SOURCE:'a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa',ACTION:'6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d',RECIPE:'0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source_argv():return [str(BLENDER),'-b','--disable-autoexec',str(SOURCE),'-t','2','--python-exit-code','93','--python',str(VERIFIER)]
def hashes():
    actual={str(p):sha(p) for p in EXPECTED}
    assert all(actual[str(p)]==v for p,v in EXPECTED.items()),'immutable input drift'
    return actual
class Memory(c.Structure):
    _fields_=[('Length',c.c_uint32),('Load',c.c_uint32)]+[(n,c.c_uint64) for n in ('TotalPhys','AvailPhys','TotalPage','AvailPage','TotalVirtual','AvailVirtual','AvailExtended')]
def resources():
    m=Memory();m.Length=c.sizeof(m)
    assert c.windll.kernel32.GlobalMemoryStatusEx(c.byref(m))
    free=shutil.disk_usage('C:/').free
    return {'free_RAM_bytes':m.AvailPhys,'free_C_bytes':free}
def resource_gate(r):return r['free_RAM_bytes']>=12*1024**3 and r['free_C_bytes']>=100*1024**3
def run(case):
    import _winapi,msvcrt
    assert os.name=='nt'
    assert case in ('probe-success','probe-timeout','source-read')
    before=hashes();initial=resources();assert resource_gate(initial),'resource preflight denied'
    if case=='source-read':
        # Missing review denies BEFORE any child is created. No CLI approval switches.
        review=json.loads((OUT/'PM_REVIEW_SOURCE_READ_APPROVED.json').read_bytes())
        assert review['scope']=='INSTALLED_BLENDER_SOURCE_DATA_READ_ONLY'
        assert review['PM_reviewed_frozen_guard_verifier_argv_and_actual_probe_receipts'] is True
        assert review['human_large_resource_acquisition_approved'] is False
        assert review['guard_sha256']==sha(Path(__file__)) and review['verifier_sha256']==sha(VERIFIER)
        assert review['argv']==source_argv() and review['blender_sha256']==BLENDER_SHA
        assert review['probe_manifest_sha256']==sha(OUT/'PROBE_MANIFEST.json')
        probe=json.loads((OUT/'PROBE_MANIFEST.json').read_bytes())
        assert probe['status']=='PASS_NORMAL_TIMEOUT_ZERO_CHILDREN'
        exe=BLENDER;expected_sha=BLENDER_SHA;argv=source_argv();timeout=120;expected_exit=0
    else:
        exe=PYTHON;expected_sha=PYTHON_SHA
        delay='0.05' if case=='probe-success' else '10'
        argv=[str(PYTHON),'-I','-c',"import time;print('FIXED_READONLY_GUARD_PROBE',flush=True);time.sleep("+delay+")"]
        timeout=3 if case=='probe-success' else 0.3;expected_exit=0 if case=='probe-success' else 88
    assert sha(exe)==expected_sha
    k=c.WinDLL('kernel32',use_last_error=True);h=c.c_void_p;u32=c.c_uint32;u64=c.c_uint64;s=c.c_size_t
    class Basic(c.Structure):
        _fields_=[('ProcessTime',c.c_int64),('JobTime',c.c_int64),('Flags',u32),('MinWS',s),('MaxWS',s),('ActiveLimit',u32),('Affinity',s),('Priority',u32),('Scheduling',u32)]
    class IO(c.Structure):_fields_=[(n,u64) for n in ('ReadOps','WriteOps','OtherOps','ReadBytes','WriteBytes','OtherBytes')]
    class Extended(c.Structure):_fields_=[('Basic',Basic),('IO',IO),('ProcessMem',s),('JobMem',s),('PeakProcessMem',s),('PeakJobMem',s)]
    class Accounting(c.Structure):_fields_=[('User',c.c_int64),('Kernel',c.c_int64),('PeriodUser',c.c_int64),('PeriodKernel',c.c_int64),('Faults',u32),('Processes',u32),('Active',u32),('Terminated',u32)]
    def bind(name,args,result):
        f=getattr(k,name);f.argtypes=args;f.restype=result;return f
    create=bind('CreateJobObjectW',[h,c.c_wchar_p],h);setinfo=bind('SetInformationJobObject',[h,c.c_int,h,u32],c.c_int)
    assign=bind('AssignProcessToJobObject',[h,h],c.c_int);query=bind('QueryInformationJobObject',[h,c.c_int,h,u32,h],c.c_int)
    resume=bind('ResumeThread',[h],u32);terminate=bind('TerminateJobObject',[h,u32],c.c_int);close=bind('CloseHandle',[h],c.c_int)
    getpid=bind('GetProcessId',[h],u32)
    class PidList(c.Structure):_fields_=[('Assigned',u32),('Count',u32),('Pids',s*16)]
    def job_pids():
        ids=PidList();assert query(job,3,c.byref(ids),c.sizeof(ids),None)
        assert ids.Count<=16
        return list(ids.Pids[:ids.Count])
    class FileTime(c.Structure):_fields_=[('Low',u32),('High',u32)]
    gettimes=bind('GetProcessTimes',[h,h,h,h,h],c.c_int)
    job=create(None,None);assert job
    process=thread=None;assigned=False;started=time.monotonic();samples=[initial]
    row={'case':case,'status':'FAIL','argv':argv,'exe_sha256':expected_sha,'inputs_before':before,'small_read_purpose':'PM_AUTHORIZED_PREPARE_AND_FIXED_PROBES_ONLY' if case!='source-read' else review['scope'],'human_large_resource_acquisition_approved':False}
    try:
        limits=Extended();limits.Basic.Flags=0x2000|0x100|0x200|0x8|0x10
        limits.Basic.ActiveLimit=1;limits.Basic.Affinity=3;limits.ProcessMem=limits.JobMem=8*1024**3
        assert setinfo(job,9,c.byref(limits),c.sizeof(limits))
        with (OUT/(case+'.log')).open('xb') as log:
            fd=msvcrt.get_osfhandle(log.fileno());os.set_handle_inheritable(fd,True)
            startup=subprocess.STARTUPINFO();startup.dwFlags=0x100|1;startup.wShowWindow=0
            startup.hStdOutput=startup.hStdError=fd;startup.hStdInput=0
            try:
                process,thread,pid,tid=_winapi.CreateProcess(str(exe),subprocess.list2cmdline(argv),None,None,True,0x4|0x08000000,None,str(OUT),startup)
            finally:os.set_handle_inheritable(fd,False)
            assert getpid(h(process))==pid
            creation=FileTime();ex=FileTime();kt=FileTime();ut=FileTime()
            assert gettimes(h(process),c.byref(creation),c.byref(ex),c.byref(kt),c.byref(ut))
            row.update(pid=pid,thread_id=tid,creation_FILETIME=(creation.High<<32)|creation.Low,created_suspended=True)
            if not assign(job,h(process)):
                _winapi.TerminateProcess(process,87);raise c.WinError(c.get_last_error())
            assigned=True;account=Accounting()
            assert query(job,1,c.byref(account),c.sizeof(account),None) and account.Active==1
            assert job_pids()==[pid]
            row.update(assigned_before_resume=True,active_before_resume=account.Active)
            assert resume(h(thread))!=0xFFFFFFFF
            reason=None
            while True:
                sample=resources();samples.append(sample)
                sample['active_job_pids']=job_pids();assert sample['active_job_pids'] in ([pid],[])
                if not resource_gate(sample):reason='RESOURCE_FLOOR';assert terminate(job,89);break
                if _winapi.WaitForSingleObject(process,25)==_winapi.WAIT_OBJECT_0:break
                if time.monotonic()-started>=timeout:reason='TIMEOUT';assert terminate(job,88);break
            assert _winapi.WaitForSingleObject(process,3000)==_winapi.WAIT_OBJECT_0
            code=_winapi.GetExitCodeProcess(process)
            drain=time.monotonic()
            while True:
                assert query(job,1,c.byref(account),c.sizeof(account),None)
                if account.Active==0 or time.monotonic()-drain>=3:break
                time.sleep(0.025)
            row.update(exit_code=code,termination_reason=reason,active_after_exit=account.Active,total_job_processes=account.Processes)
            row['final_job_pids']=job_pids()
            assert account.Active==0 and row['final_job_pids']==[] and code==expected_exit
            row['total_process_counter_is_not_unique_admitted_PID_count']='Observed Windows cumulative counter; recorded verbatim, no inference of admitted child identity'
            assert reason==('TIMEOUT' if case=='probe-timeout' else None)
            assert sha(exe)==expected_sha
            if case=='source-read':
                live=json.loads((OUT/'source-identity.json').read_bytes())
                assert live['status']=='LIVE_ORIGINAL_FULL_RECIPE_BYTE_IDENTICAL'
            row['status']='PASS'
    except Exception as error:
        row['error']=repr(error);raise
    finally:
        if process is not None and not assigned:_winapi.TerminateProcess(process,87)
        close(job) # Own job only, including on exception; never looks up unrelated PIDs.
        if process is not None:
            row['owned_process_signaled_after_job_close']=(_winapi.WaitForSingleObject(process,3000)==_winapi.WAIT_OBJECT_0)
            _winapi.CloseHandle(process)
        if thread is not None:_winapi.CloseHandle(thread)
        row.update(resources_samples=samples,wall_seconds=time.monotonic()-started,limits={'affinity_mask':3,'process_and_job_RAM_bytes':8*1024**3,'active_process_limit':1,'watchdog_seconds':timeout,'kill_on_close':True},inputs_after=hashes(),guard_sha256=sha(Path(__file__)))
        with (OUT/(case+'.json')).open('x',encoding='utf8') as f:json.dump(row,f,indent=2)
    return row
def main():
    if sys.argv[1:]==['--prove-fixed-probes']:
        assert not OUT.exists(),'immutable evidence output already exists'
        OUT.mkdir()
        rows=[run('probe-success'),run('probe-timeout')]
        result={'status':'PASS_NORMAL_TIMEOUT_ZERO_CHILDREN','cases':rows,'guard_sha256':sha(Path(__file__)),'Blender_launches':0,'native_capture_build_acquisition':False,'memory_limit_negative_test':'NOT_RUN'}
        with (OUT/'PROBE_MANIFEST.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
        print(json.dumps({'status':result['status'],'pids':[r['pid'] for r in rows],'active_after':[r['active_after_exit'] for r in rows]}))
    elif sys.argv[1:]==['--run-reviewed-source-read']:run('source-read')
    else:print('DRY_DEFAULT_NO_PROCESS: fixed probes or independently reviewed source read only')
if __name__=='__main__':main()
