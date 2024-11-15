import re
from bs4 import BeautifulSoup
import requests

from plugin_search_interface import PluginSearchBase

def convert_size_to_bytes(size_str):
    size_str = size_str.lower()
    if 'kb' in size_str:
        size_in_bytes = float(size_str.replace('kb', '').strip()) * 1024
    elif 'mb' in size_str:
        size_in_bytes = float(size_str.replace('mb', '').strip()) * 1024 * 1024
    elif 'gb' in size_str:
        size_in_bytes = float(size_str.replace('gb', '').strip()) * 1024 * 1024 * 1024
    else:
        size_in_bytes = float(size_str)  # Assume bytes if no unit is specified
    return str(int(size_in_bytes))

def convert_results(books):
    results = []
    for book in books:
        for link in book["links"]:
            results.append({
                "link": link,
                "title": book["author"] + " - " + book["title"] + " (retail) (" + book["format_type"].lower() + ")",
                "description": f"{book['author']} - {book['title']} (retail) ({book['format_type'].lower()})",
                "guid": link,
                "comments": link,
                "files": "1",
                "size": book["size"],
                "category": "7020",
                "grabs": "100"
            })
    return results
    
def search_libgen(book):
    results = []
    try:
        print("Searching for " + book)
        item = book
        found_links = []
        non_standard_chars_pattern = r"[^a-zA-Z0-9\s.]"
        item = item.replace("ø", "o")
        cleaned_string = re.sub(non_standard_chars_pattern, "", item)
        search_item = cleaned_string.replace(" ", "+")
        url = "http://libgen.is/fiction/?q=" + search_item
        response = requests.get(url, timeout=120)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.find_all('tr')
            for row in rows:
                try:
                    # Extract author
                    author = row.select_one('ul.catalog_authors li a').text.strip()

                    # Extract title and link
                    title_tag = row.select_one('td p a')
                    title = title_tag.text.strip()
                    title_link = title_tag['href']

                    # Extract ASIN
                    asin = row.select_one('p.catalog_identifier').text.replace("ASIN: ", "").strip()

                    # Extract language
                    language = row.find_all('td')[3].text.strip()

                    format_size = row.find_all('td')[4].text.strip()
                    format_type = format_size.split(" / ")[0].strip()  # e.g., "EPUB"
                    size = convert_size_to_bytes(format_size.split(" / ")[1].strip())  # e.g., "374 Kb"

                    # Extract mirror links
                    links = [a['href'] for a in row.select('ul.record_mirrors_compact li a')]
                    links.append("https://ligben.is" + title_link)

                    # Store result in a dictionary
                    results.append({
                        'author': reverse_author_name(author),
                        'title': title,
                        'asin': asin,
                        'language': language,
                        'links': links,
                        'format_type': format_type,
                        'size': size
                    })

                except AttributeError:
                    # Skip rows that don't match the expected structure
                    continue

        else:
            ret = {"Status": "Error", "Code": "Libgen Connection Error"}
            print("Libgen Connection Error: " + str(response.status_code) + "Data: " + response.text)

    except Exception as e:
        print(str(e))
        raise Exception("Error Searching libgen: " + str(e))

    finally:
        return results


def reverse_author_name(name):
    # Split the name by the comma (if it's in the "Last, First" format)
    if ',' in name:
        last_name, first_names = name.split(',', 1)
        last_name = last_name.strip().capitalize()  # Capitalize the last name
        first_names = first_names.strip()
        formatted_first_names = " ".join([first.capitalize() for first in first_names.split()])
        return f"{formatted_first_names} {last_name}"
    else:
        # If no comma, it's just a single word name (e.g., "King")
        return name.capitalize()
        
class LibGenSearch(PluginSearchBase):
    def getcat(self):
        return ["7020"]

    def gettestquery(self):
        return "sample"

    def getprefix(self):
        return "libgen"

    def search(self, query):
        books = search_libgen(query)
        results = convert_results(books)
        return results



