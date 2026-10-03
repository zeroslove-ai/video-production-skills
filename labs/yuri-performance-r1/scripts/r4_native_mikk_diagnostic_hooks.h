// Diagnostic observer only. Does not change Mikk state or output.
#pragma once
#include <cstdio>
#include <set>
#include <utility>
namespace diag {
inline FILE* stream=nullptr;
inline std::set<std::pair<unsigned,unsigned>> targets;
inline std::set<unsigned> groups;
inline bool wantFace(unsigned f) { for(auto p:targets) if(p.first==f)return true;return false; }
inline bool want(unsigned f,unsigned j) { return targets.count({f,j})!=0; }
template<class V> void vec(const char* n,V v) {
 fprintf(stream,"\"%s\":[%.9g,%.9g,%.9g]",n,double(v.x),double(v.y),double(v.z));
}
template<class V> void init(unsigned face,bool any,bool orient,float area,V os,V ot,V tangent) {
 if(!wantFace(face))return;
 fprintf(stream,"{\"event\":\"init\",\"face\":%u,\"groupWithAny\":%s,\"orientation\":%s,\"signed_UV_area\":%.9g,",face,any?"true":"false",orient?"true":"false",double(area));
 vec("vOs",os);fprintf(stream,",");vec("vOt",ot);fprintf(stream,",");vec("triangle_tangent",tangent);fprintf(stream,"}\n");
}
template<class V> void assign(unsigned face,unsigned corner,unsigned group,bool any,bool deg,V tangent) {
 if(!want(face,corner))return;
 if(group!=0xffffffffu)groups.insert(group);
 fprintf(stream,"{\"event\":\"assign\",\"face\":%u,\"corner\":%u,\"group\":%u,\"groupWithAny\":%s,\"markDegenerate\":%s,",face,corner,group,any?"true":"false",deg?"true":"false");
 vec("triangle_tangent",tangent);fprintf(stream,"}\n");
}
template<class V> void contribution(unsigned face,unsigned corner,unsigned group,float cos,float angle,V normal,V raw,V projection,V unnormalized_projection,V value,V sum) {
 if(!groups.count(group))return;
 fprintf(stream,"{\"event\":\"contribution\",\"face\":%u,\"corner\":%u,\"group\":%u,\"fCos\":%.9g,\"fast_acos_angle\":%.9g,",face,corner,group,double(cos),double(angle));
 vec("normal",normal);fprintf(stream,",");vec("triangle_tangent",raw);fprintf(stream,",");vec("projected_tangent",projection);fprintf(stream,",");vec("unnormalized_projection",unnormalized_projection);fprintf(stream,",");vec("contribution",value);fprintf(stream,",");vec("sum_before",sum);fprintf(stream,"}\n");
}
template<class V> void group(const char* phase,unsigned g,V value) {
 if(!groups.count(g))return;
 fprintf(stream,"{\"event\":\"%s\",\"group\":%u,",phase,g);vec("tangent",value);fprintf(stream,"}\n");
}
}
extern "C" __declspec(dllexport) int begin_trace(const char* path,const unsigned* pairs,int n) {
 if(diag::stream)fclose(diag::stream);
 diag::groups.clear();diag::targets.clear();
 for(int i=0;i<n;i++)diag::targets.insert({pairs[i*2],pairs[i*2+1]});
 diag::stream=fopen(path,"wb");return diag::stream?0:1;
}
extern "C" __declspec(dllexport) void end_trace() {
 if(diag::stream){fclose(diag::stream);diag::stream=nullptr;}
}
