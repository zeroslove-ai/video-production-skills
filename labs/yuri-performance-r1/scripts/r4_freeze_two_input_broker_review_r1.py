"""Freeze NEW review assets and byte clone; NEVER launches Blender or helper."""
from pathlib import Path
import hashlib,json,shutil
LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
PREP=BASE/'o1-morph67-native-broker-preparation-r4'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def main():
    assert not PREP.exists();PREP.mkdir();wf=PREP/'workflow';wf.mkdir()
    scripts=['r4_two_input_owned_barrier_broker_r1.py','r4_two_input_live_barrier_wrapper_r1.py','r4_morph67_two_input_normal_collector_DRAFT_R1.py','r4_appearance_signature.py','native_preservation.py']
    for name in scripts:
        p=LAB/'scripts'/name;compile(p.read_text(),str(p),'exec');shutil.copyfile(p,wf/name)
    helper_cmd=wf/'r4_owned_barrier_helper_r2.cmd';shutil.copyfile(LAB/'scripts'/helper_cmd.name,helper_cmd)
    collector=LAB/'scripts'/scripts[2]
    assert sha(collector)=='68f9c54d892aad1ccae72c832d32e2203d6711d1024e64f6c2a50a6c73d89717'
    source=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
    assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
    clone=BASE/'o1-morph67-native-broker-preparation-r1/SOURCE_BYTE_CLONE_R4.blend';assert sha(source)==sha(clone)
    inputs=BASE/'o1-morph67-two-input-source-normal-proposal-r1';copies=PREP/'inputs';copies.mkdir()
    for tag,h in [('WORST','170accdfe80954ae2fe340e1aca3bdef5ac2e7fd25049be2089ab69766bd77a2'),('NEUTRAL','b775d6252cc4e9c3703d76e5747a7113bfb5d8318f1d1ff5e9b2b73df5d53961')]:
        p=inputs/(tag+'_source_inputs_PRIVATE_R1.json');assert sha(p)==h;shutil.copyfile(p,copies/p.name)
    exe=Path('C:/Program Files/Blender Foundation/Blender 5.2/blender.exe');py=Path('C:/Program Files/Python313/python.exe')
    assert sha(exe)=='284f4041f98e113f3dc10654a7193ffaaa9bfdfec8b87fa116620a48b5f6d4cb'
    assert sha(py)=='d87063e5597f257004c731b66c59c56c91038861c6877b1a3dca6b8c4e919125'
    wrapper=wf/scripts[1];broker=wf/scripts[0];cmd=Path('C:/Windows/System32/cmd.exe')
    hg=PREP/'helper-gates-r1';ng=PREP/'native-gates-r1';approval=PREP/'NEW_NATIVE_APPROVAL_R1.json'
    capture=BASE/'o1-morph67-two-input-native-compare-r1';assert not capture.exists()
    argv=['--clone',str(clone),'--inputs',str(inputs),'--out',str(capture),'--new-approval',str(approval),'--guard-before',str(ng/'guard-before.json')]
    payload=PREP/'NATIVE_PAYLOAD_CONFIG_R1.json';dump(payload,{'collector_argv':argv,'scope':'FACE16/GAZE2 -> source correctives; not consumer71 forced weights'})
    config={'schema':'TWO_INPUT_LIVE_BARRIER_BROKER_R1','native_authorized':False,
        'broker_sha256':sha(broker),'collector_sha256':sha(collector),
        'limits':{'wall_seconds':90,'memory_bytes':4*1024**3,'Blender_threads':2,'process_limit':1,'output_bytes':64*1024**2,'affinity_mask':3,'kill_on_close':True,'creation_flags':0x8000c},
        'helper':{'argv':[str(cmd),'/d','/q','/s','/c',str(helper_cmd),str(hg)],
                  'command_line':f'"{cmd}" /d /q /s /c ""{helper_cmd}" "{hg}""',
                  'gates':str(hg),'result_path':str(PREP/'HELPER_PREFLIGHT_RESULT_R1.json'),'executable_sha256':sha(cmd)},
        'native':{'argv':[str(exe),'--background','--factory-startup','--disable-autoexec','--threads','2','--python',str(wrapper),'--','--kind','native','--gates',str(ng),'--collector',str(collector),'--collector-config',str(payload)],
                  'gates':str(ng),'capture_output':str(capture),'approval_path':str(approval),'result_path':str(PREP/'NATIVE_GUARD_RESULT_R1.json'),'executable_sha256':sha(exe)}}
    pinned=[source,clone,exe,py,cmd,helper_cmd,payload,*[wf/name for name in scripts],collector,
            LAB/'scripts/r4_appearance_signature.py',LAB/'scripts/native_preservation.py',
            inputs/'WORST_source_inputs_PRIVATE_R1.json',inputs/'NEUTRAL_source_inputs_PRIVATE_R1.json',
            copies/'WORST_source_inputs_PRIVATE_R1.json',copies/'NEUTRAL_source_inputs_PRIVATE_R1.json',
            BASE/'o1-source-fidelity-recovery-r1/data/Character_Body_Head_original_mesh.npz']
    config['pinned_files']={str(p):sha(p) for p in pinned}
    cp=PREP/'FIXED_BROKER_CONFIG_R1.json';dump(cp,config)
    review={'task':'ROOT_PM_TWO_INPUT_NATIVE_BROKER_FREEZE_R1','scope':'BROKER_PREPARATION_AND_HELPER_ONLY',
        'native_authorized':False,'historical_sampler_approval_reused':False,
        'config':{'path':str(cp),'sha256':sha(cp)},'broker':{'path':str(broker),'sha256':sha(broker)},
        'collector':{'execution_path':str(collector),'frozen_copy':str(wf/scripts[2]),'sha256':sha(collector)},
        'source_clone':{'path':str(clone),'bytes':clone.stat().st_size,'sha256':sha(clone)},
        'payload_config':{'path':str(payload),'sha256':sha(payload)},'pinned_files':config['pinned_files'],
        'helper_command':[str(py),str(broker),'--config',str(cp),'--helper-preflight'],
        'native_command_after_NEW_review_only':[str(py),str(broker),'--config',str(cp),'--native','--new-approval',str(approval)],
        'native_child_argv':config['native']['argv'],'limits':config['limits'],
        'strict_after':'Live postpayload barrier BEFORE release/teardown; both original/limited handle QFPI must pass. Retained original handle verifies terminal exit, JobActive0/PIDs[] and log close. Error5 is never waived.'}
    dump(PREP/'BROKER_REVIEW_PACKET_METADATA_R1.json',review)
    print(json.dumps({'prepared':str(PREP),'broker_sha256':sha(broker),'config_sha256':sha(cp),'native_Blender_calls':0}))
if __name__=='__main__':main()
