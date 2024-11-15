import requests
from bs4 import BeautifulSoup
import os
import re

from plugin_download_interface import PluginDownloadBase

class LibGenDownload(PluginDownloadBase):
    def getprefix(self):
        return ["libgen"]

    def download(self, url, title, download_dir, cat):
        full_download_dir = os.path.join(download_dir, cat, title)
        os.makedirs(full_download_dir, exist_ok=True)
        print(full_download_dir)
        full_filename = os.path.join(full_download_dir, title)

        response = requests.get(url, timeout=120)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            download_div = soup.find("div", id="download")

            if download_div:
                download_link = download_div.find("a")
                if download_link:
                    link_url = download_link.get("href")
                else:
                    return "404"
            else:
                elements_with_get = soup.find_all(string=lambda text: "GET" in text)

                for element_text in elements_with_get:
                    parent_element = element_text.parent
                    download_link = parent_element.find("a") if parent_element else None
                    if download_link:
                        link_url = download_link.get("href")
                        break
                else:
                    return "404"

            dl_resp = requests.get(link_url, stream=True)

            if dl_resp.status_code == 200:
                file_type = os.path.splitext(link_url)[1]
                valid_book_extensions = [".pdf", ".epub", ".mobi", ".azw", ".djvu", ".azw3"]
                if file_type not in valid_book_extensions:
                    return "404"

                # Download file
                full_filename += file_type
                with open(full_filename, "wb") as f:
                    for chunk in dl_resp.iter_content(chunk_size=1024):
                        f.write(chunk)
                return full_filename
            else:
                return "404"
        else:
            return "404"