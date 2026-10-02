"""Installed Comfy execution.validate_prompt only; no queue or execution engine.
Model loader functions deliberately raise if reached. Never load weights/infer.
Run with existing embedded Python. Owned dirs, CPU device, API/custom nodes disabled.
"""
from pathlib import Path
import sys,os,json,asyncio,shutil
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/comfy-video-r3'
INSTALL=Path(r'C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI')
os.environ.update(CUDA_VISIBLE_DEVICES='-1',HIP_VISIBLE_DEVICES='-1',OMP_NUM_THREADS='4',MKL_NUM_THREADS='4')
sys.path.insert(0,str(INSTALL));os.chdir(INSTALL)
from comfy.cli_args import args
args.cpu=True;args.disable_all_custom_nodes=True;args.disable_api_nodes=True
import folder_paths
local=ROOT/'local/wan-validation-r3'
for kind in ('input','output','temp','user'):(local/kind).mkdir(parents=True,exist_ok=True)
folder_paths.set_input_directory(str(local/'input'));folder_paths.set_output_directory(str(local/'output'));folder_paths.set_temp_directory(str(local/'temp'));folder_paths.set_user_directory(str(local/'user'))
shutil.copy2(ROOT/'local/acting-r2/greeting_wave/natural/hand_face/0001.png',local/'input/acting_first.png')
import nodes,execution
model_calls=[]
def forbidden_model_load(*a,**kw):model_calls.append('UNEXPECTED_MODEL_LOAD');raise AssertionError('Validation must not load models')
async def main():
    await nodes.init_extra_nodes(init_custom_nodes=False,init_api_nodes=False)
    for name in ('UNETLoader','CLIPLoader','VAELoader'):
        cls=nodes.NODE_CLASS_MAPPINGS[name];setattr(cls,cls.FUNCTION,forbidden_model_load)
    records=[]
    for name in ('A_t2v','B_first_frame'):
        path=ROOT/('workflows/acting-r2/'+name+'.json');graph=json.loads(path.read_text())
        result=await execution.validate_prompt('validation-only-'+name,graph,None)
        records.append({'graph':str(path),'validation_tuple':result,'result':'BACKEND_VALIDATION_PASS_NO_EXECUTION' if result[0] else 'FAIL'})
    receipt={'method':'Installed execution.validate_prompt() called directly; no HTTP /prompt, no PromptExecutor, no queue','cpu':args.cpu,'custom_nodes':False,'api_nodes':False,'model_loader_calls':model_calls,'model_inference_jobs':0,'records':records,'video_quality':'UNTESTED; PRODUCT_EXCLUSIVE lease unchanged'}
    (E/'wan_backend_validation.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt));assert not model_calls and all(r['result']=='BACKEND_VALIDATION_PASS_NO_EXECUTION' for r in records)
asyncio.run(main())
