from bs4 import BeautifulSoup
import requests
import zipfile
import os

sitemap_page = requests.get(
    'https://www.gobilda.com/sitemap/categories/', allow_redirects=True)
section_links = (str(a['href']) for a in BeautifulSoup(sitemap_page.content, 'html.parser').find(
    'div', class_='container').find_all('a'))

for section_link in section_links:
    section_page = requests.get(section_link, allow_redirects=True)
    part_links = (str(a['href']) for a in BeautifulSoup(
        section_page.content, 'html.parser').find_all('a', class_='card'))

    for part_link in part_links:
        if part_link[0] == '/':
            part_link = 'https://www.gobilda.com'+part_link
        part_page = requests.get(part_link, allow_redirects=True)
        step_links = (str(a['href']) for a in BeautifulSoup(
            part_page.content, 'html.parser').find_all('a', class_='product-downloadsList-listItem-link ext-zip'))

        for step_link in step_links:
            filename = "./"+step_link.replace('/content/step_files/', '')
            with open(filename, 'wb') as file:
                file.write(requests.get(
                    'https://www.gobilda.com'+step_link).content)
            if zipfile.is_zipfile(filename):
                with zipfile.ZipFile(filename, "r") as to_unzip:
                    if len(to_unzip.namelist()) > 1:
                        to_unzip.close()
                        os.remove(filename)
                        break
                    to_unzip.extractall()
            else:
                os.remove(filename)
                break
            os.remove(filename)
