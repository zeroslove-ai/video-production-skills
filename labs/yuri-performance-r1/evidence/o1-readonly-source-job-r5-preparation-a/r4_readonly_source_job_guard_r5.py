"""Final fixed-purpose source-read Job guard. Default dry; Blender needs frozen PM review.
No acquisition/native/build route or arbitrary command override. Network isolation
is not supplied by Windows Job: fixed scripts contain no network operations.
"""
from pathlib import Path
import ctypes as c,hashlib,json,os,shutil,subprocess,sys,time
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-readonly-source-job-r5'
LAB=Path(r'C:/Users/JAEWAN/projects/yuri-motion-previs-lab-r1/labs/yuri-performance-r1')
SOURCE=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
ACTION=BASE/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
RECIPE=BASE/'o1-native-armature-full-recipe-custody-r1/SourceBodyArmatureInput_0cd0bdd7_EXACT.json'
VERIFIER=LAB/'scripts/r4_readonly_recipe_verifier_r5.py'
VERIFIER_SHA='ae2320bce7f0b38c1feade7446d94e55b46c7d6f3cea34a38ccfdf500662ebfe'
PYTHON=Path(r'C:/Program Files/Python313/python.exe')
BLENDER=Path(r'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe')
PYTHON_SHA='d87063e5597f257004c731b66c59c56c91038861c6877b1a3dca6b8c4e919125'
BLENDER_SHA='284f4041f98e113f3dc10654a7193ffaaa9bfdfec8b87fa116620a48b5f6d4cb'
EXPECTED={SOURCE:'a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa',ACTION:'6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d',RECIPE:'0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source_argv():return [str(BLENDER),'-b','--factory-startup','--disable-autoexec','-t','2',str(SOURCE),'--python-exit-code','93','--python',str(VERIFIER)]
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
    assert case in ('probe-success','probe-timeout','factory-help','source-read')
    before=hashes();initial=resources();assert resource_gate(initial),'resource preflight denied'
    guard_before=sha(Path(__file__));assert sha(VERIFIER)==VERIFIER_SHA
    if case=='source-read':
        # Exact additive scoped PM receipt must be separately provided AFTER tool review.
        # No CLI approval switch, mutable argv, download/build route, or acquisition override.
        review=json.loads((OUT/'PM_REVIEW_SOURCE_READ_APPROVED_R5.json').read_bytes())
        assert review['scope']=='INSTALLED_BLENDER_SOURCE_DATA_READ_ONLY'
        assert review['PM_reviewed_exact_final_guard_verifier_argv_and_same_guard_probes'] is True
        assert review['human_large_resource_acquisition_approved'] is False
        assert review['custom_native_build_trace_capture_approved'] is False
        assert review['guard_sha256']==guard_before and review['verifier_sha256']==VERIFIER_SHA
        assert review['blender_sha256']==BLENDER_SHA and review['argv']==source_argv()
        assert review['probe_manifest_sha256']==sha(OUT/'PROBE_MANIFEST.json')
        probe=json.loads((OUT/'PROBE_MANIFEST.json').read_bytes())
        assert probe['status']=='PASS_NORMAL_TIMEOUT_ZERO_CHILDREN' and probe['guard_sha256']==guard_before
        assert probe['factory_help']['status']=='PASS' and probe['factory_help_log_sha256']==sha(OUT/'factory-help.log')
        assert review['factory_help_log_sha256']==probe['factory_help_log_sha256']
        assert all(r['status']=='PASS' and r['total_job_processes']==1 and r['active_after_exit']==0 and r['final_job_pids']==[] for r in probe['cases'])
        assert not (OUT/'source-identity.json').exists() and not (OUT/'source-read.json').exists()
        exe=BLENDER;expected_sha=BLENDER_SHA;argv=source_argv();timeout=120;expected_exit=0
    elif case=='factory-help':
        # Newly scoped PM-authorized fixed CLI-help job; no source file or Python script.
        exe=BLENDER;expected_sha=BLENDER_SHA
        argv=[str(BLENDER),'-b','--factory-startup','--disable-autoexec','--help']
        timeout=10;expected_exit=0
    else:
        exe=PYTHON;expected_sha=PYTHON_SHA
        delay='0.5' if case=='probe-success' else '10'
        argv=[str(PYTHON),'-I','-S','-c',"import time;print('FIXED_READONLY_GUARD_PROBE',flush=True);time.sleep("+delay+")"]
        timeout=3 if case=='probe-success' else 0.8;expected_exit=0 if case=='probe-success' else 88
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
    openprocess=bind('OpenProcess',[u32,c.c_int,u32],h)
    imagepath=bind('QueryFullProcessImageNameW',[h,u32,c.c_wchar_p,c.POINTER(u32)],c.c_int)
    injob=bind('IsProcessInJob',[h,h,c.POINTER(c.c_int)],c.c_int)
    snapshot=bind('CreateToolhelp32Snapshot',[u32,u32],h)
    class ProcessEntry(c.Structure):
        _fields_=[('dwSize',u32),('cntUsage',u32),('PID',u32),('Heap',s),('Module',u32),('Threads',u32),('ParentPID',u32),('BasePriority',c.c_int32),('Flags',u32),('Exe',c.c_wchar*260)]
    first=bind('Process32FirstW',[h,c.POINTER(ProcessEntry)],c.c_int)
    nextentry=bind('Process32NextW',[h,c.POINTER(ProcessEntry)],c.c_int)
    def identities(ids):
        # Query-only handles to PIDs actually returned by this owned Job; no PID kills.
        parents={};snap=snapshot(2,0)
        if snap and snap!=c.c_void_p(-1).value:
            try:
                entry=ProcessEntry();entry.dwSize=c.sizeof(entry);ok=first(snap,c.byref(entry))
                while ok:
                    if entry.PID in ids:parents[entry.PID]={'parent_pid':entry.ParentPID,'snapshot_exe':entry.Exe}
                    ok=nextentry(snap,c.byref(entry))
            finally:close(snap)
        found=[]
        for observed_pid in ids:
            item={'pid':observed_pid,**parents.get(observed_pid,{})};handle=openprocess(0x1000,False,observed_pid)
            if handle:
                try:
                    buf=c.create_unicode_buffer(32768);length=u32(len(buf))
                    if imagepath(handle,0,buf,c.byref(length)):item['executable']=buf.value
                    else:item['image_error']=c.get_last_error()
                    ct,et,kt,ut=[FileTime() for _ in range(4)]
                    if gettimes(handle,c.byref(ct),c.byref(et),c.byref(kt),c.byref(ut)):
                        item.update(creation_FILETIME=(ct.High<<32)|ct.Low,exit_FILETIME=(et.High<<32)|et.Low)
                    match=c.c_int()
                    if injob(handle,job,c.byref(match)):item['in_this_owned_job']=bool(match.value)
                    item['exit_code_query']=_winapi.GetExitCodeProcess(int(handle))
                finally:close(handle)
            else:item['open_error']=c.get_last_error()
            found.append(item)
        return found
    job=create(None,None);assert job
    process=thread=None;assigned=False;started=time.monotonic();samples=[initial]
    row={'case':case,'status':'FAIL','argv':argv,'exe_sha256':expected_sha,'inputs_before':before,'small_read_purpose':'PM_REVIEWED_INSTALLED_SOURCE_IDENTITY_ONLY' if case=='source-read' else 'PM_AUTHORIZED_FINAL_GUARD_FIXED_PROBES_AND_CLI_HELP_ONLY','human_large_resource_acquisition_approved':False,
      'native_layout':{'Basic_size':c.sizeof(Basic),'Extended_size':c.sizeof(Extended),'Accounting_size':c.sizeof(Accounting),'PidList_ids_offset':PidList.Pids.offset,'Basic_flags_offset':Basic.Flags.offset,'Basic_active_offset':Basic.ActiveLimit.offset,'Accounting_active_offset':Accounting.Active.offset,'ProcessEntry_size':c.sizeof(ProcessEntry),'ProcessEntry_parent_offset':ProcessEntry.ParentPID.offset}}
    assert row['native_layout']=={'Basic_size':64,'Extended_size':144,'Accounting_size':48,'PidList_ids_offset':8,'Basic_flags_offset':16,'Basic_active_offset':40,'Accounting_active_offset':40,'ProcessEntry_size':568,'ProcessEntry_parent_offset':32}
    try:
        limits=Extended();limits.Basic.Flags=0x2000|0x100|0x200|0x8|0x10
        limits.Basic.ActiveLimit=1;limits.Basic.Affinity=3;limits.ProcessMem=limits.JobMem=8*1024**3
        assert setinfo(job,9,c.byref(limits),c.sizeof(limits))
        readback=Extended();assert query(job,9,c.byref(readback),c.sizeof(readback),None)
        assert readback.Basic.Flags==limits.Basic.Flags and readback.Basic.ActiveLimit==1 and readback.Basic.Affinity==3
        assert readback.ProcessMem==readback.JobMem==8*1024**3
        row['job_limit_readback_verified']=True
        with (OUT/(case+'.log')).open('xb') as log:
            fd=msvcrt.get_osfhandle(log.fileno());os.set_handle_inheritable(fd,True)
            startup=subprocess.STARTUPINFO();startup.dwFlags=0x100|1;startup.wShowWindow=0
            startup.hStdOutput=startup.hStdError=fd;startup.hStdInput=0
            try:
                # DETACHED_PROCESS denies console inheritance/allocation; stdio remains fixed log handles.
                process,thread,pid,tid=_winapi.CreateProcess(str(exe),subprocess.list2cmdline(argv),None,None,True,0x4|0x8,None,str(OUT),startup)
            finally:os.set_handle_inheritable(fd,False)
            assert getpid(h(process))==pid
            creation=FileTime();ex=FileTime();kt=FileTime();ut=FileTime()
            assert gettimes(h(process),c.byref(creation),c.byref(ex),c.byref(kt),c.byref(ut))
            row.update(pid=pid,thread_id=tid,creation_FILETIME=(creation.High<<32)|creation.Low,created_suspended=True,creation_flags=12,detached_console=True)
            if not assign(job,h(process)):
                _winapi.TerminateProcess(process,87);raise c.WinError(c.get_last_error())
            assigned=True;account=Accounting()
            assert query(job,1,c.byref(account),c.sizeof(account),None) and account.Active==1
            assert job_pids()==[pid]
            row.update(assigned_before_resume=True,active_before_resume=account.Active)
            assert resume(h(thread))!=0xFFFFFFFF
            row.update(native_process_handle=int(process),native_job_handle=int(job),guard_parent_pid=os.getpid())
            print(json.dumps({'event':'OWNED_CHILD_RESUMED','case':case,'pid':pid,'creation_FILETIME':row['creation_FILETIME'],'native_process_handle':int(process),'native_job_handle':int(job),'guard_parent_pid':os.getpid(),'exe_sha256':expected_sha}),flush=True)
            reason=None
            while True:
                sample=resources();samples.append(sample)
                sample['monotonic_since_create']=time.monotonic()-started
                sample_account=Accounting();assert query(job,1,c.byref(sample_account),c.sizeof(sample_account),None)
                sample['accounting_before_PID_query']={'active':sample_account.Active,'total':sample_account.Processes,'limit_terminated':sample_account.Terminated}
                assert sample_account.Active<=1 and sample_account.Processes==1 and sample_account.Terminated==0
                sample['owned_handle_terminal_before_identity']=(_winapi.WaitForSingleObject(process,0)==_winapi.WAIT_OBJECT_0)
                if sample['owned_handle_terminal_before_identity']:
                    # Terminal root: collect final owned-handle exit and Job drain below.
                    break
                sample['associated_job_pids']=job_pids()
                sample['PID_identities']=identities(sample['associated_job_pids'])
                assert query(job,1,c.byref(sample_account),c.sizeof(sample_account),None)
                sample['accounting_after_identity_query']={'active':sample_account.Active,'total':sample_account.Processes,'limit_terminated':sample_account.Terminated}
                assert sample['associated_job_pids'] in ([pid],[]) and sample_account.Active<=1 and sample_account.Processes==1
                for identity in sample['PID_identities']:
                    assert identity['pid']==pid,'never accept unknown Job PID'
                    if 'creation_FILETIME' in identity:assert identity['creation_FILETIME']==row['creation_FILETIME'],'altered PID creation identity'
                    if 'executable' not in identity:
                        terminal_now=(_winapi.WaitForSingleObject(process,0)==_winapi.WAIT_OBJECT_0)
                        sample['owned_handle_terminal_after_missing_image']=terminal_now
                        assert terminal_now,'missing image on LIVE owned process is failure'
                        row['terminal_image_query_race_tolerated_with_owned_handle']=True
                        break
                    assert identity['in_this_owned_job'] is True and Path(identity['executable']).resolve()==exe.resolve()
                if sample.get('owned_handle_terminal_after_missing_image'):break
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
            row.update(exit_code=code,termination_reason=reason,active_after_exit=account.Active,total_job_processes=account.Processes,limit_terminated_processes=account.Terminated)
            row['final_job_pids']=job_pids()
            assert account.Active==0 and row['final_job_pids']==[] and code==expected_exit
            # Do not equate cumulative association counts with successfully admitted PIDs.
            # Preserve the unexpected count/PID-list observation for mandatory PM review.
            assert account.Processes==1 and account.Terminated==0
            row['extra_associations']='NONE_OBSERVED_WITH_DETACHED_PROCESS'
            assert reason==('TIMEOUT' if case=='probe-timeout' else None)
            assert sha(exe)==expected_sha
            assert sha(VERIFIER)==VERIFIER_SHA and sha(Path(__file__))==guard_before
            if case=='factory-help':
                help_text=(OUT/'factory-help.log').read_text(errors='replace')
                assert '--factory-startup' in help_text and '--disable-autoexec' in help_text
                assert 'BlenderMCP' not in help_text and 'Higgsfield' not in help_text and 'MPFB' not in help_text
            if case=='source-read':
                live=json.loads((OUT/'source-identity.json').read_bytes())
                assert live['status']=='LIVE_ORIGINAL_FULL_RECIPE_BYTE_IDENTICAL'
                assert live['vertices']==63561 and live['slots']==57 and live['CSR_entries']==304799 and live['groups']==58 and live['mask_group']==52
                assert live['source_post_sha256']==EXPECTED[SOURCE] and live['recipe_post_sha256']==EXPECTED[RECIPE]
            row['status']='PASS'
    except Exception as error:
        row['error']=repr(error);raise
    finally:
        if process is not None and not assigned:_winapi.TerminateProcess(process,87)
        if process is not None and assigned:
            # Even failure retains authoritative terminal handle/accounting evidence before close.
            if _winapi.WaitForSingleObject(process,0)!=_winapi.WAIT_OBJECT_0:
                row['failure_cleanup_terminated_owned_job']=bool(terminate(job,90))
            row['cleanup_owned_handle_terminal']=(_winapi.WaitForSingleObject(process,3000)==_winapi.WAIT_OBJECT_0)
            if row['cleanup_owned_handle_terminal']:row['cleanup_owned_handle_exit_code']=_winapi.GetExitCodeProcess(process)
            cleanup=Accounting();cleanup_start=time.monotonic()
            while True:
                assert query(job,1,c.byref(cleanup),c.sizeof(cleanup),None)
                if cleanup.Active==0 or time.monotonic()-cleanup_start>=3:break
                time.sleep(0.025)
            row['cleanup_terminal_job_accounting']={'active':cleanup.Active,'total':cleanup.Processes,'limit_terminated':cleanup.Terminated}
            row['cleanup_final_job_pids']=job_pids()
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
        help_row=run('factory-help')
        result={'status':'PASS_NORMAL_TIMEOUT_ZERO_CHILDREN','cases':rows,'factory_help':help_row,'factory_help_log_sha256':sha(OUT/'factory-help.log'),'guard_sha256':sha(Path(__file__)),'Blender_CLI_help_launches':1,'Blender_source_reads':0,'native_capture_build_acquisition':False,'memory_limit_negative_test':'NOT_RUN'}
        with (OUT/'PROBE_MANIFEST.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
        print(json.dumps({'status':result['status'],'pids':[r['pid'] for r in rows],'active_after':[r['active_after_exit'] for r in rows]}))
    elif sys.argv[1:]==['--run-reviewed-source-read']:run('source-read')
    else:print('DRY_DEFAULT_NO_PROCESS: fixed probes or independently reviewed source read only')
if __name__=='__main__':main()
