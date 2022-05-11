# JasSort
KiCad Hand-soldering Annotator

This plugin adds an annotation button to the PCB Editor toolbar that re-annotates all components the following way:

1. Group by Reference, Value, Footprint
2. Arrange the groups by distance to top left of board.
3. Components within each group are sorted from left to right.

**Important: You'll need to manually go to Tools > Update Schematic From PCB when done**

## Why this way?
1. Pick all of one type of component at a time. Ex: Your board has 10x 10k resistors R2-R11. Prepare 10 for placement.
2. Find the first one (R2) and place it. All other 10k resistors will now be below or to the right of it.
3. If you look at the board and find R4, but didn't find R3 yet, you know that it'll be between R2 (that you already placed) and R4.

It makes manually placing components a bit more efficient!

