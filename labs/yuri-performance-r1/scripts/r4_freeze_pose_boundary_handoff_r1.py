"""File-only receipt/hash binding and small metadata handoff, no native replay."""
from pathlib import Path
import hashlib,json,zipfile
LAB=Path(__file__).resolve().parent.parent
E=LAB/'evidence/o1-source-pose-matrix-input-boundary-r1'
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    analysis=json.loads((E/'SOURCE_POSE_MATRIX_BOUNDARY_ANALYSIS_R1.json').read_bytes())
    raw=json.loads((BASE/'o1-raw-pose-driver-stage-reference-r1/RAW_POSE_DRIVER_STAGE_MANIFEST.json').read_bytes())
    names=analysis['rows'][0]['bone_names']
    assert names==raw['original_body_bone_order']
    recipe_path=str(BASE/'o1-native-armature-full-recipe-custody-r1/SourceBodyArmatureInput_0cd0bdd7_EXACT.json')
    assert analysis['inputs'][recipe_path]['sha256']=='0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0'
    assert all(sha(Path(p))==row['sha256'] for p,row in analysis['inputs'].items())
    sources=[E/'SOURCE_POSE_MATRIX_BOUNDARY_ANALYSIS_R1.json',E/'LAPTOP_EXISTING_INPUT_AB_CONTRACT_R1.json',E/'SOURCE_POSE_MATRIX_BOUNDARY_HANDOFF_R1.md',LAB/'scripts/r4_source_pose_matrix_boundary_analysis_r1.py',Path(__file__)]
    packet=E/'YURI_O1_SOURCE_POSE_MATRIX_BOUNDARY_HANDOFF_R1.zip'
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        for p in sources:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        for p in sources:assert hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
    value={'status':'FILE_ONLY_SOURCE_INPUT_BOUNDARY_METADATA_NO_NEW_CAPTURE','packet':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'input_hashes_and_original57_raw_order_checked':True,'zip_CRC_and_all_member_SHA_verified':True,'raw_numeric_pose_geometry_recipe_in_packet':False,'native_receiver_packet41802754_resent':False,'Laptop_actual_native_custody_SHA':'41798f214f1b5a67c78765c42e9d82d3763157e85da0dca9c81964db10cdbedf','first_cause':'NOT_ISOLATED','members':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sources}}
    with (E/'PACKET_CUSTODY_R1.json').open('x',encoding='utf8') as f:json.dump(value,f,indent=2)
    print(json.dumps({'packet_bytes':value['bytes'],'packet_sha256':value['sha256'],'status':value['status']}))

if __name__=='__main__':main()
