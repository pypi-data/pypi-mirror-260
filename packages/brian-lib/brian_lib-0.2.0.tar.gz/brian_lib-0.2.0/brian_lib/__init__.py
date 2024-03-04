import sys
import os
sys.path.append(os.getcwd())
from beartype.claw import beartype_this_package
beartype_this_package()
