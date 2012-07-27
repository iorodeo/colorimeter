= Colorimeter.

Design files, software and firmware for IO Rodeos's open source (hardware &
software) scientific colorimeter kit for educators, students and DIY
scientists. 

Colorimeters are analytical devices commonly used in science labs to measure
the concentration of a solution from its light absorbing properties.
Colorimeters are extremely useful and flexible lab instruments for a wide range
of science education labs. Some examples of how the colorimeter can be used for
are listed below.

* Investigate Beers Law - Use food dye or other colored solution to investigate
the relationship between concentration and absorbance;

* Water quality - measure several water parameters such as turbidity, pH, water
hardness, phosphate content and more;

* Population growth - measure the absorbance of a microbial culture over time to
follow population growth;

* Enzyme kinetics - measure the activity of an enzyme over time and different
environmental parameters (temp, pH, inhibitors); Nitrogen cycle - quantify the
amount of ammonia, nitrite and nitrate in a newly established aquarium.

How it works: The colorimeter essentially consists of two electronics boards:
i) a red-green-blue (RGB) LED board and a light sensor board. A cuvette holder
in the center of the colorimeter properly positions the sample between the LED
and the sensor. The sensor board connects to an Arduino via the colorimeter
shield. When the colorimeter is operating, the RGB LED illuminates the sample
in the cuvette with one of three different wavelengths of light: 625 nm (red),
528 nm (true green) and 470 nm (blue). On the opposite side of the cuvette a
slit in the colorimeter allows light to pass through the sample to the light
sensor. Finally absorbance (A) of the sample is determined by comparing the
intensity of incident light (I0) to the intensity of light after it has passed
through the sample (I) using the following equation: A = log10(I/I0).

