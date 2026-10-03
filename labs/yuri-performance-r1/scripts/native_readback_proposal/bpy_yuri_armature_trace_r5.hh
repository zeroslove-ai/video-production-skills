/* GPL-2.0-or-later. Included by bpy_interface.cc only in owned debug builds. */
#pragma once
#ifdef WITH_YURI_ARMATURE_TRACE_R1
#include <Python.h>
#include "BLI_yuri_armature_trace_r1.hh"
namespace blender {
namespace yuri_armature_bridge_r5 {
inline std::atomic<bool> evaluating{false}, evaluated{false};
static PyObject *begin(PyObject *,PyObject *args) {
  int row;float frame;const char *action,*rig,*body,*source,*actions,*pose,*recipe,*request;
  if(!PyArg_ParseTuple(args,"isfsssssss:begin",&row,&action,&frame,&rig,&body,&source,&actions,&pose,&recipe,&request))return nullptr;
  if(evaluating || yuri_armature_trace_r1::requested.load()!=-1)Py_RETURN_FALSE;
  evaluated=false;
  if(yuri_armature_trace_r1::begin(row,action,frame,rig,body,source,actions,pose,recipe,request))Py_RETURN_TRUE;
  Py_RETURN_FALSE; // Native begin never retains stream/request ownership on false.
}
static PyObject *evaluate_and_join(PyObject *,PyObject *args) {
  int row;if(!PyArg_ParseTuple(args,"i:evaluate_and_join",&row))return nullptr;
  if(row<0 || row>1 || evaluating || evaluated || yuri_armature_trace_r1::requested.load()!=row) {
    PyErr_SetString(PyExc_RuntimeError,"unarmed, repeated or concurrent owned evaluation");return nullptr;
  }
  PyObject *main=PyImport_AddModule("__main__");if(!main)return nullptr;
  PyObject *globals=PyModule_GetDict(main); // Borrowed, Python owned process context.
  evaluating=true;
  // Fixed code calls actual RNA update synchronously; no user callback or async task.
  // Source RNA_view_layer_update -> BKE_scene_graph_update_tagged -> depsgraph
  // evaluation waits for worker completion before returning. Force complete
  // intended rig and ordinary mesh re-evaluation without changing Action/frame.
  PyObject *result=PyRun_String(
    "import bpy\n"
    "bpy.data.objects['Meshy_Fitted_Rig'].data.update_tag()\n"
    "bpy.data.objects['Meshy_Fitted_Rig'].update_tag(refresh={'OBJECT','DATA','TIME'})\n"
    "bpy.data.objects['Meshy_Body_NeutralCovered'].update_tag(refresh={'OBJECT','DATA'})\n"
    "bpy.context.view_layer.update()\n",Py_file_input,globals,globals);
  evaluating=false;
  if(!result)return nullptr; // The synchronous call returned; adapter can close safely.
  Py_DECREF(result);evaluated=true;Py_RETURN_TRUE;
}
static PyObject *cancel_and_join(PyObject *,PyObject *) {
  // No bridge-launched background work exists. GIL-held synchronous evaluation
  // must have returned/raised before Python finally can invoke this method.
  if(evaluating) {PyErr_SetString(PyExc_RuntimeError,"evaluation still active");return nullptr;}
  Py_RETURN_TRUE;
}
static PyObject *finish(PyObject *,PyObject *) {
  if(evaluating) {PyErr_SetString(PyExc_RuntimeError,"finish before synchronous worker join");return nullptr;}
  const bool closed=yuri_armature_trace_r1::finish();const bool complete=evaluated;
  evaluated=false;if(closed && complete)Py_RETURN_TRUE;Py_RETURN_FALSE;
}
static PyObject *build_info(PyObject *,PyObject *) {
#ifdef _MSC_VER
  const int msvc=_MSC_VER;
#else
  const int msvc=0;
#endif
  return Py_BuildValue("{s:s,s:s,s:i,s:s}","binding","YURI_ARMATURE_TRACE_R5",
    "pinned_source_commit","9e2066aef7ef7e20c142ad7bd3303138a4304c93",
    "MSVC_compat_version",msvc,"scope","owned default-OFF; per-TU flags/backend require external compiled custody");
}
inline PyMethodDef methods[]={
 {"begin",begin,METH_VARARGS,"Verified-input, atomic exclusive owned arming."},
 {"evaluate_and_join",evaluate_and_join,METH_VARARGS,"Fixed synchronous RNA evaluation, no async/user callback."},
 {"cancel_and_join",cancel_and_join,METH_NOARGS,"Confirm synchronous evaluation has returned."},
 {"finish",finish,METH_NOARGS,"Close only after returned evaluation; reject incomplete/failed output."},
 {"build_info",build_info,METH_NOARGS,"Source/binding marker; not installed compiler equivalence."},
 {nullptr,nullptr,0,nullptr}};
inline PyModuleDef module={PyModuleDef_HEAD_INIT,"_yuri_armature_trace_r5",nullptr,-1,methods,nullptr,nullptr,nullptr,nullptr};
} // namespace yuri_armature_bridge_r5
static PyObject *BPyInit_yuri_armature_trace_r5() {return PyModule_Create(&yuri_armature_bridge_r5::module);}
} // namespace blender
#endif
