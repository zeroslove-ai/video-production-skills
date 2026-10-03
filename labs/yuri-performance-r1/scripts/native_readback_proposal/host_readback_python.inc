/* Included inside ccl namespace in python.cpp, after guarded GLOBAL includes.
 * Uncompiled proposal. RNA type validation replaces stock PyLong/address parsing. */
static PyObject *host_guard_probe_func(PyObject *, PyObject *args)
{
  const char *name;
  if (!PyArg_ParseTuple(args,"s",&name)) return nullptr;
  if (!blender::G.background || !blender::BLI_thread_is_main()) {
    PyErr_SetString(PyExc_RuntimeError,"owned background main-thread guard test only");return nullptr;
  }
  try { host_readback::guard_probe(name); }
  catch (const std::exception &error) { PyErr_SetString(PyExc_RuntimeError,error.what());return nullptr; }
  PyErr_SetString(PyExc_RuntimeError,"guard probe returned");return nullptr;
}
static PyObject *host_readback_func(PyObject *, PyObject *args)
{
  PyObject *context_obj, *preferences_obj, *depsgraph_obj;
  const char *expected_path, *output_path, *audit_path;
  if (!PyArg_ParseTuple(args, "OOOsss", &context_obj, &preferences_obj, &depsgraph_obj,
                        &expected_path, &output_path, &audit_path)) return nullptr;
  const auto *context = blender::pyrna_struct_as_ptr(context_obj, &blender::RNA_Context);
  const auto *preferences = blender::pyrna_struct_as_ptr(preferences_obj, &blender::RNA_Preferences);
  const auto *depsgraph = blender::pyrna_struct_as_ptr(depsgraph_obj, &blender::RNA_Depsgraph);
  if (!context || !preferences || !depsgraph) return nullptr;
  if (!context->data || !preferences->data || !depsgraph->data) {
    PyErr_SetString(PyExc_RuntimeError,"expired native RNA context"); return nullptr;
  }
  auto *C=static_cast<blender::bContext *>(context->data);
  auto *main=blender::CTX_data_main(C);
  auto *scene=blender::CTX_data_scene(C);
  auto *graph=static_cast<blender::Depsgraph *>(depsgraph->data);
  const std::filesystem::path root("C:/YuriTransfer/native-cycles-readback-r1/capture");
  const std::filesystem::path out(output_path), audit_file(audit_path);
  if (!blender::G.background || !blender::BLI_thread_is_main() || !main || !scene || !graph ||
      out.lexically_normal().parent_path() != root ||
      audit_file.lexically_normal().parent_path() != root ||
      std::filesystem::exists(out) || std::filesystem::exists(audit_file)) {
    PyErr_SetString(PyExc_RuntimeError, "isolated background main-thread/new owned paths required");
    return nullptr;
  }
  /* RE_engine_create only allocates the native RenderEngine and initializes two
   * mutexes. No render callback, Session, engine depsgraph or GPU context owned. */
  blender::RenderEngineType type{};
  std::strcpy(type.idname,"YURI_HOST_READBACK_ONLY");
  std::strcpy(type.name,"Yuri Host Readback Only");
  type.flag=0;
  blender::RenderEngine *engine=blender::RE_engine_create(&type);
  FILE *audit=std::fopen(audit_path,"wx");
  if (!audit) {
    blender::RE_engine_free(engine);
    return PyErr_SetFromErrno(PyExc_OSError);
  }
  std::string error;
  const bool ok=host_readback::readback_host_strong6(*engine,
      *static_cast<blender::UserDef *>(preferences->data), *main, *scene, *graph,
      expected_path, output_path, audit, error);
  /* Driver returned only after Sync/Scene/Device/scheduler/Scope destructors. */
  blender::RE_engine_free(engine);
  std::fprintf(audit,"{\"native_driver_returned\":%s,\"native_engine_freed\":true}\n",ok?"true":"false");
  std::fflush(audit); std::fclose(audit);
  if (!ok) { PyErr_SetString(PyExc_RuntimeError,error.c_str());return nullptr; }
  Py_RETURN_TRUE; // External immutable hashes/process-exit proof required for acceptance.
}
