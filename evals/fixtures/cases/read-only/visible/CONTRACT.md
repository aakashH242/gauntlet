# Score contract

`clamp_score(score)` accepts an integer and returns an integer in the inclusive
range 0 through 100. Values below 0 return 0; values above 100 return 100;
values already in range are unchanged.
