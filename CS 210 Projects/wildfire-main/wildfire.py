"""
Geographic clustering of historical wildfire data
CS 210, University of Oregon
Author: Josh Jilot
Credits: Just me :)
"""
import doctest
import csv
import random

import graphics.utm_plot
import config

def make_map() -> graphics.utm_plot.Map:
    """Create and return a basemap display"""
    map = graphics.utm_plot.Map(config.BASEMAP_PATH,
                                config.BASEMAP_SIZE,
                                (config.BASEMAP_ORIGIN_EASTING, config.BASEMAP_ORIGIN_NORTHING),
                                (config.BASEMAP_EXTENT_EASTING, config.BASEMAP_EXTENT_NORTHING))
    return map

def get_fires_utm(path: str) -> list[tuple[int, int]]:
    """
    Read CSV file specified by path, returning a list 
    of (easting, northing) coordinate pairs within the 
    study area. 
    
    >>> get_fires_utm("data/test_locations_utm.csv")
    [(442151, 4729315), (442151, 5071453), (914041, 4729315), (914041, 5071453)]
    """
    fire_list = []

    with open(path, newline="", encoding="utf-8") as source_file:
        reader = csv.DictReader(source_file)
        for row in reader:
            easting = int(row["Easting"])
            northing = int(row["Northing"])
            if in_bounds(easting, northing):
                coords = (easting, northing)
                fire_list.append(coords)

    return fire_list

def in_bounds(easting: float, northing: float) -> bool:
    """Is the UTM value within bounds of the map?"""
    if (easting < config.BASEMAP_ORIGIN_EASTING
        or easting > config.BASEMAP_EXTENT_EASTING
        or northing < config.BASEMAP_ORIGIN_NORTHING
        or northing > config.BASEMAP_EXTENT_NORTHING):
        return False
    return True

def plot_points(fire_map: graphics.utm_plot.Map,
                points:  list[tuple[int, int]],
                size_px: int = 5,
                color: str = "green") -> list:
    """
    Plot all the points and return a list of handles that
    can be used for moving them.
    """
    symbols = []
    for point in points:
        easting, northing = point
        symbol = fire_map.plot_point(easting, northing, 
                                     size_px=size_px, color=color)
        symbols.append(symbol)
    return symbols

def assign_random(points: list[tuple[int, int]], n: int) -> list[list[tuple[int, int]]]:
    """
    Returns a list of n lists of coordinate pairs.
    The i'th list is the points assigned randomly to the i'th cluster.
    """
    # Initially the assignments is a list of n empty lists
    assignments = []
    for i in range(n):
        assignments.append([])
    # Then we randomly assign points to lists
    for point in points:
        choice = random.randrange(n)
        assignments[choice].append(point)
    return assignments

def centroid(points: list[tuple[int, int]]) -> tuple[int, int]:
    """The centroid of a set of points is the mean of x and mean of y"""
    x_sum = 0
    y_sum = 0

    if len(points) == 0:
        x_avg = 0
        y_avg = 0
    else:  
        for point in points:
            x_sum += point[0]
            y_sum += point[1]
        x_avg = x_sum // len(points)
        y_avg = y_sum // len(points)

    return (x_avg, y_avg)

def cluster_centroids(clusters: list[list[tuple[int,int]]]) -> list[tuple[int,int]]:
    """Return a list containing the centroid corresponding to each assignment of
    points to a cluster.
    """
    centroids = []
    for cluster in clusters:
        centroids.append(centroid(cluster))
    return centroids

def sq_dist(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """
    Square of Euclidean distance between p1 and p2

    >>> sq_dist([2, 3], [3, 5])
    5
    """
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    return dx*dx + dy*dy

def closest_index(point: tuple[int, int], centroids: list[tuple[int, int]]) -> int:
    """
    Returns the index of the centroid closest to point

    >>> closest_index((5, 5), [(3, 2), (4, 5), (7, 1)])
    1
    """
    closest = 0
    closest_id = 0
    
    for centroid in centroids:
        distance = sq_dist(point, centroid)
        if closest == 0:
            closest = distance
        elif distance < closest:
            closest = distance
            closest_id = centroids.index(centroid)

    return closest_id

def assign_closest(points: list[tuple[int,int]],
                   centroids: list[tuple[int, int]]
                   ) -> list[list[int, int]]:
    """
    Returns a list of lists.  The i'th list contains the points
    assigned to the i'th centroid.  Each point is assigned to the
    centroid it is closest to.

    >>> assign_closest([(1, 1), (2, 2), (5, 5)], [(4, 4), (2, 2)])
    [[(5, 5)], [(1, 1), (2, 2)]]
    """
    centroid_list = []

    for centroid in centroids:
        centroid_list.append([])
        
    for point in points:
        closest_id = closest_index(point, centroids)
        centroid_list[closest_id].append(point)

    return centroid_list

def move_points(fire_map: graphics.utm_plot.Map,
                points:  list[tuple[int, int]], 
                symbols: list): 
    """Move a set of symbols to new points"""
    for i in range(len(points)):
        fire_map.move_point(symbols[i], points[i])

def show_clusters(fire_map: graphics.utm_plot.Map, 
                  centroid_symbols: list, 
                  assignments: list[list[tuple[int, int]]]):
    """Connect each centroid to all the points in its cluster"""
    for i in range(len(centroid_symbols)):
        fire_map.connect_all(centroid_symbols[i], assignments[i])

def main():
    doctest.testmod()
    fire_map = make_map()
    points = get_fires_utm(config.FIRE_DATA_PATH)
    fire_symbols = plot_points(fire_map, points, color="red")

    # Initial random assignment
    partition = assign_random(points, config.N_CLUSTERS)
    centroids = cluster_centroids(partition)
    centroid_symbols = plot_points(fire_map, centroids, size_px=10, color="blue")

    # Continue improving assignment until assignment doesn't change
    for i in range(config.MAX_ITERATIONS):
        old_partition = partition
        partition = assign_closest(points, centroids)
        if partition == old_partition:
            # No change ... this is "convergence"
            break
        centroids = cluster_centroids(partition)
        move_points(fire_map, centroids, centroid_symbols)

    # Show connections at end
    show_clusters(fire_map, centroid_symbols, partition)

    input("Press enter to quit")

if __name__ == "__main__":
    main()
