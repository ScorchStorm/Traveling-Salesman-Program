# Connect-The-Dots
Finds A Really Short Path To Connect A Bunch of Points A.K.A. Connects the Dots With a Really Short Line

This program uses the nearest neighbor algorithm (which always adds to the line the next closest dot that isn't part of the line already) for every point entered into it, and sorts them by their length. Next 2 algorithms, one which moves individual points and the other which switches endpoints of line segments cycle through every point and line to attempt to make the overall path (the series of all lines) shorter. When neither of those algorithms can shorten the line, it prints the series of points in that optimized line. It then moves onto the next point and uses the 2 algorithms to shorten it. It continues this until all lines made by the nearest neighbor algorithm have been completely optimized by both algorithms.

It might sound like this will take a while, but its actually rather fast because of the optimizations I've made to it. The computer doesn't have to calculate the length of the entire line made to find the difference made by moving one point for switching the end points of one lien segment with the end points of another line segment. It instead makes calculations based only on the line segments which will actually change. This greatly increases the speed of the calculations it makes and allows the program to more quickly optimize paths.

To run this file, you will need to save two separate .csv files in the same directory as this one. 
Name first file dots.csv, and add you list of the coordinates of your dots to it, the first column will the x coordinate of each dot, and the 2nd column will be the y coordinate
Name the second file desmos_print_list.csv. It will save the shortest path it can find as a list of coordinates which you can copy and paste into Desmos to see a visual representation of the path
