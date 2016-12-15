## Game of ~~life~~ evolution

#Rules
Standart gol rules but cells can move and each cell has 
a genome that determines their preferences of movement.
Red color means cell likes to be alone, blue means cell
likes to be in a big company, grean means cell likes to be
near 2 or 3 cells. Also cells can mutate with 1/100 chance.

#Requierments
[Python3](www.python.org)
[pygame](http://www.pygame.org/download.shtml)

#How to launch
By double-click or by a comand:
  `python gol.py %width% %height%`
  width and height are optional, default is 600, 400
