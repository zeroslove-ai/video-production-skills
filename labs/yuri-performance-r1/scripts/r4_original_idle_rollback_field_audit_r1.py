"""File-only captured AnimData field versus frozen rollback inventory; no root-cause claim."""
from pathlib import Path
import ast,hashlib,json
LAB=Path(__file__).resolve().parent.parent
PRIVATE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-original-idle-sampling-r2/ORIGINAL_BINDING_KEY_INPUTS_PRIVATE_R1.json')
DEST=LAB/'evidence/o1-original-idle-sampling-result-r2/CAPTURED_ANIMDATA_ROLLBACK_FIELD_AUDIT_R1.json'
def main():
    assert not DEST.exists()
    source=(LAB/'scripts/r4_original_idle_sample_r2.py').read_text(encoding='utf8')
    assert "ad.action=r['original_action']" in source and "if r['original_action'] is not None:ad.action_slot=r['original_slot']" in source
    assigned={t.attr for node in ast.walk(ast.parse(source)) if isinstance(node,ast.Assign) for t in node.targets if isinstance(t,ast.Attribute) and isinstance(t.value,ast.Name) and t.value.id=='ad'}
    assert 'last_slot_identifier' not in assigned and 'action_slot_handle' not in assigned
    data=json.loads(PRIVATE.read_bytes());targets={'Character_Body_Head','Hair_Rig_R4','Meshy_Fitted_Rig','FaceControls_TEST_Jaw_Smile.001'}
    rows=[]
    for row in data['bindings']:
        if row['owner'] not in targets:continue
        fields=[]
        for name,value in row['animation_data'].items():
            obligation='NOT_EXPLICITLY_RESTORED; unchanged native state must be verified in raw final readback'
            if name=='action':obligation='EXPLICIT_ASSIGN_ORIGINAL'
            if name=='action_slot':obligation='RESTORED_ONLY_IF_ORIGINAL_ACTION_NONNULL; null branch has no explicit slot readback'
            if name=='action_slot_handle':obligation='IMPLICIT_ACTION_CLEAR_BEHAVIOR_ONLY; no explicit assignment or final raw readback'
            if name=='last_slot_identifier':obligation='CONCRETE_OMITTED_EXPLICIT_ROLLBACK; original empty; final raw value missing; cause UNPROVEN'
            fields.append({'field':name,'saved_value_sha256':hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest(),'rollback_obligation':obligation,'after_native_field_status':'NOT_RECORDED'})
        rows.append({'owner':row['owner'],'ID_type':row['type'],'fields':fields})
    assert len(rows)==4
    report={'status':'FILE_ONLY_ACTUAL_CAPTURED_FIELD_TO_FROZEN_CODE_COMPARISON','native_runs':0,'original_capture_sha256':hashlib.sha256(PRIVATE.read_bytes()).hexdigest(),'frozen_collector_sha256':hashlib.sha256(source.encode()).hexdigest(),'rows':rows,'scope':'Four actual AnimData owners including original Key; full raw props/custom/anim before/ON/after required in R3. Key AnimData contributes to owner mesh_attributes fingerprint. No category omission/epsilon waiver.','root_cause':'UNPROVEN; no final raw fields captured, hashes cannot isolate the exact field'}
    with DEST.open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({'owners':len(rows),'status':report['status']}))
if __name__=='__main__':main()
