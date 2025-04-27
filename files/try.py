# Importing necessary libraries:
import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML
import networkx as nx  # For creating and managing graphs (NetworkX)

from urllib.parse import urlparse  # For safely handling and checking URLs

def fetch_page(url):
    """
    Fetch the HTML content of a web page. Adds 'http://' if missing.
    Returns the HTML content as a string if the request succeeds (status 200).
    """
    # Check if the URL has a scheme like 'http' or 'https'
    if not urlparse(url).scheme:
        url = "http://" + url  # Default to http if no scheme provided

    # Try to fetch the URL with a 5-second timeout and a user-agent header
    response = requests.get(url, timeout=5,
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
                                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                     'Accept-Language': 'en-US,en;q=0.5',
                                     'Connection': 'keep-alive'})

    # Return HTML content if request was successful
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch {url}, with status code {response.status_code}")
        return None


def extract_links(html):
    """
    Extract all hyperlinks from the given HTML using BeautifulSoup.
    Returns a list of href attributes from <a> tags.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # List all href attributes from anchor tags
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links

def filter_links(links, start_url):
    """
    Filter a list of links, returning only those that start with a specific path.
    Useful to keep the crawler focused on internal wiki pages, for example.
    """
    filtered_links = []
    for link in links:
        if link.startswith(start_url):  # Could be '/index.php/' or similar
            filtered_links.append(link)
    return filtered_links


def build_graph(start_url, depth, graph=None, max_nodes=0, max_children=0):
    """
    Recursively builds a graph of connected web pages starting from 'start_url'.

    Parameters:
    - start_url: the initial page to crawl from
    - depth: how deep the recursion should go
    - graph: an existing NetworkX graph to add to (or None to create new)
    - max_nodes: hard limit on total number of nodes to avoid infinite crawl
    - max_children: how many links to follow per page (randomly sampled)
    """

    if graph is None:
        graph = nx.Graph()  # Create a new graph if one isn't passed in

    if depth == 0:
        return graph  # Stop recursion when depth reaches zero

    if graph.number_of_nodes() > max_nodes:
        return graph  # Stop if the graph has grown beyond the limit

    html = fetch_page(start_url)

    if html:
        links = extract_links(html)
        # Keep only links that match the desired internal structure
        links = filter_links(links, "/index.php/")

        # Randomize the order of links and limit how many to follow
        import random
        random.shuffle(links)
        links = links[:max_children + 1]  # +1 ensures at least one is taken

        for link in links:
            # Convert relative link to full URL
            next_url = "https://awoiaf.westeros.org" + link
            if next_url not in graph:
                graph.add_node(next_url)  # Add node if it's not already there
            graph.add_edge(start_url, next_url)  # Connect current and next page

            # Recursively crawl deeper
            build_graph(next_url, depth - 1, graph, max_nodes=max_nodes, max_children=max_children)

    return graph


# Example usage:
start_url = "https://awoiaf.westeros.org/index.php/Main_Page"  # Starting point
depth_limit = 3  # Maximum depth of recursive crawling
graph = build_graph(start_url, depth_limit, graph=None, max_nodes=10_000, max_children=20)
