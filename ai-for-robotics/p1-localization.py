"""
Udacity - AI for Robotics - Lession 1 - Localization

Requires:
	- Python 3
	
	This code is taken from lecture 1 of AI for Robotics taught by Sebastian Thrun.  It tackles the essense of Localization, or how an autonomous robot may accurately figure out its position in an environment using sensors. A simple visual example of a robot in a 1D world:

[1] The robot starts in a state of uniform maximum confusion, or a uniform probability distribution.

    P ^		
      |
      |
      |________________________
      +------------------------> location

[2] Sense:  Then the robot senses where it is and modifies its probability distribution, guessing where it's likely to be based on the environment.

    P ^
      |   _    _         _
      |  / \  / \       / \ 
      |_/   \/   \_____/   \____ 
      +-------------------------> location

    Measurements are calculated via Bayes Rule:

    Say, Xi = location at a given point i, Z = measurement

    p(Xi|Z) = P(Z|Xi) * P(Xi) / P(Z)

    p(Xi|Z):  Belief of robot's location after seeing the measurement.
    p(Z|Xi):  Chances of seeing a particular landmark at a particular location.
    p(Xi):  Prior probability.
    p(Z):  Normalization. Therefore, p(Z) = sum_i( p(Z|Xi) * P(Xi) )  

[3] Motion:  Then the robot moves.  Its probability distribution of where it is moves with the robot, however the bumps flatten due to uncertainty(you arent sensing!).

    P ^
      |
      |        _    _        _
      |_______/ \__/ \______/ \_
      +-------------------------> location

    Motion is determined via Total Probability:

    p(Xi_t) = sum_j( p(Xj_t-1) * p(Xi|Xj) )

    p(Xi_t):  The probability of robot being in location Xi at time t.
    p(Xj_t-1):  All locations Xj the robot could have come from 1 timestep earlier.
    p(Xi|Xj):  The probability that the motion would carry the robot from Xj to Xi.


[4] Convolving sense [2] and move [3], or multiplying each probability in [2] and [3] at a location you get a posterior distribution with the robot's location!

    P ^        
      |        _ 
      |       / \ 
      |______/   \_____________
      +-------------------------> location

The code itself is a simulation of a robot in a 2D world.  Green ('G') and Red ('R') cells are the landmarks of this gridded world.  The world is also cyclic, so the robot may move from the last column or row to the first column or row. For example:

[0,0]         [0,x]
     R R G R R
     G G R G G
     R R G R R
[y,0]         [y,x]

Inputs:

	- colors: The environment, or world for the robot.
	- measurements:  What the robot sees at each time slot.
	- motions:  Where the robot moves in [y,x] format.
	- sensor_right:  The probability that the sensor is detecting the correct color. This is the measurement uncertainty.
	- p_move:  The probability that the robot overshoots or undershoots its intended location.  This is the actuator uncertainty.

Outputs:

	- p:  The probability distribution of the robot's location.

"""

colors = [['R', 'G', 'G', 'R', 'R'],
          ['R', 'R', 'G', 'R', 'R'],
	  ['R', 'R', 'G', 'G', 'R'],
	  ['R', 'R', 'R', 'R', 'R']]
measurements = ['G', 'G', 'G', 'G', 'G']
motions = [[0,0], [0,1], [1,0], [1,0], [0,1]]
sensor_right = 0.7
p_move = 0.8

def sense(p, colors, measurement):
	aux = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]
	s = 0.0
	for y in range(len(p)):
		for x in range(len(p[y])):
			hit = (measurement == colors[y][x])
			aux[y][x] = p[y][x] * (hit * sensor_right + (1 - hit) * (1 - sensor_right))
			s += aux[y][x]
	for y in range(len(aux)):
		for x in range(len(aux[y])):
			aux[y][x] /= s
	return aux

def move(p, motion):
	aux = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]
	for y in range(len(p)):
		for x in range(len(p[y])):
			aux[y][x] = (p_move * p[(y - motion[0]) % len(p)][(x - motion[1]) % len(p[y])]) + ((1 - p_move) * p[y][x])
	return aux

def show(p):
	for i in range(len(p)):
		print(p[i])


if len(measurements) != len(motions):
	raise ValueError("error in size of measurement/motion vector")

pinit = 1.0/float(len(colors))/float(len(colors[0]))
p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]

for t in range(len(measurements)):
	p = move(p, motions[t])
	p = sense(p, colors, measurements[t])

show(p)
