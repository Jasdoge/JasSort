# JasSort
KiCad Hand-soldering Annotator

This plugin adds an annotation button to the PCB Editor toolbar that re-annotates all components the following way:

1. Group by Reference, Value, Footprint
2. Arrange the groups by distance to top left of board.
3. Components within each group are sorted from left to right.

**Important: You'll need to manually go to Tools > Update Schematic From PCB when done**

### DOUBLE IMPORTANT: When updating schematic from PCB, you MUST UNCHECK "Re-link footprints to schematic symbols based on their reference designators"

Not doing so will **break** your schematic!


## Why this way?
1. Pick all of one type of component at a time. Ex: Your board has 10x 10k resistors R2-R11. Prepare 10 for placement.
2. Find the first one (R2) and place it. All other 10k resistors will now be below or to the right of it.
3. If you look at the board and find R4, but didn't find R3 yet, you know that it'll be between R2 (that you already placed) and R4.

It makes manually placing components a bit more efficient!

## Install
1. Git clone or unzip into your KiCad 6 plugin directory, such as %USERPROFILE%\Documents\KiCad\6.0\scripting\plugins<br />
  That way you should have a directory like %USERPROFILE%\Documents\KiCad\6.0\scripting\plugins\JasSort
2. If PCB Editor is running, go to Tools > External Plugins > Refresh Plugins.
3. An annotator icon with a J is added to the main toolbar. Clicking it will immediately perform the annotation.'
4. Go to Tools > Update Schematic From PCB. **Make sure `Re-link footprints to schematic symbols based on their reference designators` is UNCHECKED before accepting the change. Not doing so will break your schematic!**
