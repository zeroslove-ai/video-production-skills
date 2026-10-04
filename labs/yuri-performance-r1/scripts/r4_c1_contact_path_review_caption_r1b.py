"""Correct a copied review caption without replacing movies, candidates or R1 HTML."""
from pathlib import Path
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');D=B/'alpha-c1-contact-path-delivery-r1';s=(D/'REVIEW_C1_LEFT_ARM_CONTACT_R1.html').read_text(encoding='utf-8');s=s.replace('<title>R4 finger-only source QA</title>','<title>C1 left arm contact source QA</title>').replace('close camera follows C1 wrist only','close camera follows derivative C1 wrist only').replace('return reaches C1 baseline only','return reaches the derivative start pose; left-arm endpoint differs from old C1 and is not original R4 neutral');s+='<h2>Matched same-camera controls</h2>'
for view in ['hand_close','front','side','fullbody']:s+=f'<p>{view}: top original C1+R2 fingers / bottom single upper-arm clearance derivative+same R2 fingers</p><img src="SAME_CAMERA_BEFORE_AFTER_{view}_R1.jpg">'
p=D/'REVIEW_C1_LEFT_ARM_CONTACT_R1B.html'
with p.open('x',encoding='utf-8') as f:f.write(s)
print(p)
