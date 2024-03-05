# __init__.py

# Import important classes, functions, or variables that you want to make available when the package is imported.
from .Classes import Line, LineSegment, Polygon
from .generate_line_segments import generate_line_segments
from .generate_line_network import generate_line_network
from .get_intersection_segments import get_intersection_segments
from .draw_segments import draw_segments

# Define the __all__ variable to specify what should be imported when using "from my_package import *".
__all__ = ['generate_line_segments', 
           'generate_line_network',
           'get_intersection_segments',
           'draw_segments', 
           'sample_in_polygon',
           'Line', 
           'LineSegment', 
           'Polygon'
           ]