"""Latest research receipt: evidence counts, never planned=completed."""
from pathlib import Path
import json,hashlib,time,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'local/acting-r2';E=ROOT/'evidence/acting-r2'
candidate=OUT/'YURI_PERFORMANCE_ACTING_R2.blend'
render=json.loads((E/'render_jobs.json').read_text())
delivery=json.loads((E/'video_delivery.json').read_text())
receipt={'run_id':'yuri-performance-r1-acting-r2-20261002','time_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
 'workspace':str(ROOT.parents[1]),'branch':'research/yuri-performance-previs-r1-20261002','source_revision':'f5752b7',
 'previous_run_receipt':str(E/'previous_latest_run_r1.json'),'latest_run_directory':str(OUT),
 'blender_file':str(candidate),'candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),
 'review_html':str(OUT/'REVIEW_ACTING_R2.html'),'result':'DESKTOP_RESEARCH_IN_PROGRESS',
 'semantic_base_recipes':3,'approved_actual_yuri_performances':0,'planned_catalog_count':48,
 'derived_render_jobs_done':sum(v['returncode']==0 for v in render['jobs'].values()),'derived_render_jobs_planned':19,
 'encoded_derived_reference_videos':len(delivery['videos']),'these_are_not_completed_yuri_motion_count':True,
 'gpu_lease':'PRODUCT_EXCLUSIVE_UNCHANGED','model_video_inference_jobs':0,'paid_provider_jobs':0,
 'product_repos_changed':False,'main_merged':False,'laptop_work_changed':False,
 'next_bounded_task':'Review same acting scores in five cameras and head-follow/head-amplitude AB at 1x, improve weakest beat only.',
 'research_horizon':'User requested approximately 4–8 hours; active goal, not declared complete at this checkpoint.'}
native=ROOT/'evidence/native-body-r3/build_receipt.json'
if native.exists():
    n=json.loads(native.read_text());q=json.loads((native.parent/'structural_qa.json').read_text())
    receipt['native_body_reference']={'candidate':n['candidate'],'sha256':n['candidate_sha256'],'source_actions_preserved':66,'recipes':3,'face':'NEUTRAL ONLY','structural_gate':[{'clip':c['clip'],'technical':c['technical']} for c in q['clips']],'visual_gate':'CONTACT_REVIEW_IN_PROGRESS; please hand readability weak','actual_yuri_approved_performances':0}
if (ROOT/'evidence/source-face-r2/mouth_measurement.json').exists():receipt['source_face_gate']='PARTIAL: neutral/blink/gaze response confirmed; FAIL_A_O_READABILITY; elaborate target facial recipes withheld'
receipt['offline_video_AB_plan']=str(E/'video_AB_plan.json') if (E/'video_AB_plan.json').exists() else None
receipt['pipeline_checkpoint_document']=str(ROOT/'R3_PIPELINE_CHECKPOINT_KO.md')
receipt['completed_evidence_by_candidate']={}
for folder in ('acting-r3-blink','native-body-r3','native-body-r3-please-hands','native-body-r3-please-elbow','native-camera-r4','face-mix-r4','comparison-r3'):
    e=ROOT/'evidence'/folder;d=e/'video_delivery.json' if folder!='comparison-r3' else e/'delivery.json'
    b=e/'build_receipt.json';m=json.loads(b.read_text()) if b.exists() else {}
    receipt['completed_evidence_by_candidate'][folder]={'candidate_sha256':m.get('candidate_sha256',m.get('sha256')),'encoded_reference_videos':len(json.loads(d.read_text()).get('videos',[])) if d.exists() else 0,'actual_yuri_approved':0}
receipt['native_body_reference']['visual_gate']='RESEARCH_REFERENCE: greeting/shy playback; please hand strategy improved; wrist ingress/recovery defects remain; selected camera R4 underway'
receipt['comfy_video_roundtrip']='CPU_CORE_PASS; 24fps/5s/120frames; SSIM .993819; no models loaded'
receipt['wan_backend_graph_validation']='T2V_AND_FIRST_FRAME_PASS; execution/model benefit UNTESTED'
receipt['next_bounded_task']='Complete selected native five-camera CPU references and independent proxy face/gaze composition proof, then score normal-speed playback and package reproducible recipes.'
encoded=json.dumps(receipt,indent=2,ensure_ascii=False)+'\n'
temporary=ROOT/'LATEST_RUN.json.tmp';temporary.write_text(encoded,encoding='utf-8')
json.loads(temporary.read_text(encoding='utf-8'));temporary.replace(ROOT/'LATEST_RUN.json')
print(json.dumps(receipt,indent=2,ensure_ascii=True))
