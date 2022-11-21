from csv import reader, writer, QUOTE_NONE
from random import randint

def main():
    '''This is the main function'''
    all_coords_lists = []
    dots_list = []
    dots_list = make_dots_list()
    beeline_lists = make_short_beelines(dots_list)
    for list in beeline_lists:
        all_coords_lists.append(list)
    shortest_lists = sort_lists(all_coords_lists)
    for n in range(len(shortest_lists)):
        list = extract_points(shortest_lists[n])
        original_distance = find_total_distance(list)
        shortest_list = use_all_methods(list, original_distance, 1, original_distance, len(list))
        desmos_list(shortest_list)

def use_all_methods(shortest_points, old_shortest_distance, number, original_distance, number_of_points):
    '''This switches between both algorithms used to shorten the lines until neither algorithm can make the line any shorter'''
    ordinal = ['0th','1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th']
    distances = []
    loop_number = 1
    for _ in range(0,5):
        print(f'\n\nStarting Switchblade Algorithim for the {ordinal[loop_number]} time')
        shortest_points, old_shortest_distance = switchblade(shortest_points, number_of_points, old_shortest_distance, original_distance, number)
        distance = find_total_distance(shortest_points)
        distances.append(distance)
        print(f'\nStarting New Rearrange Algorithim for the {ordinal[loop_number]} time')
        shortest_points, old_shortest_distance = rearrange_points(shortest_points, number_of_points, old_shortest_distance, original_distance, number)
        distance = find_total_distance(shortest_points)
        distances.append(distance)
        loop_number += 1
    print(f'distances = {distances}')
    print(f'last distance = {distance}')
    return shortest_points

def reverse_list(points, shortest_distance, reverse_start_index, reverse_end_index):
    '''This switches the endpoints of any two lines in a given path, it simply changes the list of points to make that happen'''
    points_copy = points.copy()
    reverse_list = []
    list_length = reverse_end_index - reverse_start_index
    for i in range(list_length):
        reverse_list.append(points[reverse_start_index+i])
        points_copy.remove(points[reverse_start_index+i])
    for n in range(list_length):
        points_copy.insert(reverse_start_index, reverse_list[n])
    total_distance = find_total_distance(points_copy)
    if total_distance > shortest_distance:
        return points_copy
    else:
        print('someting went wrong with reversing the list')
        print(f'total_distance = {total_distance}')
        print(f'shortest_distance = {shortest_distance}')

def switchblade(points, number_of_points, old_shortest_distance, original_distance, number):
    '''This algorithm essentially goes through a list of every line segment and predicts whether switching it's endpoints with the endpoints of any other line would make the overall path shorter '''
    for i in range(len(points)-1):
        for n in range(i+1,len(points)):
            if i == 0:
                old_distance = distance(points[n-1],points[n])
                new_distance = distance(points[i],points[n])
            elif i > 0:
                old_distance = distance(points[i-1],points[i]) + distance(points[n-1],points[n])
                new_distance = distance(points[i],points[n]) + distance(points[i-1],points[n-1])
            else:
                print(f'\n\n\nSorry, there has been an error!!')
            distance_saved = old_distance - new_distance
            if 0 < distance_saved:
                switched_points = reverse_list(points.copy(), new_distance, i, n)
                is_shorter, new_shortest_distance, number = report_progress('Switchblade', switched_points, number, original_distance, number_of_points, old_shortest_distance, i, n, distance_saved)
                if is_shorter:
                    return switchblade(switched_points, number_of_points, new_shortest_distance, original_distance, number)
    return points, old_shortest_distance

def report_progress(name, switched_points, number, original_distance, number_of_points, old_shortest_distance, i, n, distance_saved):
    '''This function checks whether the predicted distance change is correct and reports how much shorter the path becomes'''
    new_shortest_distance = find_total_distance(switched_points) # Remove this line when you feel that the code is ready
    if len(switched_points) != number_of_points:
        print('There has been an error. A point has been lost')
        print(f'len(switched_points) = {len(switched_points)},   number_of_points = {number_of_points}')
        return False, old_shortest_distance, number
    if round(new_shortest_distance,8) != round(old_shortest_distance - distance_saved,8):
        '''Hopefully this part of the function will never be called'''
        print('There was an error. the change in distance was not what we expected it to be.')
        print(f'old_shortest_distance = {old_shortest_distance}')
        print(f'new_shortest_distance = {new_shortest_distance}')
        print(f'find_total_distance(switched_points) = {find_total_distance(switched_points)}')
        print(f'old_shortest_distance - distance_saved = {old_shortest_distance - distance_saved}')
        print(f'distance_saved = {distance_saved}')
        print(f'{new_shortest_distance} != {old_shortest_distance - distance_saved}')
    if new_shortest_distance < old_shortest_distance:
        print(f'\n{name} Optimization number {number}:')
        print(f'Congrats! We found a new shorter path with a distance of {new_shortest_distance}')
        print(f'This optimization makes it {(old_shortest_distance - new_shortest_distance):.4f} shorter than the last path!')
        print(f'The path is now {100*(1 - new_shortest_distance/original_distance):.4f}% shorter than the original path!')
        print(f'The path is now {(original_distance - new_shortest_distance):.4f} blocks shorter than the original path!')
        number += 1
        return True, new_shortest_distance, number
    else:
        print(f'\n\n\nAn error has occurred! The line we calculated was shorter was not really shorter!')
        print(f'i = {i}, n = {n}')
        print(f'distance_saved = {distance_saved}')
        print(f'old_shortest_distance = {old_shortest_distance}.  new_shortest_distance = {new_shortest_distance}')
        return False, old_shortest_distance, number

def rounded(number, decimals=0):
    '''This rounds a given number to a certain number of decimals'''
    multiplier = 10 ** decimals
    return round(number * multiplier) / multiplier

def make_dots_list():
    '''This function reads a csv file to create a list of points that the program will then try to find the shortest paths between'''
    dots_list = []
    with open('dots.csv', "rt") as csv_file:
        csv_reader = reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            dots_list.append([int(line[0]), int(line[1])])
    return dots_list

def distance(coord1,coord2):
    '''Uses pythagrean theorm to find the distance between two given points'''
    distance = ((coord2[0]-coord1[0])**2 + (coord2[1]-coord1[1])**2)**0.5
    return distance

def make_distance_lists(coords, coord1 = 'N/A'):
    '''Creates a list of the distance from any given point to every other point'''
    distances = []
    '''distances = [[x_coord, y_coord], distance]'''
    if coord1 == 'N/A':
        coord1 = coords[-1]
    for coord in coords:
        distances.append([distance(coord1,coord), coord])
    return distances

def find_total_distance(list): #This is meant for lists of points only
    '''Finds the total distance of a path that connects every point to every other point'''
    total_distance = 0
    for n in range(len(list)-1):
        dist = distance(list[n],list[n+1])
        total_distance += dist
    return total_distance

def sort_lists(beeline_lists):
    '''This takes a list of paths to connect each point and sorts them by distance, the shortest ones first'''
    global shortest_beeline_distance
    def return_distance(list):
        return list[0]
    beeline_lists.sort(key=return_distance)
    shortest_beeline_distance = beeline_lists[0][0]
    return beeline_lists

def random_items(list, n_items):
    '''This function creates a list of random items from a much longer list. Essentially a random sample'''
    new_list = []
    while len(new_list) < n_items:
        ran_int = randint(0,len(list)-1)
        if list[ran_int] not in new_list:
            new_list.append(list[ran_int])
    return new_list

def find_nearest_neighbor(coord1, coords_original):
    '''This function finds the closest point to any given point'''
    coords = coords_original.copy()
    if coord1 in coords:
        coords.remove(coord1)
    distances = make_distance_lists(coords, coord1)
    distances.sort()
    coords = coords_original
    return distances[0][1]

def make_short_beelines(dots_list):
    '''This function goes through a list of points to perform the nearest neightbor algorithm starting at each point'''
    beeline_lists = []
    n_dots = len(dots_list)
    for n in range(n_dots):
        beeline_list = make_short_beeline(dots_list[n], dots_list.copy())
        beeline_lists.append(beeline_list)
        print(f'Completed Nearest Neighbor Algorithim Starting at Dot: {n}/{n_dots}')
    return beeline_lists

def make_short_beeline(last_dot, dots_list):
    '''This function performs the nearest neighbor algorithm starting at a given point'''
    beeline_list = [last_dot]
    dots_list.remove(last_dot)
    for _ in range(len(dots_list)):
        nearest_dot = find_nearest_neighbor(last_dot, dots_list)
        beeline_list.append(nearest_dot)
        dots_list.remove(nearest_dot)
        last_dot = nearest_dot
    beeline_list = points_to_lines(beeline_list)
    return beeline_list

def points_to_lines(points):
    '''This takes a list of only points and returns a list of each line and it's length'''
    lines = []
    for n in range(len(points)-1):
        lines.append([points[n],points[n+1]])
    return lines

def extract_points(list):
    '''This takes a list of each line and it's length, and returns list of only points'''
    points = [list[1][0]]
    for items in list[1:]:
        points.append(items[1])
    return points

def rearrange_points(points, number_of_points, old_shortest_distance, original_distance, number):
    '''This function tries moving every point to ever other place in the list to see if it makes the overall path shorter'''
    f = len(points) - 1
    for i in range(f+1):
        for n in range(f+1):
            if i != n:
                if i == 0 and 0 < n < f:
                    old_distance = distance(points[i],points[i+1]) + distance(points[n],points[n+1])
                    new_distance = distance(points[n],points[i]) + distance(points[i],points[n+1])
                elif i == 0 and n == f:
                    old_distance = distance(points[i],points[i+1])
                    new_distance = distance(points[n], points[i])
                elif  i < f and n == 0:
                    old_distance = distance(points[i-1],points[i]) + distance(points[i],points[i+1])
                    new_distance = distance(points[i],points[n]) + distance(points[i-1],points[i+1])
                elif 0 < i < f and 0 < n < i:
                    old_distance = distance(points[i-1],points[i]) + distance(points[i],points[i+1]) + distance(points[n-1],points[n])
                    new_distance = distance(points[i-1],points[i+1]) + distance(points[n-1],points[i]) + distance(points[i],points[n])
                elif  0 < i < f and i < n < f:
                    old_distance = distance(points[i-1],points[i]) + distance(points[i],points[i+1]) + distance(points[n],points[n+1])
                    new_distance = distance(points[i-1],points[i+1]) + distance(points[n],points[i]) + distance(points[i],points[n+1])
                elif  0 < i and n == f:
                    old_distance = distance(points[i-1],points[i]) + distance(points[i],points[i+1])
                    new_distance = distance(points[i-1],points[i+1]) + distance(points[n],points[i])
                elif i == f and n == 0:
                    old_distance = distance(points[i-1],points[i])
                    new_distance = distance(points[i],points[n])
                elif i == f and 0 < n:
                    old_distance = distance(points[i-1],points[i]) + distance(points[n-1],points[n])
                    new_distance = distance(points[n-1],points[i]) + distance(points[i],points[n])
                else:
                    print("Something has gone wrong for this function")
                    print(f' i = {i},  n = {n}')
                distance_saved = old_distance - new_distance
                if distance_saved > 0:
                    points_copy = points.copy()
                    points_copy.remove(points[i])
                    points_copy.insert(n, points[i])
                    is_shorter, new_shortest_distance, number = report_progress('New Rearrange Points', points_copy, number, original_distance, number_of_points, old_shortest_distance, i, n, distance_saved)
                    if is_shorter:
                        return rearrange_points(points_copy, number_of_points, new_shortest_distance, original_distance, number)
    return points, old_shortest_distance

def desmos_list(list):
    '''This Function prints out a list of coordinates that can be copy/pasted into Desmos to see what the paths found by the program look like'''
    desmos_print_list = []
    distance = find_total_distance(list)
    print(f'distance = {distance}')
    for items in list[1:]: # We're skipping the first element in the list
        desmos_print_list += f', ({items[0]}, {items[1]})'
    print(desmos_print_list.remove(','))
    write_to_csv(list, distance)

def write_to_csv(list, distance):
    '''This program prints the points as well as their distance to a format that can also be copy/pasted into Desmos, but you will have to backspace the distance part'''
    coordinates_list = [f'distance = {distance}, ({list[1][0]},{list[1][1]})']
    for items in list[1:]:
        coordinates_list.append(f'({items[0]},{items[1]})')
    with open('desmos_print_lists.csv', 'at', newline='\n') as csv_file:
        csv_writer = writer(csv_file, escapechar=' ', quoting=QUOTE_NONE)
        csv_writer.writerow(coordinates_list)

if __name__ == "__main__":
    main()