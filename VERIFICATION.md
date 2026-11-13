# Verification record

Dataset: 335 rows, 12 columns. SHA-256: `ea705a4e445e8878d3c72b87bede3f92afff87cd93ba30f7e03f3849e1063b09`.

The scripts were run on 2026-11-13 with Python and the dependencies available in the working environment. Fold-wise scaling and the model selection from the consolidated manuscript were applied.

| Target | Reproduced MAE | Manuscript MAE |
|---|---:|---:|
| Relative permittivity | 0.00977249 | 0.00983 |
| Loss tangent | 0.0002768205 | 0.000277 |

The permittivity result is slightly different from the archived manuscript result; this was also observed in previous independent reproductions and should not be silently rounded into an exact match. The loss-tangent MAE matches the manuscript to the reported precision. Results may vary with dependency versions and numerical optimization.

This deposit is deliberately limited to the principal regression evaluation. The auxiliary studies and the full-wave model are not reproducible from this package alone.