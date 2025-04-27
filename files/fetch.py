import argparse
import requests

# Function to fetch the page with proxy and timeout
def fetch_page(url, proxy, timeout=5):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=timeout)
        response.raise_for_status()  # This will raise an exception for 4xx or 5xx responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

# Main function to build the graph (your original logic here)
def build_graph(start_url, depth_limit, graph=None, max_nodes=10_000, max_children=20):
    # Example function, modify with your own logic for graph building
    html = fetch_page(start_url, proxy)
    if html:
        print(f"Successfully fetched {start_url}")
    else:
        print(f"Failed to fetch {start_url}")

if __name__ == "__main__":
    # Parse arguments from the command line
    parser = argparse.ArgumentParser(description="Fetch a page using a proxy")
    parser.add_argument('proxy', type=str, help="The proxy address (e.g., 'proxy_address:port')")
    parser.add_argument('url', type=str, help="The URL to fetch (e.g., 'https://awoiaf.westeros.org/index.php/Main_Page')")
    args = parser.parse_args()

    # Now we can pass the proxy and url arguments to your code
    proxy = args.proxy
    url = args.url
    
    # Example usage: pass these to your graph-building function
    fetch_url(url, proxy)
