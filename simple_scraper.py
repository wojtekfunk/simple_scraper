import requests
import click
from lxml.html import fromstring
from lxml import etree
import time

# url / patter for testing
# url_kaufland = "https://sklep.kaufland.pl/oferta/przeglad.html?kloffer-week=current&kloffer-category=04_Mro%C5%BConki"
# url_kaufland = "https://sklep.kaufland.pl/asortyment/swieze-artykuly.html"
# pattern = "//div[contains(@class, 'k-product-tile__title')]/text()"


def check_response(response):
    """
    Checks server response, returns False if not 200.
    """
    if response.status_code != 200:
        print(f"Error retrieving data, server response: {response.status_code}")
        return False
    else:
        print(f"Successfully connected with status code {response.status_code}, retrieving data...")
        return True
    

def write_fetched(response):
    """
    Writes fetched data to 'products_debug.html' file.
    """
    with open('products_debug.html', 'w', encoding='utf-8') as writer:
        writer.write(response.text)
        print("Fetched raw data saved to 'products_debug.html'")


def process_fetched(response, pattern):
    """
    Parses fetched data to html and processes with xpath pattern, returns [str] or None. 
    """
    print("Checking fetched data...")
    dom = fromstring(response.text)
    try:
        products = dom.xpath(pattern)
    except etree.XPathEvalError:
        print("Error! Invalid XPath expression, please try different pattern.")
        products = None
    return products


def check_fetched(fetched):
    """
    Prints info on fetched and processed list.
    """
    if not fetched:
        print("No products fetched, provide different url or pattern!")
        print("Please see 'products_debug.html' for details.")
        return False
    else:
        print(f"Success! Found {len(fetched)} products!")
        return True


def format_fetched(results):
    """
    Formats processed list into a dictionary.
    """
    items = []
    for i, result in enumerate(results, 1):
        items.append((i, result.replace('\n', '').strip()))
    return dict(items)


def print_result(results_dict:dict):
    """
    As name indicates... prints out results to the terminal.
    """
    for key, value in results_dict.items():
        print(f'{key} - {value}')


def save_result(results_dict:dict):
    """
    Writes results to 'scraped_products.txt' in the local context. 
    """
    with open('scraped_products.txt', 'w', encoding='utf-8') as writer:
        for key, value in results_dict.items():
            writer.write(f'{key} - {value}\n')
    print("Fetched products list saved to 'scraped_products.txt'")



def scrape_products(url, pattern):
    """
    Main module for products scraper.
    
    Organizes the flow of data nad sequence of each function, initiates target server communication.
    Provides server response to other functions.
    
    Required arguments:
    -url- provide url,
    -xpath_pattern- provide pattern for xpath html/text conversion.
    """
    separator = '-' * 80
    try:
        time.sleep(1)
        resp = requests.get(url)
        print(separator)
        if not check_response(resp):
            return
        print(separator)
        write_fetched(resp)
        print(separator)
        products = process_fetched(resp, pattern)
        if not check_fetched(products):
            return
        print(separator)
        results_dict = format_fetched(products)
        print_result(results_dict)
        print(separator)
        save_result(results_dict)
        print(separator)
    except requests.RequestException as error:
        print(f"Error fetching page: {error}")
    

@click.command()
@click.argument('url', nargs=1)
@click.argument('xpath_pattern', nargs=1)
def main(url, xpath_pattern):
    """
    Displays list of scraped products.
    
    Returns None, saves scraped raw data to 'products_debug.html' file in the local context with 'w' parameter,
    saves formatted list of scraped products to 'scraped_products.txt' file. The files will be
    overwritten each time the function is used.
    
    Required arguments:
    -url- provide url,
    -xpath_pattern- provide pattern for xpath html/text conversion.
    """
    scrape_products(url, xpath_pattern)


if __name__ == "__main__":
    main()