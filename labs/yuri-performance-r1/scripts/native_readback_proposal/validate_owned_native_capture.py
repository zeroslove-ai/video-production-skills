"""External data validation proposal. Import/read only; never launches a process."""
from pathlib import Path
import hashlib,json
import numpy as np
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
EXPECTED=BASE/'o1-guarded-native-resource-sizing-r1/expected-Strong6-v3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(root):
    root=Path(root);output=root/'Strong6-native-host'
    pending=json.loads((root/'Strong6-pending-process-exit.json').read_text())
    assert pending['status']=='DATA_AND_NATIVE_CLEANUP_VALIDATED_PENDING_SUPERVISOR_EXIT0'
    assert pending['OFF_restore_exact'] is True and pending['source_temporal_settings_unchanged'] is True
    expected=json.loads((EXPECTED/'EXPECTED_INPUTS.json').read_text())
    for row in expected['files']:
        p=output/row['path']
        assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
    for row in pending['files']:
        p=output/row['path'];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
    metadata=json.loads((output/'ACTUAL_ATTRIBUTE_METADATA.json').read_text())
    attrs={r['standard_name']:r for r in metadata['attributes']}
    assert set(attrs)=={'P','N','uv','tangent','tangent_sign'}
    for key,stride,count in [('P',12,63561),('N',4,381120),('uv',8,381120),('tangent',12,381120),('tangent_sign',4,381120)]:
        assert attrs[key]['stride']==stride and attrs[key]['count']==count and attrs[key]['motion_steps']==1
        assert attrs[key]['buffer_bytes']==stride*count and attrs[key]['TypeDesc']
    slots=np.fromfile(output/'material_slots.i32',dtype='<i4')
    shaders=np.fromfile(output/'shader_ids.i32',dtype='<i4')
    smooth=np.fromfile(output/'registered_smooth.u8',dtype='u1')
    assert len(slots)==len(shaders)==len(smooth)==127040
    assert metadata['shader_slot_count']>0
    assert np.array_equal(shaders,np.clip(slots,0,metadata['shader_slot_count']-1))
    assert np.array_equal(smooth,np.fromfile(output/'smooth.u8',dtype='u1'))
    t=np.fromfile(output/'tangent.f32',dtype='<f4');s=np.fromfile(output/'sign.f32',dtype='<f4')
    assert len(t)==381120*3 and len(s)==381120 and np.isfinite(t).all() and np.isfinite(s).all()
    assert np.isin(s,[-1,1]).all()
    lengths=np.linalg.norm(t.reshape(-1,3).astype(np.float64),axis=1)
    nonzero=lengths[lengths>0]
    assert len(nonzero)>0 and abs(nonzero-1).max()<1e-5
    return {'classification':'ACTUAL_CUSTOM_HOST_CENTER_SNAPSHOT_ONLY','files_verified':len(pending['files']),
      'zero_tangent_count':int((lengths==0).sum()),'runtime_PBR':'HOLD','installed_renderer_equivalence':False}
