import os
from dotenv import load_dotenv
import algorithm

if __name__ == '__main__':
    load_dotenv()

    if os.getenv('API_KEY') == '':
        raise Exception('API_KEY is not provided')
    if os.getenv('SECRET_KEY') == '':
        raise Exception('SECRET_KEY is not provided')
    
    algorithm.run()