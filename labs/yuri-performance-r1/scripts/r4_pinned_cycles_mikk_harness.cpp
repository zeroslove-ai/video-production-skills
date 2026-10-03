// Research-only minimal buffer facade; no renderer-buffer claim.
// Original MikkMeshWrapper and Triangle::compute_normal are included verbatim.
#include <array>
#include <vector>
#include <atomic>
#include <cstdint>
#include <exception>
#define CCL_NAMESPACE_BEGIN namespace ccl {
#define CCL_NAMESPACE_END }
#include "util/types_normal.h"
using uint = unsigned int;
#include "mikktspace.hh"
using namespace ccl;
namespace mikk { using uint = unsigned int; }
namespace ccl {
struct Mesh {
 struct Triangle { int v[3]; float3 compute_normal(const packed_float3*) const; };
 std::vector<packed_float3> position;
 std::vector<int> triangles;
 std::vector<bool> smooth;
 const packed_float3* get_position() const { return position.data(); }
 int num_triangles() const { return int(triangles.size()/3); }
 const std::vector<int>& get_triangles() const { return triangles; }
 const std::vector<bool>& get_smooth() const { return smooth; }
 Triangle get_triangle(int i) const { return {{triangles[i*3],triangles[i*3+1],triangles[i*3+2]}}; }
};
#include "pinned_wrapper.inc"
// Explicit raw-float ablation only, not the canonical packed-normal wrapper.
struct RawNormalWrapper : MikkMeshWrapper {
 const float* raw;
 using MikkMeshWrapper::MikkMeshWrapper;
 mikk::float3 GetNormal(int f,int v) {
   if (!mesh->get_smooth()[f]) return MikkMeshWrapper::GetNormal(f,v);
   const float* n=raw+CornerIndex(f,v)*3;
   return mikk::float3(n[0],n[1],n[2]);
 }
};
}
extern "C" __declspec(dllexport) int compute_reference(
 int nv,int nc,int nt,const float* pos,const float* normals,const float* uv,
 const int* verts,const int* corners,const unsigned char* smooth,int raw_mode,
 uint32_t* packed_out,float* decoded_out,float* tangent_out,float* sign_out) {
 try {
   Mesh mesh;mesh.position.resize(nv);mesh.triangles.assign(verts,verts+nt*3);mesh.smooth.resize(nt);
   for(int i=0;i<nv;i++)mesh.position[i]=packed_float3(make_float3(pos[i*3],pos[i*3+1],pos[i*3+2]));
   for(int i=0;i<nt;i++)mesh.smooth[i]=smooth[i]!=0;
   std::vector<packed_normal> pn(nt*3);std::vector<float2> uvs(nt*3);
   std::vector<packed_float3> tan(nt*3);std::vector<float> raw(nt*9);
   for(int i=0;i<nt*3;i++) {
     int c=corners[i];if(c<0 || c>=nc)return 2;
     pn[i]=packed_normal(make_float3(normals[c*3],normals[c*3+1],normals[c*3+2]));
     float3 d=pn[i].decode();packed_out[i]=pn[i].value;
     decoded_out[i*3]=d.x;decoded_out[i*3+1]=d.y;decoded_out[i*3+2]=d.z;
     uvs[i]=make_float2(uv[c*2],uv[c*2+1]);
     for(int j=0;j<3;j++)raw[i*3+j]=normals[c*3+j];
   }
   if(raw_mode) {
     RawNormalWrapper w(&mesh,nullptr,pn.data(),uvs.data(),tan.data(),sign_out);w.raw=raw.data();
     mikk::Mikktspace(w).genTangSpace();
   } else {
     MikkMeshWrapper w(&mesh,nullptr,pn.data(),uvs.data(),tan.data(),sign_out);
     mikk::Mikktspace(w).genTangSpace();
   }
   for(int i=0;i<nt*3;i++){tangent_out[i*3]=tan[i].x;tangent_out[i*3+1]=tan[i].y;tangent_out[i*3+2]=tan[i].z;}
   return 0;
 } catch(const std::exception&) { return 3; }
}
