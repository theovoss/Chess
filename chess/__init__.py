"""Package for Chess."""

import os

__project__ = 'Chess'
__version__ = '0.1.0'

VERSION = __project__ + '-' + __version__

script_dir = os.path.dirname(__file__)
standard_chess_json = os.path.join(script_dir, 'chess_game.json')
