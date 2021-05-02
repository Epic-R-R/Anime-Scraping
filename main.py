from PyInquirer import prompt
from colorama import init, Fore
from halo import Halo
from styles import style
from time import sleep
import sys

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(f'{Fore.RED}Some modules are not installed! Installing them with this command.\n{Fore.GREEN}pip install -r requirement.txt')

title = []
link = []

def details(link):
    source_code = requests.get("https://www10.gogoanime.io"+link)
    content = source_code.content
    soup = BeautifulSoup(content,'html.parser')
    container_soup = soup.find('div', {'class':'anime_info_body_bg'})
    print("\nName of the Anime : ", container_soup.find('h1').getText(),"\n") 
    titles_detail = container_soup.find_all('p',{'class':'type'})
    for elem in titles_detail:
        print(elem.getText())
        print("\n")

def get_details(soup):
    raw_soup = soup.find_all('div', {"class":'img'})
    for item in raw_soup:
        temp_soup = item.find('a')
        title.append(temp_soup['title'])
        link.append(temp_soup['href'])

def links(title,link):
    for i in range(len(title)):
        print("%d. %s : https://www10.gogoanime.io%s\n" % (i+1,title[i],link[i]))

def entry():
    question = [
        {
            "type": "input",
            "name": "anime_name",
            "message": "Enter the name of the Anime :"
        }
    ]
    anime_name = prompt(question, style=style)
    search_url = f"https://www10.gogoanime.io//search.html?keyword={anime_name['anime_name']}"
    spinner = Halo(stream=sys.stderr)
    spinner.start("Loading for get data")
    source_code = requests.get(search_url)
    content = source_code.content
    global soup
    soup = BeautifulSoup(content,features="html.parser")
    spinner.stop()
    spinner.succeed("Loading Completed.")
    choice = [
        {
            "type": "list",
            "name": "choice",
            "message": "Do you want Details or Anime Links? (details/links) :",
            "choices": ["details", "links"]
        }
    ]
    choice = prompt(choice, style=style)
    if choice["choice"] == "details":
        spinner = Halo(stream=sys.stderr)
        spinner.start("Loading for get details")
        get_details(soup)
        details(link[0])
        spinner.stop()
        spinner.succeed("Loading Completed.")
    elif choice["choice"] == "links":
        spinner = Halo(stream=sys.stderr)
        spinner.start("Loading for get links")
        get_details(soup)
        links(title,link)
        spinner.stop()
        spinner.succeed("Loading Completed.")
    else:
        print("[-] Enter a valid choice.")

if __name__ == "__main__":
    init(autoreset=True)
    entry()
