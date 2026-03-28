import sys
import os

# Add your project directory to the path
project_home = '/home/<your-username>/Stock-Analyst/main'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['FLASK_DEBUG'] = 'false'

from app import app as application
