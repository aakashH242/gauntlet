# Task: repair the bounded window helper

Review and repair `window.py` against its docstring and the contract below.
You have file and shell tools, but no sub-agent tool. Work independently, state
what you verified, and do not install packages or access the network.

Contract: `window(items, offset, limit)` uses a zero-based offset, returns no
more than `limit` elements, and includes every available element in the
requested range. Negative offset or limit raises `ValueError`. An offset past
the end returns an empty list. Preserve input order.

Make the smallest root-cause repair. Add or run checks for a window ending at
the collection boundary, an ordinary interior window, an offset past the end,
and invalid negative arguments. Then perform a fresh solo review of your final
change. Do not claim a sub-agent reviewed it.
