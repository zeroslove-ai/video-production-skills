"""UNRUN owned Windows process supervisor proposal; no download/build/GUI attach.
--execute requires a separate human/build review receipt. Default prints plan only.
Uses documented Windows Job APIs, never Blender memory/addresses/ctypes loading.
"""
from pathlib import Path
import argparse, ctypes as c, hashlib, json, os, shutil, subprocess, time
ROOT=Path(r'C:/YuriTransfer/native-cycles-readback-r1')
CAPTURE=ROOT/'capture'
SOURCE=Path(r'C:/Users/JAEWAN/projects/yuri-motion-previs-lab-r1/labs/yuri-performance-r1/local/model-handoff-r4/Character_Master_NeckSkin_R4.blend')
LIB=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def within(p):return p.resolve().is_relative_to(ROOT.resolve())
def run(exe, script, review, timeout=120, expected_exit=0, extra=(), command_override=None, RAM_cap=8*1024**3, processes=1, affinity=15, environment=None):
    import _winapi, msvcrt
    assert os.name=='nt' and exe.is_file()
    assert review['human_large_resource_acquisition_approved'] is True
    if command_override is not None:
        assert review['allowed_tools'][str(exe.resolve())]==sha(exe)
        assert command_override[0]==str(exe) and processes<=8 and RAM_cap<=16*1024**3
    else:
        assert within(exe) and review['compile_link_accepted'] is True and sha(exe)==review['research_exe_sha256']
        assert script.resolve() in [Path(p).resolve() for p in review['allowed_script_paths']]
        assert sha(script)==review['allowed_script_sha256'][str(script.resolve())]
        if expected_exit==0:assert review['denial_selftests_and_caller_accepted'] is True
    assert sha(SOURCE)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
    assert sha(LIB)=='6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d'
    assert shutil.disk_usage(ROOT).free>=100*1024**3
    assert CAPTURE.is_dir() and (command_override is not None or script.is_file())
    kernel=c.WinDLL('kernel32',use_last_error=True)
    u32=c.c_uint32;u64=c.c_uint64;size=c.c_size_t;handle=c.c_void_p
    class Basic(c.Structure):
        _fields_=[('ProcessTime',c.c_int64),('JobTime',c.c_int64),('Flags',u32),
          ('MinWS',size),('MaxWS',size),('ActiveLimit',u32),('Affinity',size),('Priority',u32),('Scheduling',u32)]
    class IO(c.Structure):_fields_=[(n,u64) for n in ('ReadOps','WriteOps','OtherOps','ReadBytes','WriteBytes','OtherBytes')]
    class Extended(c.Structure):_fields_=[('Basic',Basic),('IO',IO),('ProcessMem',size),('JobMem',size),('PeakProcessMem',size),('PeakJobMem',size)]
    class Accounting(c.Structure):
        _fields_=[('User',c.c_int64),('Kernel',c.c_int64),('PeriodUser',c.c_int64),('PeriodKernel',c.c_int64),
          ('Faults',u32),('Processes',u32),('Active',u32),('Terminated',u32)]
    class Memory(c.Structure):
        _fields_=[('Length',u32),('Load',u32)]+[(n,u64) for n in ('TotalPhys','AvailPhys','TotalPage','AvailPage','TotalVirtual','AvailVirtual','AvailExtended')]
    assert c.sizeof(Extended)==144 and c.sizeof(Accounting)==48 and c.sizeof(Memory)==64
    def bind(name,args,result):
        f=getattr(kernel,name);f.argtypes=args;f.restype=result;return f
    create=bind('CreateJobObjectW',[handle,c.c_wchar_p],handle)
    setinfo=bind('SetInformationJobObject',[handle,c.c_int,handle,u32],c.c_int)
    assign=bind('AssignProcessToJobObject',[handle,handle],c.c_int)
    query=bind('QueryInformationJobObject',[handle,c.c_int,handle,u32,handle],c.c_int)
    resume=bind('ResumeThread',[handle],u32)
    close=bind('CloseHandle',[handle],c.c_int)
    terminate=bind('TerminateJobObject',[handle,u32],c.c_int)
    memory_status=bind('GlobalMemoryStatusEx',[c.POINTER(Memory)],c.c_int)
    def free_ram():
        mem=Memory();mem.Length=c.sizeof(mem)
        if not memory_status(c.byref(mem)):raise c.WinError(c.get_last_error())
        return mem.AvailPhys
    assert free_ram()>=12*1024**3
    job=create(None,None)
    if not job:raise c.WinError(c.get_last_error())
    limit=Extended();limit.Basic.Flags=0x2000|0x100|0x200|0x8|0x10
    limit.Basic.ActiveLimit=processes;limit.Basic.Affinity=affinity
    limit.ProcessMem=limit.JobMem=RAM_cap
    process=thread=None;log=None;result={'status':'FAIL_PARTIAL_OUTPUTS_REJECTED'};started=time.monotonic()
    disk_start=shutil.disk_usage(ROOT).free
    try:
        if not setinfo(job,9,c.byref(limit),c.sizeof(limit)):raise c.WinError(c.get_last_error())
        # Exact SDK JobObjectExtendedLimitInformation(9). Spawn suspended so no
        # child activity precedes successful assignment to this owned job.
        token=str(time.time_ns());log_path=CAPTURE/f'owned-{token}.log';log=log_path.open('xb')
        hlog=msvcrt.get_osfhandle(log.fileno());os.set_handle_inheritable(hlog,True)
        startup=subprocess.STARTUPINFO();startup.dwFlags=0x100|1;startup.wShowWindow=0
        startup.hStdOutput=startup.hStdError=hlog;startup.hStdInput=0
        command=command_override or [str(exe),'--background','--factory-startup',str(SOURCE),'--threads','4',
                 '--python',str(script),*extra]
        process,thread,pid,tid=_winapi.CreateProcess(str(exe),subprocess.list2cmdline(command),
           None,None,True,0x4|0x08000000,environment,str(ROOT),startup)
        os.set_handle_inheritable(hlog,False)
        result={'status':'FAIL_PARTIAL_OUTPUTS_REJECTED','pid':pid,'thread_id':tid,'exe_sha256':sha(exe),'command':command,
          'spawned_suspended':True,'owned_job_only':True,'RAM_cap_bytes':RAM_cap,
          'active_process_limit':processes,'CPU_affinity_mask':affinity,'timeout_seconds':timeout}
        if not assign(job,handle(process)):
            _winapi.TerminateProcess(process,87)  # This newly owned suspended handle only.
            raise c.WinError(c.get_last_error())
        if resume(handle(thread))==0xFFFFFFFF:raise c.WinError(c.get_last_error())
        while _winapi.WaitForSingleObject(process,1000)!=_winapi.WAIT_OBJECT_0:
            disk_free=shutil.disk_usage(ROOT).free
            if time.monotonic()-started>=timeout or free_ram()<12*1024**3 or disk_free<100*1024**3 or disk_start-disk_free>=80*1024**3:
                terminate(job,88)
                _winapi.WaitForSingleObject(process,10000)
                raise RuntimeError('Owned job aborted by wall-time/free-resource guard; partial outputs rejected')
        exit_code=_winapi.GetExitCodeProcess(process)
        accounting=Accounting()
        if not query(job,1,c.byref(accounting),c.sizeof(accounting),None):raise c.WinError(c.get_last_error())
        immediate_active=accounting.Active;drain_started=time.monotonic()
        while accounting.Active and time.monotonic()-drain_started<1:
            time.sleep(0.025)
            if not query(job,1,c.byref(accounting),c.sizeof(accounting),None):raise c.WinError(c.get_last_error())
            if time.monotonic()-started>=timeout or free_ram()<12*1024**3 or shutil.disk_usage(ROOT).free<100*1024**3:
                terminate(job,88)
                raise RuntimeError('Owned job drain exceeded wall/free-resource guard; partial data rejected')
        result.update({'immediate_active_after_wait':immediate_active,'job_drain_seconds':time.monotonic()-drain_started,
                       'job_total_processes':accounting.Processes,'job_terminated_processes':accounting.Terminated})
        result.update({'exit_code':exit_code,'owned_job_active_processes_after_exit':accounting.Active,
                       'wall_seconds':time.monotonic()-started,'stdout_log':str(log_path)})
        assert exit_code==expected_exit and accounting.Active==0
        assert sha(SOURCE)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
        assert sha(LIB)=='6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d'
        if expected_exit==0 and command_override is None:
            from validate_owned_native_capture import validate
            result['data_QA']=validate(CAPTURE)
        elif expected_exit==86:
            expected_entry={'factory':'unique_ptr<Device> Device::create','session':'Session::Session',
              'scene-upload':'void Scene::device_update(','scene-kernel':'bool Scene::load_kernels(',
              'alloc':'void CPUDevice::mem_alloc','upload':'void CPUDevice::mem_copy_to',
              'copy-from':'void CPUDevice::mem_copy_from','zero':'void CPUDevice::mem_zero',
              'subptr':'device_ptr CPUDevice::mem_alloc_sub_ptr','const':'void CPUDevice::const_copy_to',
              'global':'void CPUDevice::global_alloc','kernel':'bool CPUDevice::load_kernels',
              'kernel-globals':'vector<ThreadKernelGlobalsCPU> *CPUDevice::acquire_cpu_kernel_thread_globals'}[extra[-1]]
            log.flush()
            events=[json.loads(line) for line in log_path.read_text(encoding='utf8',errors='replace').splitlines() if line.startswith('{')]
            assert any(expected_entry in row.get('denied_entry','') and row.get('before_original_body') is True for row in events)
            result['actual_guard_probe_entry']=expected_entry
        result['status']='OWNED_PROCESS_AND_DATA_QA_ONLY_NOT_RUNTIME_PBR_PASS'
        return result
    finally:
        # KILL_ON_JOB_CLOSE contains any survivor. Never enumerate/kill unrelated PIDs.
        close(job)
        if thread is not None:_winapi.CloseHandle(thread)
        if process is not None:_winapi.CloseHandle(process)
        if log:log.close()
        (CAPTURE/f'owned-supervisor-{time.time_ns()}.json').write_text(json.dumps(result,indent=2),encoding='utf8')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true')
    p.add_argument('--exe',type=Path);p.add_argument('--review',type=Path)
    p.add_argument('--script',type=Path);p.add_argument('--probe',choices=('factory','session','scene-upload','scene-kernel','alloc','upload','copy-from','zero','subptr','const','global','kernel','kernel-globals'))
    a=p.parse_args()
    if not a.execute:print('PLAN_ONLY_UNRUN: requires approved isolated binary, compile/link review, guard tests and owned root; no process launched')
    else:
        assert a.exe and a.review and a.script
        review=json.loads(a.review.read_text(encoding='utf8'))
        extra=('--',a.probe) if a.probe else ()
        print(json.dumps(run(a.exe,a.script,review,expected_exit=86 if a.probe else 0,extra=extra)))
