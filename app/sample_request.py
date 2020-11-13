import itertools
import time
import requests
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED

 
def test_request(timeout: int):    
    resp = requests.get('https://exponea-engineering-assignment.appspot.com/api/work', timeout=timeout)
    resp.raise_for_status()
    if resp.status_code == 200:      
        data = resp.json()                
        return data      

def task(timeout:int):
    try:
       return test_request(timeout)
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    p = ThreadPoolExecutor(max_workers=None)
    timeout = 1
    tasks = [
        p.submit(
            task,
            obj[0]
        )
        for obj in [[1], [1], [1]]
    ]
    print(wait(tasks, timeout=timeout, return_when=ALL_COMPLETED))
    

        
              
