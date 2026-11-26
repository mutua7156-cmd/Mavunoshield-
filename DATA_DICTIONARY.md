# Data dictionary

| Column | Required | Meaning | Unit / format |
|---|---|---|---|
| year | Yes | Calendar year of the observation | Integer |
| rainfall_mm | Yes | Rainfall total for a consistently defined season or year | Millimetres |
| season | No | Named season, e.g. MAM or OND | Text |
| location | No | Station, grid cell or area identifier | Text |
| source | No | Dataset/provider name | Text |

Do not combine different locations, seasons, or rainfall products without explicitly documenting the method. Missing observations should be handled and reported, not silently treated as zero.
