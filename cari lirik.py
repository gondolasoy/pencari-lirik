import requests
from bs4 import BeautifulSoup
import os
import time

album_data = []

def crawl_and_store(url, file_path):
    global album_data
    # Send a GET request to the URL
    response = requests.get(url)
    time.sleep(10)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    album_divs = soup.find_all(class_="album")

    for album_div in album_divs:
        album_name = album_div.b.get_text()
        links = []
        next_sibling = album_div.find_next_sibling()

        while next_sibling and next_sibling.get('class') != ['album']:
            link = next_sibling.find('a')
            if link:
                links.append(link['href'])
            next_sibling = next_sibling.find_next_sibling()

        album_data.append({'album_name': album_name, 'links': links})

def change_title(title):
    title = title.replace('"', '')
    title = title.replace("?", "")
    title = title.replace("\\", "")
    title = title.replace("/", "")
    title = title.replace("*", "")
    title = title.replace(":", "")
    title = title.replace("<", "")
    title = title.replace(">", "")
    title = title.replace("|", "")
    return str(title)


def crawl_lyrics(url_file_path, output_folder):
    content = ""
    response = requests.get(url_file_path)
    soup = BeautifulSoup(response.content, 'html.parser')
    time.sleep(10)

    title = soup.find('h1').get_text()
    title = change_title(title)

    lyric_next = soup.find(class_="ringtone")
    next_sibling = lyric_next.find_next_sibling()

    while next_sibling and next_sibling.get('class') != ["noprint"]:
        content = content + str(next_sibling.get_text())
        next_sibling = next_sibling.find_next_sibling()

    # Create the file path and filename
    filename = f"{title}.md"
    file_path = os.path.join(output_folder, filename)

    print(title)

    # Write the page content to the Markdown file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"# {title}\n\n")
        file.write(content)


# Specify the URL to crawl
url = input("Enter the URL of the band in AzLyrics: ")

# Specify the output folder
output_folder = input("Enter the path of the output folder: ")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Call the function to crawl and store the URL content
crawl_and_store(url, output_folder)

for album_list in album_data:
    print(album_list['album_name'])

album_target = input("Enter the album you want to find: ")
for album_list in album_data:
    if album_list['album_name'] == album_target:
        links = album_list['links']
        for link in links:
            link_target = "https://www.azlyrics.com" + link
            crawl_lyrics(link_target, output_folder)
