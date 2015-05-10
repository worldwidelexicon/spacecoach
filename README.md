# Spacecoach
Spacecoach parametric model
by Brian S McConnell <bsmcconnell@gmail.com>

This parametric model is used to generate the graphs at spacecoachmodels.appspot.com.

USAGE:

from spacecoach import spacecoach

s = spacecoach(mass=40000, water_cost=1700) # for a 40,000 kg ship with Falcon 9 Heavy water delivery to LEO

print s.data


When you initialize the spacecoach class, it will calculate costs for a variety of missions across a range
of values for specific impulse. This data is stored as a two dimensional dictionary array in the data property
of the class.

The method generate_html() converts the data into a data series that can be imported into a highcharts spline
graph (we use this in the interactive graphing tool at spacecoachmodels.appspot.com)

The delta-v values for each mission are approximate, and assume low thrust propulsion to/from EML-2 and the destination. This is sufficient for general estimation, but you'll want to do a numerical simulation using a tool like STK to get exact delta-v numbers.

The parametric model accounts for the following factors:

* The cost of fabricating the ship (default: $200,000,000)
* The number of missions per ship service life (default: 10 missions)
* The cost of launching non-water material and equipment to low earth orbit (default: $1700 for Falcon 9 Heavy)
* The cost of launching water to low earth orbit (default: $1700 for Falcon 9 Heavy)
* The cost of launching crew, perishables and last minute supplies via Falcon 9 Heavy on via chemical propulsion (default: $105,000,000)
* Engine specific impulse, used to calculate the cost of boosting material to EML-2 via electric propulsion (assume ~ 7 km/s to spiral out from LEO to EML-2)
* Engine specific impulse, used to calculate mass budget for the interplanetary trip
* Calculates total mission cost across a range of specific impulse from 1,000s to 5,000s

Feel free to experiment with different parameter values to see how mission costs vary in relation to delta-v and specific impulse in particular.

SUMMARY: using reasonable assumptions about ship service life, and with engine specific impulse expected to be 1,500-2,000s or better, even fairly large ships can be operated inexpensively by manned spaceflight standards, well under the cost of a Space Shuttle mission even for ambitious destinations like Ceres.
