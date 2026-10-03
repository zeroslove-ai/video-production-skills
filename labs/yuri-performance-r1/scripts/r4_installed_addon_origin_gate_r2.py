"""Read-only origin/installed-file gate; never import/enable/disable addon modules."""
import hashlib, json, sys
from pathlib import Path

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def inspect_and_require(bpy, manifest_path, output_directory, phase):
    manifest=json.loads(Path(manifest_path).read_bytes())
    preferences=sorted(bpy.context.preferences.addons.keys())
    # Hidden core addons aren't necessarily in preferences. Do not import a
    # missing module to discover it; inspect only the already loaded snapshot.
    loaded=dict(sys.modules)
    flagged=sorted(n for n,m in loaded.items() if m is not None and getattr(m,'__addon_enabled__',False) is True)
    names=sorted(set(preferences)|set(flagged))
    records=[];errors=[]
    expected=manifest['installed_bundled_allowlist']
    for name in names:
        mod=loaded.get(name)
        raw=getattr(mod,'__file__',None) if mod is not None else None
        spec_origin=getattr(getattr(mod,'__spec__',None),'origin',None) if mod is not None else None
        row={'module':name,'in_preferences':name in preferences,'already_loaded':mod is not None,'enabled_flag':getattr(mod,'__addon_enabled__',None) is True,'origin':raw,'spec_origin':spec_origin,'classification':'UNAPPROVED_OR_UNKNOWN'}
        try:
            if raw:
                p=Path(raw).resolve();row['resolved_origin']=str(p)
                if p.is_file():row['origin_sha256']=sha(p)
            if name in expected and mod is not None:
                allowed=expected[name]
                origin=Path(allowed['entry_path']).resolve()
                assert raw and Path(raw).resolve()==origin
                assert spec_origin and Path(spec_origin).resolve()==origin
                assert row['origin_sha256']==allowed['entry_sha256'] and row['enabled_flag']
                row['classification']='PINNED_INSTALLED_BUNDLED_MODULE'
            else:errors.append({'module':name,'reason':'not in exact installed-bundle allowlist or module not loaded'})
        except Exception as error:errors.append({'module':name,'reason':repr(error)})
        records.append(row)
    checked=0
    for name, package in expected.items():
        for p,digest in package['python_files'].items():
            try:
                assert sha(Path(p))==digest, 'installed Python source hash drift'
                checked+=1
            except Exception as error:errors.append({'module':name,'file':p,'reason':repr(error)})
    for p,digest in manifest['startup_control_files'].items():
        try:assert sha(Path(p))==digest
        except Exception as error:errors.append({'file':p,'reason':repr(error)})
    if not bpy.app.factory_startup:errors.append({'reason':'bpy.app.factory_startup is false'})
    result={'phase':phase,'status':'PASS_PINNED_INSTALLED_ORIGINS_ONLY' if not errors else 'FAIL_UNKNOWN_OR_EXTERNAL_OR_DRIFT','factory_startup':bool(bpy.app.factory_startup),'preferences_module_names':preferences,'loaded_enabled_module_names':flagged,'modules':records,'installed_python_files_checked':checked,'errors':errors,'factory_enabled_defaults_exact_membership':'UNKNOWN_NOT_CAPTURED_IN_PRIOR_RUN; this is installed-origin trust, not default-membership assertion','network_side_effects':'NOT_MEASURED; post-startup inspection does not undo startup or establish packet isolation'}
    target=Path(output_directory)/f'ADDON_ORIGIN_INVENTORY_{phase.upper()}_R2.json'
    with target.open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps({'event':'READONLY_ADDON_ORIGIN_INVENTORY','phase':phase,'status':result['status'],'preferences':preferences,'enabled':flagged}),flush=True)
    assert not errors, 'Unapproved/unknown addon origin or installed hash drift; inventory retained'
    return result
