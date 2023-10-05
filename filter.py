import csv
import requests
import threading

FILE_NAME = "url.csv"
MAX_THREADS = 10  # You can adjust this number based on your machine's capabilities.

# Disable the warnings about not verifying the certificate
requests.packages.urllib3.disable_warnings()

# Thread lock for writing to the CSV
lock = threading.Lock()

def check_protocol_reachability(url, protocol):
    try:
        print(f"Checking for this {protocol} URL: {url}")
        response = requests.get(f"{protocol}://{url}", timeout=5, verify=False)
        return True
    except requests.exceptions.ConnectionError:
        print(f"Failed to connect to {url} due to a connection error.")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred when connecting to {url} using {protocol}: {e}")
    return False

def reachable(url, good_csv):
    protocols = ["https", "http"]
    for protocol in protocols:
        if check_protocol_reachability(url, protocol):
            with lock:  # Ensure only one thread writes to the file at a time.
                good_csv.write(f"{url}\n")
            return

def find_reachable_links(name):
    with open("fixed_url.csv", 'a') as good_csv:
        with open(name, 'r') as url_csv: 
            lines = url_csv.readlines()
            threads = []
            
            for line in lines:
                result = line.split(',')
                url = result[0]
                
                if url == "URL" or len(result) > 2:
                    continue

                thread = threading.Thread(target=reachable, args=(url, good_csv))
                threads.append(thread)
                thread.start()

                # Wait for all threads to finish if we've reached the max thread limit
                if len(threads) == MAX_THREADS:
                    for thread in threads:
                        thread.join()
                    threads = []

            # Ensure any remaining threads finish
            for thread in threads:
                thread.join()

find_reachable_links(FILE_NAME)
