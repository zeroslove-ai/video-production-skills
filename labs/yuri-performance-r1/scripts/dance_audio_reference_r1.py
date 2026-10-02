"""Reference-only audio motif candidates; no extraction beyond first phrase."""
from pathlib import Path
import subprocess,shutil,json
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft,find_peaks
R=Path(__file__).resolve().parents[1];L=R/'local/dance-benchmark-r1';E=R/'evidence/dance-benchmark-r1';wav=L/'reference/audio_analysis.wav'
subprocess.run([shutil.which('ffmpeg'),'-y','-i',str(L/'reference/reference.mp4'),'-vn','-ac','1','-ar','22050',str(wav)],capture_output=True,check=True);sr,a=wavfile.read(wav);a=a.astype(float)/32768;f,t,z=stft(a,fs=sr,nperseg=2048,noverlap=1536);power=np.abs(z)**2;chroma=np.zeros((12,len(t)));valid=(f>80)&(f<2500);midi=np.round(69+12*np.log2(f[valid]/440)).astype(int)
for pitch in range(12):chroma[pitch]=power[valid][midi%12==pitch].sum(0)
chroma=np.log1p(chroma*1e4);chroma/=np.maximum(np.linalg.norm(chroma,axis=0),1e-8);times=np.arange(0,len(a)/sr,.1);features=np.array([np.interp(times,t,c) for c in chroma]).T;ref=features[200:260];scores=[]
for k in range(len(features)-60):
    if 10<k/10<36:continue
    score=float(np.mean(np.sum(ref*features[k:k+60],axis=1)));scores.append([k/10,score])
selected=[]
for start,score in sorted(scores,key=lambda x:x[1],reverse=True):
    if all(abs(start-p['start_seconds'])>=7 for p in selected):selected.append({'start_seconds':start,'end_seconds':start+6,'chroma_similarity':score})
    if len(selected)==8:break
flux=np.maximum(np.diff(np.log1p(power.sum(0)*1e5)),0);peaks,_=find_peaks(flux,distance=8,prominence=.15);onsets=t[1:][peaks];d={'method':'12 pitch-class STFT chroma, 100ms sampling, six-second template20–26s; pitch-class similarity may match generic harmony and is only a candidate locator','template':[20,26],'repeated_audio_candidates':selected,'chorus_label':'UNVERIFIED; musical similarity is not a chorus annotation','selected_segment_audio_onsets_seconds':onsets[(onsets>=20)&(onsets<26)].tolist(),'onset_scope':'signal transients, not manually labelled dance beats'};(E/'audio_reference_analysis.json').write_text(json.dumps(d,indent=2));print(json.dumps(d))
