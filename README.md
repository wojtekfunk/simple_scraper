Simple scraper I wrote in python as an excersise for a python course.
Displays list of scraped products.
    
Returns None, saves scraped raw data to 'products_debug.html' file in the local context with 'w' parameter, saves formatted list 
of scraped products to 'scraped_products.txt' file. The files will be overwritten each time the function is used.
    
Required arguments:
 -url- provide url,
 -xpath_pattern- provide pattern for xpath html/text conversion.

Imports:
  requests,
  click,
  lxml,
  time
