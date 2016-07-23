import os
import sys
from collections import namedtuple

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))

Machine = namedtuple("Machine", ("number_of_needles", "needle_positions"))
