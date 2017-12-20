#The idea of this code is build a football playing bot that can avoid all the 'player' bots and reach the ball and then shoot it to the goal.#
#So, image processing using opencCV was employed to detect the ball, all obstacles, goal and player bot#
#Once this data is obtained, we run the algorithm and determine the trajecotory the bot has to take#

import Field
import Imagepart

(a,b,c,d,e,f,g) = Imagepart.image_processing()

Field.graph_field(a,b,c,d,e,f,g)


