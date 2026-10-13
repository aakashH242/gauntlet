# Stable uniqueness contract

`stable_unique(values)` returns each distinct hashable value exactly once, in
the order of that value's first occurrence in `values`. It does not sort. For
example, `["pear", "apple", "pear", "fig"]` becomes
`["pear", "apple", "fig"]`.
