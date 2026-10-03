# Float32 input identity before attributing a matrix delta

This additive note does not change the frozen b7f108d2 metadata packet or native data.

PM's bodyWorld~2.622604e-8 is a reported numeric component delta, not by itself proof that actual operator-input float32 bits differ. A decimal JSON value widened to float64 may differ from a directly widened native float32 value while both round to the same float32 value. Compare the **actual consumer matrix float32 input bits before the operator**, with full serialization/parse provenance, against NPZ body_world_f64 cast once to float32. Apply the same rule to rigWorld, rest and pose. Do not reconstruct a missing actual rigWorld from another matrix.

The direct native NPZ float64 matrices were independently verified to be exact widened float32 values. Inverse/rest/multiply operations performed in float64 and then rounded are distinct from native float32 operation ordering even when the input bits match. R2 has no internal native inverse-rest/deform/DQ/premat cache trace. Input identity is necessary before testing arithmetic, but does not prove operator identity or justify changing precision to achieve agreement.

Quaternion sign-aligned/component error and rest “same values” likewise do not replace the original raw wxyz/row-major float32 bit comparison. Preserve original source helpers/flags/weights and the unchanged tolerance gates. No cause is assigned by this note and no new source execution is requested.
