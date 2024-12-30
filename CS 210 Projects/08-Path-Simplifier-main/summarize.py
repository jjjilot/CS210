"""
Summarize a path in a map, using the standard Ramer-Douglas-Peucher (aka Duda-Hart)
split-and-merge algorithm.
Author: Josh Jilot
Credits: Just me :)
"""

import csv
import doctest
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

import geometry
import map_view
import config

def read_points(path: str) -> list[tuple[float, float]]:
    '''read CSV into list of (easting, northing) tuples'''
    coords_list = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            easting = float(row['Easting'])
            northing = float(row['Northing'])
            coords_list.append((easting, northing))

    return coords_list

def summarize(points: list[tuple[float, float]],
              tolerance: int = config.TOLERANCE_METERS,
              ) -> list[tuple[float, float]]:
    '''
    summarize points and return summary
    
    >>> path = [(0,0), (1,1), (2,2), (2,3), (2,4), (3,4), (4,4)]
    >>> expect = [(0,0), (2,2), (2,4), (4,4)]
    >>> simple = summarize(path, tolerance=0.5)
    >>> simple == expect
    True
    '''

    summary: list[tuple[float, float]] = [points[0]]
    epsilon = float(tolerance * tolerance)

    def simplify(start: int, end: int):
        """Add necessary points in (start, end] to summary."""
        map_view.scratch(points[start], points[end])
        greatest_index = 0
        greatest_dist = 0
        
        for point in points[start + 1: end]:
            point_dist = geometry.deviation_sq(points[start], points[end], point)
            if (point_dist > epsilon) and (point_dist > greatest_dist):
                greatest_dist = point_dist
                greatest_index = points.index(point)

        if greatest_dist != 0:
            simplify(start, greatest_index)
            simplify(greatest_index, end)
        else:  
            summary.append(points[end])
            map_view.plot_to(point)

        log.debug(f"Simplifying from {start}: {points[start]} to {end}: {points[end]}, {points[start+1:end]}")
        log.debug(f"Summary so far: {summary}")
        return

    simplify(0, len(points)-1)
    map_view.clean_scratches()
    return summary

def main():
    map_view.init()
    points = read_points(config.UTM_CSV)
    #for point in points:
    #    map_view.plot_to(point)
    #map_view.wait_to_close()
    print(f"{len(points)} raw points")
    summary = summarize(points, config.TOLERANCE_METERS)
    print(f"{len(summary)} points in summary")
    
if __name__ == "__main__":
    doctest.testmod()
    print("Doctests Complete!")
    main()
