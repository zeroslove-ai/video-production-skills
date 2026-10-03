# Preparation failures and corrections

No Blender/build/acquisition/probe was launched during these failures.

- Initial V3 Python code generation joined a non-raw string containing escaped newlines; AST compilation rejected an unterminated string before output. Changed the injected block to one raw string; generation passed.
- One PowerShell inline Python edit failed at PowerShell parsing. No target file was changed; used an explicit file patch for the caller's finally/schema correction.
- R2 helper inspection first hit Windows cp949 decoding of a UTF-8 Python comment, then report writing hit an em dash encoding error. Explicit UTF-8 parsing/report encoding fixed both. Final helper AST and safe imports passed. No native source/geometry/material mutation occurred.
- Earlier reviewed V2 draft and a later uncompiled revision were distinct hashes. Both were preserved: V2r1 reconstruction exactly matched its reviewed SHA; V2r2 separate SHA was retained. V3/R1 and V4/R2 are additive frozen packets and inherit no prior execution/compile approval.

Captured-smooth authority remains pending. Generated smooth.u8 is explicitly a derived absent-sharp-face source-policy expectation, anchored to the original inventory SHA, with native route comparison rejecting drift. It is not mislabeled an actual evaluated/Cycles buffer. Compile/runtime/probe coverage gaps are recorded separately and are not treated as preparation failures that were silently passed.
