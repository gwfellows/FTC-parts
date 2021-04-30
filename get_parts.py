from bs4 import BeautifulSoup
import requests
import shutil
import zipfile
import os


def get_goBILDA_parts():
    filepath = "./goBILDA"

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
                filename = filepath + \
                    step_link.replace('/content/step_files/', '')
                print("Processing "+filename+"...")
                with open(filename, 'wb') as file:
                    file.write(requests.get(
                        'https://www.gobilda.com'+step_link).content)
                if zipfile.is_zipfile(filename):
                    with zipfile.ZipFile(filename, "r") as to_unzip:
                        if len(to_unzip.namelist()) > 1:
                            to_unzip.close()
                            os.remove(filename)
                            print("Done\n")
                            break
                        to_unzip.extractall()
                else:
                    os.remove(filename)
                    print("Done\n")
                    break
                os.remove(filename)
                print("Done\n")


def get_REV_parts():
    filepath = "./REV/ALL-REV-PARTS-STEP.zip"
    partslink = "https://www.revrobotics.com/content/cad/ALL-REV-PARTS-STEP.zip"
    with open(filepath, 'wb') as file:
        file.write(requests.get(partslink).content)
    with zipfile.ZipFile(filepath, "r") as to_unzip:
        to_unzip.extractall(path="./REV")
    shutil.copytree("./REV/Already Uploaded", "./REV", dirs_exist_ok=True)
    os.remove(filepath)
    shutil.rmtree("./REV/Already Uploaded")

    files_in_directory = os.listdir("./REV")
    filtered_files = [
        file for file in files_in_directory if not file.endswith(".STEP")]
    for file in filtered_files:
        path_to_file = "./REV/"+file
        os.remove(path_to_file)


get_REV_parts()
get_goBILDA_parts()
