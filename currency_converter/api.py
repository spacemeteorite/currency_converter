# Get currencgeolocation eexchange_rateschange rates based on EUR
# API site: https://www.vatcomplgeolocation.com/

import requests
import json
import threading
import time
from queue import Queue, Empty



def timer(func):
    def timed_func():
        start_time = time.time()
        print(f"<func {func.__name__}> started")
        func()
        end_time = time.time()
        print(f"<func {func.__name__}> consumes {end_time - start_time}")
    return timed_func


def get_exchange_rates(base: str='EUR',
                       selected_currencies: tuple[str]=None) -> dict:
    """
    Summary:
        use api provided by 'https://www.vatcomplgeolocation.com/' to fetch 
        currencies exchange rates.
    Keyword Arguments:
        selected_currencies -- choose what currencies' rates you want to fetch,
                               if None, return whole dict.
        base -- fetch currencies's rates based on base currency.
    Return:
        rates_dict -- return a dict consist of currencies' rates with base
                      currency's rate=1.

    Note:
        available currency types(base: 'EUR'):
            ['EUR', 'USD', 'JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN', 'RON', 
            'SEK', 'CHF', 'ISK', 'NOK', 'TRY', 'AUD', 'BRL', 'CAD', 'CNY', 'HKD', 
            'IDR', 'ILS', 'INR', 'KRW', 'MXN', 'MYR', 'NZD', 'PHP', 'SGD', 'THB', 
            'ZAR']
    """
    print('try connecting api')

    response = requests.get(f"https://api.vatcomply.com/rates?base={base}")
    response_dict = json.loads(response.text)

    print('response got')

    if selected_currencies == None:
        return response_dict['rates']        
    else:
        rates_dict = {k: response_dict['rates'][k] for k in selected_currencies}
        return rates_dict


def get_geolocation() -> dict:
    response = requests.get("https://api.vatcomply.com/geolocate")
    response_dict = json.loads(response.text)
    return response_dict


def worker(work_queue: Queue):
    while not work_queue.empty():
        try:
            item = work_queue.get_nowait()
        except Empty:
            break
        else:
            get_exchange_rates(base=item)
            work_queue.task_done()


def main():
    work_queue = Queue()

    li = ['EUR', 'USD', 'ILS']
    for e in li:
        work_queue.put(e)
    
    threads = [
        threading.Thread(target=worker, args=(work_queue, ))
        for _ in range(THREAD_POOL_SIZE)
    ]

    for thread in threads:
        thread.start()

    work_queue.join()

    while threads:
        threads.pop().join()


if __name__ == "__main__":
    THREAD_POOL_SIZE = 4
    started = time.time()
    main()
    elapsed = time.time() - started

    print()
    print(f"time elapsed: {elapsed:.2f}s")

    print(get_exchange_rates(base='USD'))