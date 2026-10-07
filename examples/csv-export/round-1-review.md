# Round 1: real delegated findings

Snapshot: 4c4782a8978d4321ad560b2205acdeea4e29877fd243b1cd9008a9b9eb60ba80.

csv_contract_review: confirmed zero/false loss caused by value || ''. Probed empty inputs, scalar conversion, frozen and mutable inputs; no mutation found. Encoding outside assigned lens.
csv_encoding_review: independently reproduced zero/false loss and missing standalone CR quoting. Baseline, eight directed cases and six neighboring checks executed. Commas, quote doubling, LF, CRLF and trailing empty cells behaved as expected.

Parent independently reproduced [[0,false]] -> ',' instead of '0,false', and [['a\rb']] -> bare a\rb instead of quoted cell. Both confirmed with executable evidence. Duplicate scalar-loss reports merged by mechanism. Severity recorded medium for this isolated utility; no production loss or deployment asserted.

F-01: scalar preservation violated because truthiness fallback conflates valid 0/false with missing values. Fix at shared cell conversion.
F-02: CR quoting invariant violated because quote-trigger character class lacks carriage return. Fix at shared cell encoder.
Only one shared encoding path exists; every cell routes through it. Formula evaluation and unsupported input types explicitly outside contract.
