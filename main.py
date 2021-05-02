from PyInquirer import prompt
from colorama import init, Fore
from halo import Halo
from styles import style

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(f'{Fore.RED}Some modules are not installed! Installing them with this command.\n{Fore.GREEN}pip install -r requirement.txt')


def links(title,link):
    for i in range(len(title)):
        print("%d. %s : https://www10.gogoanime.io%s\n" % (i+1,title[i],link[i]))

def entry():
    question = [
        {
            "type": "input",
            "name": "anime_name",
            "message": "[+] Enter the name of the Anime :"
        }
    ]
    anime_name = prompt(question, style=style)
    search_url = f"https://www10.gogoanime.io//search.html?keyword={anime_name['anime_name']}"
    source_code = requests.get(search_url)
    content = source_code.content
    global soup
    soup = BeautifulSoup(content,features="html.parser")
    choice = [
        {
            "type": "list",
            "name": "choice",
            "message": "[+] Do you want Details or Anime Links? (details/links) :",
            "choices": ["details", "links"]
        }
    ]
    choice = prompt(choice, style=style)
    if choice["choice"] == "details":
        get_details(soup)
        details(link[0])
    elif choice["choice"] == "links":
        get_details(soup)
        links(title,link)
    else:
        print("[-] Enter a valid choice.")

if __name__ == "__main__":
    init(autoreset=True)
    # main()
