import os
import runpy

# Delegate to the real setup.py inside languages/python/oso/
ROOT = os.path.abspath(os.path.dirname(__file__))
SETUP_PATH = os.path.join(ROOT, "languages", "python", "oso", "setup.py")

if __name__ == "__main__":
    runpy.run_path(SETUP_PATH, run_name="__main__")
