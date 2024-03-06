import geopandas as gpd
import shapely

from cartagen4py.algorithms.lines.line_smoothing import *
from cartagen4py.utils.geometry.angle import *
from cartagen4py.utils.geometry.line import *

from test_functions import *

def detect_bends(line, sigma, threshold):
    """
    Detect bends from a given LineString.
    """

    # Create the gaussian smoothed line
    smoothed = gaussian_smoothing(line, sigma, threshold, densify=False)

    # Get inflexion points indexes
    indexes = inflexion_points(smoothed)

    vertices = list(line.coords)

    current = []
    lines = []
    for i, vertex in enumerate(vertices):
        current.append(vertex)
        if i in indexes:
            lines.append({'bend': get_bend_side(shapely.LineString(current)), 'geometry': shapely.LineString(current)})
            current = [vertex]

    lines.append({'bend': get_bend_side(shapely.LineString(current)), 'geometry': shapely.LineString(current)})
    
    make_gdf([{'geometry': shapely.Point(list(smoothed.coords)[x])} for x in indexes], 'inflexion')
    make_gdf(lines, 'lines')

    return smoothed