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
encoded=json.dumps(receipt,indent=2,ensure_ascii=False)+'\n'
temporary=ROOT/'LATEST_RUN.json.tmp';temporary.write_text(encoded,encoding='utf-8')
json.loads(temporary.read_text(encoding='utf-8'));temporary.replace(ROOT/'LATEST_RUN.json')
print(json.dumps(receipt,indent=2,ensure_ascii=True))
