# untitled init
import os, logging

from .common import ABSPATH
from .engine import start_game

logging.basicConfig(
    filename=os.path.join(ABSPATH, "logs", "untitled_errors.log"),      # Name of the log file
    filemode='a',
    format='%(asctime)s %(levelname)s: %(funcName)s: %(message)s',
    level=logging.INFO
)

def main():
    start_game()

if __name__ == "__main__":
    main()
