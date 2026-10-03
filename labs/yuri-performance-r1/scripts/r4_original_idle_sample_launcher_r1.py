"""Prepared fixed route only. Dry by default; exact external review required.

R5 Job ownership/limits reused; no probe/help/retry/arbitrary-command routes.
Windows Job is not network isolation. No runtime validation in preparation.
"""
from pathlib import Path
import ctypes as c
import hashlib, json, os, shutil, subprocess, sys, time, traceback

LAB = Path('C:/Users/JAEWAN/projects/yuri-motion-previs-lab-r1/labs/yuri-performance-r1')
BASE = Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT = BASE / 'o1-original-idle-sampling-r1'
CONFIG = LAB / 'evidence/o1-original-idle-sampling-preparation-r1/FIXED_ROUTE_CONFIG_R1.json'
PROPOSAL = LAB / 'evidence/o1-original-idle-sampling-preparation-r1/SAMPLING_PROPOSAL_R1.json'
COLLECTOR = LAB / 'scripts/r4_original_idle_sample_r1.py'
EXE = Path('C:/Program Files/Blender Foundation/Blender 5.2/blender.exe')
REVIEW = OUT / 'PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R1.json'

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''): h.update(b)
    return h.hexdigest()

class Memory(c.Structure):
    _fields_ = [('Length', c.c_uint32), ('Load', c.c_uint32)] + [(n, c.c_uint64) for n in ('TotalPhys', 'AvailPhys', 'TotalPage', 'AvailPage', 'TotalVirtual', 'AvailVirtual', 'AvailExtended')]

def resources():
    m = Memory(); m.Length = c.sizeof(m)
    if not c.windll.kernel32.GlobalMemoryStatusEx(c.byref(m)): raise c.WinError()
    return {'free_RAM_bytes': m.AvailPhys, 'free_C_bytes': shutil.disk_usage('C:/').free}

def resource_gate(r): return r['free_RAM_bytes'] >= 12*1024**3 and r['free_C_bytes'] >= 100*1024**3

def preflight():
    config = json.loads(CONFIG.read_bytes())
    proposal = json.loads(PROPOSAL.read_bytes())
    review = json.loads(REVIEW.read_bytes())
    assert review['scope'] == 'ORIGINAL_IDLE_EXPLICIT_FOUR_QA_BINDING_145_FRAME_SAMPLING'
    assert review['approved'] is True and review['reviewed_owned_job_terminal_behavior'] is True
    assert review['custom_native_build_trace_capture_approved'] is False
    assert review['large_resource_acquisition_approved'] is False
    for field, p in [('launcher_sha256', Path(__file__)), ('config_sha256', CONFIG), ('proposal_sha256', PROPOSAL), ('collector_sha256', COLLECTOR)]:
        assert review[field] == sha(p), ('review binding', field)
    assert config['launcher_sha256'] == sha(__file__)
    assert config['proposal_sha256'] == sha(PROPOSAL) and config['collector_sha256'] == sha(COLLECTOR)
    assert review['argv'] == config['argv'] == proposal['argv']
    assert config['argv'][0] == str(EXE) and config['argv'][-1] == str(COLLECTOR)
    assert review['blender_sha256'] == config['blender_sha256'] == proposal['blender_sha256'] == sha(EXE)
    assert config['output_directory'] == str(OUT)
    assert config['limits'] == {'affinity_mask': 3, 'process_memory_bytes': 8*1024**3, 'job_memory_bytes': 8*1024**3, 'active_process_limit': 1, 'watchdog_seconds': 120, 'kill_on_close': True, 'creation_flags': 12}
    assert not (OUT/'OWNED_JOB_RESULT_R1.json').exists() and not (OUT/'fixed-capture.log').exists()
    assert not list(OUT.glob('*.npz')) and not (OUT/'IDLE_SAMPLING_RESULT_R1.json').exists()
    before = {p: sha(p) for p in proposal['inputs']}
    assert all(before[p] == row['sha256'] for p, row in proposal['inputs'].items())
    assert resource_gate(resources()), 'resource preflight floor'
    return config, before

def run():
    import _winapi, msvcrt
    assert os.name == 'nt' and c.sizeof(c.c_void_p) == 8
    config, before = preflight()
    k = c.WinDLL('kernel32', use_last_error=True)
    h, u32, u64, size = c.c_void_p, c.c_uint32, c.c_uint64, c.c_size_t
    class Basic(c.Structure):
        _fields_ = [('ProcessTime', c.c_int64), ('JobTime', c.c_int64), ('Flags', u32), ('MinWS', size), ('MaxWS', size), ('ActiveLimit', u32), ('Affinity', size), ('Priority', u32), ('Scheduling', u32)]
    class IO(c.Structure): _fields_ = [(n, u64) for n in ('ReadOps', 'WriteOps', 'OtherOps', 'ReadBytes', 'WriteBytes', 'OtherBytes')]
    class Extended(c.Structure): _fields_ = [('Basic', Basic), ('IO', IO), ('ProcessMem', size), ('JobMem', size), ('PeakProcessMem', size), ('PeakJobMem', size)]
    class Accounting(c.Structure): _fields_ = [('User', c.c_int64), ('Kernel', c.c_int64), ('PeriodUser', c.c_int64), ('PeriodKernel', c.c_int64), ('Faults', u32), ('Processes', u32), ('Active', u32), ('Terminated', u32)]
    class Pids(c.Structure): _fields_ = [('Assigned', u32), ('Count', u32), ('Pids', size*16)]
    class FileTime(c.Structure): _fields_ = [('Low', u32), ('High', u32)]
    def bind(name, args, result):
        f = getattr(k, name); f.argtypes = args; f.restype = result; return f
    create = bind('CreateJobObjectW', [h, c.c_wchar_p], h)
    setinfo = bind('SetInformationJobObject', [h, c.c_int, h, u32], c.c_int)
    query = bind('QueryInformationJobObject', [h, c.c_int, h, u32, h], c.c_int)
    assign = bind('AssignProcessToJobObject', [h, h], c.c_int)
    resume = bind('ResumeThread', [h], u32)
    terminate = bind('TerminateJobObject', [h, u32], c.c_int)
    close = bind('CloseHandle', [h], c.c_int)
    getpid = bind('GetProcessId', [h], u32)
    gettimes = bind('GetProcessTimes', [h, h, h, h, h], c.c_int)
    image = bind('QueryFullProcessImageNameW', [h, u32, c.c_wchar_p, c.POINTER(u32)], c.c_int)
    injob = bind('IsProcessInJob', [h, h, c.POINTER(c.c_int)], c.c_int)
    assert (c.sizeof(Basic), c.sizeof(Extended), c.sizeof(Accounting), Pids.Pids.offset, Basic.Flags.offset, Basic.ActiveLimit.offset, Accounting.Active.offset) == (64, 144, 48, 8, 16, 40, 40)
    job = create(None, None)
    assert job, 'CreateJobObject failed before child creation'
    process = thread = None
    assigned = False
    row = {'guard_status': 'FAIL', 'data_result': 'NOT_READ', 'scope': 'ORIGINAL_IDLE_EXPLICIT_FOUR_QA_BINDING_145_FRAME_SAMPLING', 'argv': config['argv'], 'inputs_before': before, 'launcher_sha256': sha(__file__), 'config_sha256': sha(CONFIG), 'proposal_sha256': sha(PROPOSAL), 'approval_receipt_sha256': sha(REVIEW), 'resource_samples': [], 'R5_whole_guard_status': 'FAIL_PRESERVED', 'retry_count': 0}
    started = time.monotonic()
    def terminal(): return _winapi.WaitForSingleObject(process, 0) == _winapi.WAIT_OBJECT_0
    def accounting():
        a = Accounting()
        if not query(job, 1, c.byref(a), c.sizeof(a), None): raise c.WinError()
        return {'active': a.Active, 'total': a.Processes, 'limit_terminated': a.Terminated, 'user_100ns': a.User, 'kernel_100ns': a.Kernel}
    def pids():
        a = Pids()
        if not query(job, 3, c.byref(a), c.sizeof(a), None): raise c.WinError()
        assert a.Count <= 16
        return list(a.Pids[:a.Count])
    def owned_times():
        ct, et, kt, ut = [FileTime() for _ in range(4)]
        if not gettimes(h(process), c.byref(ct), c.byref(et), c.byref(kt), c.byref(ut)): raise c.WinError()
        return {'creation_FILETIME': (ct.High << 32) | ct.Low, 'exit_FILETIME': (et.High << 32) | et.Low}
    try:
        limits = Extended(); limits.Basic.Flags = 0x2000|0x100|0x200|0x8|0x10
        limits.Basic.ActiveLimit = 1; limits.Basic.Affinity = 3
        limits.ProcessMem = limits.JobMem = 8*1024**3
        if not setinfo(job, 9, c.byref(limits), c.sizeof(limits)): raise c.WinError()
        rb = Extended()
        if not query(job, 9, c.byref(rb), c.sizeof(rb), None): raise c.WinError()
        row['native_job_limit_readback'] = {'flags': rb.Basic.Flags, 'active_process_limit': rb.Basic.ActiveLimit, 'affinity_mask': rb.Basic.Affinity, 'process_memory_bytes': rb.ProcessMem, 'job_memory_bytes': rb.JobMem}
        assert row['native_job_limit_readback'] == {'flags': limits.Basic.Flags, 'active_process_limit': 1, 'affinity_mask': 3, 'process_memory_bytes': 8*1024**3, 'job_memory_bytes': 8*1024**3}
        with (OUT/'fixed-capture.log').open('xb') as log:
            fd = msvcrt.get_osfhandle(log.fileno()); os.set_handle_inheritable(fd, True)
            si = subprocess.STARTUPINFO(); si.dwFlags = 0x100|1; si.wShowWindow = 0
            si.hStdOutput = si.hStdError = fd; si.hStdInput = 0
            try:
                process, thread, pid, tid = _winapi.CreateProcess(str(EXE), subprocess.list2cmdline(config['argv']), None, None, True, 12, None, str(OUT), si)
            finally: os.set_handle_inheritable(fd, False)
            assert getpid(h(process)) == pid
            row.update(pid=pid, thread_id=tid, guard_parent_pid=os.getpid(), native_process_handle=int(process), native_job_handle=int(job), **owned_times())
            if not assign(job, h(process)):
                error = c.get_last_error()
                _winapi.TerminateProcess(process, 87)
                raise c.WinError(error)
            assigned = True
            assert accounting()['active'] == 1 and pids() == [pid]
            row['assigned_suspended_before_resume'] = True
            assert resume(h(thread)) != 0xFFFFFFFF
            print(json.dumps({'event': 'OWNED_CHILD_RESUMED', 'pid': pid, 'creation_FILETIME': row['creation_FILETIME'], 'native_process_handle': int(process), 'native_job_handle': int(job), 'guard_parent_pid': os.getpid()}), flush=True)
            while True:
                sample = resources(); sample['elapsed_seconds'] = time.monotonic()-started
                row['resource_samples'].append(sample)
                sample['accounting'] = accounting(); sample['job_pids'] = pids()
                assert sample['accounting']['total'] == 1 and sample['accounting']['active'] <= 1 and sample['accounting']['limit_terminated'] == 0
                assert sample['job_pids'] in ([pid], []), 'unknown owned Job PID'
                sample['owned_handle_signaled_before_image'] = terminal()
                if sample['owned_handle_signaled_before_image']:
                    sample['classification'] = 'TERMINAL_OWNED_HANDLE'
                    break
                sample.update(owned_times())
                assert sample['creation_FILETIME'] == row['creation_FILETIME']
                buf = c.create_unicode_buffer(32768); length = u32(len(buf))
                image_ok = bool(image(h(process), 0, buf, c.byref(length)))
                sample['image_query_success'] = image_ok
                if image_ok: sample['executable'] = buf.value
                else: sample['image_error'] = c.get_last_error()
                sample['owned_handle_signaled_after_image'] = terminal()
                if sample['owned_handle_signaled_after_image']:
                    sample['classification'] = 'TERMINAL_DURING_IMAGE_QUERY_USE_OWNED_EXIT_CODE'
                    break
                # Exit FILETIME or a non-STILL_ACTIVE exit code is not a substitute
                # for authoritative handle signaling. R5 LIVE race remains FAIL.
                assert image_ok, 'missing executable image while owned handle genuinely LIVE'
                assert Path(buf.value).resolve() == EXE.resolve(), 'wrong LIVE executable'
                belongs = c.c_int()
                assert injob(h(process), job, c.byref(belongs)) and belongs.value
                sample['classification'] = 'LIVE_IMAGE_AND_OWNERSHIP_VERIFIED'
                assert resource_gate(sample), 'RESOURCE_FLOOR'
                assert time.monotonic()-started < 120, 'WATCHDOG_TIMEOUT'
                if _winapi.WaitForSingleObject(process, 25) == _winapi.WAIT_OBJECT_0: break
            assert terminal()
            row['terminal_owned_handle_exit_code'] = _winapi.GetExitCodeProcess(process)
            row['terminal_owned_times'] = owned_times()
            assert row['terminal_owned_handle_exit_code'] == 0, 'nonzero owned exit'
            drain_start = time.monotonic()
            while accounting()['active'] != 0 and time.monotonic()-drain_start < 3: time.sleep(0.025)
            row['terminal_job_accounting'] = accounting(); row['terminal_job_pids'] = pids()
            assert row['terminal_job_accounting']['active'] == 0 and row['terminal_job_pids'] == []
            assert row['terminal_job_accounting']['total'] == 1 and row['terminal_job_accounting']['limit_terminated'] == 0
            assert all(sha(p) == s for p, s in before.items())
            assert sha(EXE) == config['blender_sha256'] and sha(CONFIG) == row['config_sha256'] and sha(PROPOSAL) == row['proposal_sha256'] and sha(__file__) == row['launcher_sha256'] and sha(REVIEW) == row['approval_receipt_sha256']
            row['guard_status'] = 'PASS_OWNED_JOB_EXIT_ZERO_DRAINED'
    except Exception:
        row['error'] = traceback.format_exc()
    finally:
        # Each cleanup operation records independently; no failing assertion can
        # skip Job close or prevent the raw receipt from being written.
        cleanup_errors = []
        def safe(label, operation):
            try: row[label] = operation()
            except Exception: cleanup_errors.append({'operation': label, 'error': traceback.format_exc()})
        if process is not None:
            if assigned:
                safe('cleanup_terminate_owned_job_if_live', lambda: True if terminal() else bool(terminate(job, 90)))
            else: safe('cleanup_terminate_only_unassigned_created_process', lambda: _winapi.TerminateProcess(process, 87))
            safe('cleanup_owned_handle_signaled', lambda: _winapi.WaitForSingleObject(process, 3000) == _winapi.WAIT_OBJECT_0)
            if row.get('cleanup_owned_handle_signaled'):
                safe('cleanup_owned_handle_exit_code', lambda: _winapi.GetExitCodeProcess(process))
                safe('cleanup_owned_times', owned_times)
            if assigned:
                try:
                    drain_start = time.monotonic()
                    while accounting()['active'] != 0 and time.monotonic()-drain_start < 3: time.sleep(0.025)
                except Exception: cleanup_errors.append({'operation': 'cleanup_drain', 'error': traceback.format_exc()})
                safe('cleanup_job_accounting_before_close', accounting)
                safe('cleanup_job_pids_before_close', pids)
        safe('job_close_success', lambda: bool(close(job)))
        if process is not None:
            safe('owned_process_signaled_after_job_close', lambda: _winapi.WaitForSingleObject(process, 3000) == _winapi.WAIT_OBJECT_0)
            safe('owned_process_handle_close', lambda: _winapi.CloseHandle(process))
        if thread is not None: safe('owned_thread_handle_close', lambda: _winapi.CloseHandle(thread))
        if cleanup_errors or not row.get('cleanup_owned_handle_signaled') or row.get('cleanup_job_accounting_before_close', {}).get('active') != 0 or row.get('cleanup_job_pids_before_close') != [] or not row.get('job_close_success') or not row.get('owned_process_signaled_after_job_close'):
            row['guard_status'] = 'FAIL'
        row['cleanup_errors'] = cleanup_errors
        safe('inputs_after', lambda: {p: sha(p) for p in before})
        if row.get('inputs_after') != before: row['guard_status'] = 'FAIL'
        # Data availability is independent of whole guard, even on a LIVE race.
        result = OUT/'IDLE_SAMPLING_RESULT_R1.json'
        if result.exists():
            safe('data_manifest_sha256', lambda: sha(result))
            try:
                data = json.loads(result.read_bytes())
                row['data_result'] = data['status']
                row['data_files'] = [{'path': n, 'actual_sha256': sha(OUT/n)} for n in ['SCENE_SIGNATURE_BEFORE_AFTER.json','ADDON_ORIGIN_INVENTORY_BEFORE_R2.json','ADDON_ORIGIN_INVENTORY_AFTER_R2.json']]
                row['sampling_schema_validated_separately'] = (data['sample_count'] == 145 and data['original137bones'] is True and data['original78Actions'] is True and len(data['original13muted_bridges']) == 13 and data['original_scene_signature_differences'] == {})
                row['target_binding_and_playback_acceptance'] = 'EXPLICIT_PM_QA_BINDINGS; NOT_VISUAL_OR_PRODUCT_ACCEPTANCE'
            except Exception: row['data_result'] = 'UNREADABLE_OR_PARTIAL'; row['data_error'] = traceback.format_exc()
        row['partial_files_retained'] = [p.name for p in OUT.iterdir() if p.is_file()]
        row['wall_seconds'] = time.monotonic()-started
        with (OUT/'OWNED_JOB_RESULT_R1.json').open('x', encoding='utf8') as f: json.dump(row, f, indent=2)
        print(json.dumps({'guard_status': row['guard_status'], 'data_result': row['data_result'], 'pid': row.get('pid'), 'retry_count': 0}), flush=True)
    return row

if __name__ == '__main__':
    if sys.argv[1:] == ['--run-approved-fixed-capture']:
        report = run()
        if report['guard_status'] != 'PASS_OWNED_JOB_EXIT_ZERO_DRAINED': raise SystemExit(1)
    elif sys.argv[1:]: raise SystemExit('Only the fixed reviewed route is supported')
    else: print('DRY_DEFAULT_PREPARATION_ONLY_NO_PROCESS')
