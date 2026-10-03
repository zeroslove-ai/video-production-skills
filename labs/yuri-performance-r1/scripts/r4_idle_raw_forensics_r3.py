"""Exact original Object/mesh/Key fingerprint inputs; private raw phase evidence."""
import gzip,json,traceback
import bpy
from r4_appearance_signature import props,custom,anim,attribute_hash,val,digest

def object_payload(o):
    return {'props':props(o),'custom':custom(o),'anim':anim(o),
        'modifiers':[[m.name,props(m),custom(m)] for m in o.modifiers],
        'constraints':[[c.name,props(c)] for c in o.constraints],
        'materials':[[p.name,props(p)] for p in o.material_slots],
        'groups':[[g.name,g.index,g.lock_weight] for g in o.vertex_groups],
        'pose':[[b.name,props(b),custom(b),[[c.name,props(c)] for c in b.constraints]] for b in o.pose.bones] if o.type=='ARMATURE' else None}

def mesh_payload(m):
    return {'props':props(m),
        'vertices':[[*v.co,*v.normal,v.hide,v.select] for v in m.vertices],
        'edges':[[*e.vertices,e.use_edge_sharp,e.use_seam] for e in m.edges],
        'polygons':[[*p.vertices,p.material_index,p.use_smooth] for p in m.polygons],
        'attributes':[[a.name,a.data_type,a.domain,attribute_hash(a)] for a in m.attributes],
        'keys':{'props':props(m.shape_keys),'anim':anim(m.shape_keys),'blocks':[[k.name,props(k)] for k in m.shape_keys.key_blocks]} if m.shape_keys else None}

def schema(o):return [{'field':p.identifier,'type':p.type,'is_readonly':p.is_readonly} for p in o.bl_rna.properties]

def ui(o):
    result={}
    for k in o.keys():
        if k=='_RNA_UI':continue
        try:result[k]={'metadata':val(o.id_properties_ui(k).as_dict()),'status':'CAPTURED_NO_UNIT_INFERENCE'}
        except (TypeError,ValueError,KeyError) as e:result[k]={'status':'UNKNOWN_UI_METADATA','error':repr(e)}
    return result

def capture(phase,expected,out):
    raw={'objects':{o.name:object_payload(o) for o in bpy.data.objects},
         'mesh_attributes':{m.name:mesh_payload(m) for m in bpy.data.meshes},
         'Keys':{k.name:{'props':props(k),'custom':custom(k),'anim':anim(k),'blocks':[[b.name,props(b),custom(b)] for b in k.key_blocks]} for k in bpy.data.shape_keys},
         'owner_UI_and_RNA_schema':{o.name:{'type':o.bl_rna.identifier,'UI':ui(o),'schema':schema(o),'AnimData_schema':schema(o.animation_data) if o.animation_data else None} for o in list(bpy.data.objects)+list(bpy.data.shape_keys)}}
    hashes={category:{name:digest(payload) for name,payload in raw[category].items()} for category in ['objects','mesh_attributes']}
    match={c:hashes[c]==expected[c] for c in hashes}
    with gzip.open(out/f'RAW_FINGERPRINT_INPUTS_{phase}_PRIVATE_R3.json.gz','xb',compresslevel=1) as f:f.write(json.dumps(raw,separators=(',',':')).encode())
    with (out/f'RAW_RECOMPUTED_HASHES_{phase}_R3.json').open('x',encoding='utf8') as f:json.dump({'hashes':hashes,'exact_original_signature_matches':match},f,indent=2)
    assert all(match.values()),('Exact raw serializer mismatch',phase,match)

def raw_diff(out):
    with gzip.open(out/'RAW_FINGERPRINT_INPUTS_BEFORE_PRIVATE_R3.json.gz','rt') as f:before=json.load(f)
    with gzip.open(out/'RAW_FINGERPRINT_INPUTS_AFTER_PRIVATE_R3.json.gz','rt') as f:after=json.load(f)
    changes=[]
    def visit(a,b,path):
        if type(a) is not type(b):changes.append({'path':path,'before':a,'after':b});return
        if isinstance(a,dict):
            for key in sorted(set(a)|set(b)):
                if key not in a or key not in b:changes.append({'path':path+[key],'before':a.get(key),'after':b.get(key),'missing_key':True})
                else:visit(a[key],b[key],path+[key])
        elif isinstance(a,list):
            if len(a)!=len(b):changes.append({'path':path,'before':a,'after':b,'length_mismatch':True})
            else:
                for i,(x,y) in enumerate(zip(a,b)):visit(x,y,path+[i])
        elif a!=b:changes.append({'path':path,'before':a,'after':b})
    visit(before,after,[])
    with gzip.open(out/'RAW_FIELD_DIFF_PRIVATE_R3.json.gz','xb',compresslevel=1) as f:f.write(json.dumps(changes,separators=(',',':')).encode())
    with (out/'RAW_FIELD_DIFF_PATHS_R3.json').open('x',encoding='utf8') as f:json.dump({'difference_count':len(changes),'paths':[r['path'] for r in changes],'no_field_exclusions_epsilon_or_cosmetic_waiver':True},f,indent=2)
    return changes

def save_ad(ad):
    if ad is None:return None
    # Values remain native references for Action/slot; arrays copied, no invented IDs.
    saved={}
    for field in props(ad):
        value=getattr(ad,field)
        saved[field]=tuple(value) if hasattr(value,'__len__') and not isinstance(value,(str,bpy.types.bpy_struct)) else value
    return saved

def restore_ad(target,saved,ledger):
    if saved is None:
        target.animation_data_clear();ledger.append({'owner':target.name,'operation':'RESTORE_ORIGINAL_NO_ANIMDATA','readback_none':target.animation_data is None});return
    ad=target.animation_data
    if ad is None:
        ledger.append({'owner':target.name,'error':'EXISTING_ANIMDATA_MISSING; no rebuild permitted'});return
    # Binding first, original no-action slot metadata explicitly after binding.
    ordered=['action','action_slot','action_slot_handle','last_slot_identifier']+[k for k in saved if k not in {'action','action_slot','action_slot_handle','last_slot_identifier'}]
    for field in ordered:
        if field not in saved:continue
        entry={'owner':target.name,'field':field,'saved':val(saved[field])}
        try:
            prop=ad.bl_rna.properties[field];entry['is_readonly']=prop.is_readonly
            current=getattr(ad,field)
            if val(current)!=val(saved[field]):
                if prop.is_readonly:entry['error']='READ_ONLY_MISMATCH_NOT_WAIVED'
                else:setattr(ad,field,saved[field]);entry['assignment']='RESTORED_EXACT_NATIVE_VALUE'
            else:entry['assignment']='ALREADY_EXACT'
            entry['readback']=val(getattr(ad,field));entry['exact']=entry['readback']==entry['saved']
        except BaseException:entry['error']=traceback.format_exc();entry['exact']=False
        ledger.append(entry)

def restore_all(resolved,object_state,pose_state,key_state,saved_frame,restore_channels,out):
    ledger=[]
    def attempt(owner,operation,fn):
        try:fn();ledger.append({'owner':owner,'operation':operation,'success':True})
        except BaseException:ledger.append({'owner':owner,'operation':operation,'error':traceback.format_exc()})
    for r in resolved:
        restore_ad(r['target'],r['original_ad_fields'],ledger)
        for path,index,value in r['touched']:
            if path.startswith('["'):
                attempt(r['target'].name,path,lambda t=r['target'],k=path[2:-2],v=value:t.__setitem__(k,v))
    for o,state in object_state:attempt(o.name,'OBJECT_TRANSFORM_CHANNELS',lambda o=o,s=state:restore_channels(o,s))
    for b,state in pose_state:attempt(b.name,'POSE_TRANSFORM_CHANNELS',lambda b=b,s=state:restore_channels(b,s))
    for k,value in key_state:attempt(k.name,'KEY_VALUE',lambda k=k,v=value:setattr(k,'value',v))
    attempt('Scene','FRAME_AND_DEPGRAPH',lambda:bpy.context.scene.frame_set(saved_frame[0],subframe=saved_frame[1]))
    attempt('ViewLayer','UPDATE',lambda:bpy.context.view_layer.update())
    # Final readback after frame evaluation; readonly and unmodified fields still must be exact.
    for r in resolved:
        saved=r['original_ad_fields'];ad=r['target'].animation_data
        if saved is not None and ad is not None:
            for field,value in saved.items():
                try:ledger.append({'owner':r['target'].name,'field':field,'operation':'POST_FRAME_READBACK','exact':val(getattr(ad,field))==val(value),'saved':val(value),'actual':val(getattr(ad,field))})
                except BaseException:ledger.append({'owner':r['target'].name,'field':field,'error':traceback.format_exc()})
    with (out/'RESTORATION_LEDGER_PRIVATE_R3.json').open('x',encoding='utf8') as f:json.dump(ledger,f,indent=2)
    return ledger
