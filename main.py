import os
from dotenv import load_dotenv
from pathlib import Path

Path('.logs').mkdir(parents=True, exist_ok=True)
Path('.cache').mkdir(parents=True, exist_ok=True)

from lib import algorithm


if __name__ == '__main__':
    load_dotenv()

    if os.getenv('API_KEY') == '':
        raise Exception('API_KEY is not provided')
    if os.getenv('SECRET_KEY') == '':
        raise Exception('SECRET_KEY is not provided')
    
    algorithm.run()
    
