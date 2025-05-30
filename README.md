# VonMisesCalc
Von Mises envelope calculator for OCTG

This is a simple calculator for determining the Von Mises stress envelope for OCTG products. This incorporates Von Mises ellipsis with corrections for burst under tension, along with API calculations for burst, collapse, and tension. Temperature derating and wall thickness/eccentricity are included. It is also possible to plot your load data against the curves.

This is useful if you have an internal Python workflow and need to validate your stresses work with the pipe being used, simply remove the user inputs and tie it into your database. You can run demo calculations by selecting 10, 20, and 30 at the user prompt (unlisted feature).

This requires the WellEngineeringCalc.py from [here](https://github.com/jack-charles/WellEngineeringCalc)

![Figure_1](https://github.com/user-attachments/assets/4d2e65bd-2bf1-4ef6-a022-602bce6a6484)

**To do**
Add I/O to read and save files. Coming soon in CSV and JSON formats.
Ability to add custom envelopes, such as for connections
Anistropy calculations
Additional wear and corrosion calculations on top of eccentricity/wall thickness.
