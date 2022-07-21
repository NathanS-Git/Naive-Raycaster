# Naive Raycaster
This utilizes the very old method Wolfenstein 3D used - albeit modified. It sends out *n* rays from the camera, and the distance they intersect with an object at, you draw a rectangle of width ![delta d](https://latex.codecogs.com/svg.image?\Delta&space;d) , and height corresponding to the distance. This creates the illusion of a first person view. The actual calculation method for determining intersection distance is different from the Wolfenstein 3D method - but the end result is visually identical. 

## Top-down view
![A Gif showing the top-down view](docs/top_down.gif)

You can change the view in the running program by pressing 'v'.

## First person view
![A Gif showing the first person view](docs/first_person.gif)
*(This is not 1:1 with the above gif)*

### More info
This project was inspired by this [tutorial](https://lodev.org/cgtutor/raycasting.html).