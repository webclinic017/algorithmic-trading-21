import os
from dotenv import load_dotenv
import algorithm

if __name__ == '__main__':
    load_dotenv()

    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('SECRET_KEY')
    
    if api_key == '':
        raise Exception('API_KEY is not provided')
    if secret_key == '':
        raise Exception('SECRET_KEY is not provided')
    
    algorithm.run()