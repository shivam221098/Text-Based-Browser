import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

pages_stack = []


def pages(url):
    r = requests.get(url)
    return r.text


def link_highlighter(content):
    colored = ""
    new_data = ""
    for word in content:
        if word.name == "a":
            colored += word.get_text() + " "
    for word in content:
        if word.get_text() in colored:
            new_data += Fore.BLUE + word.get_text() + " "
        else:
            new_data += word.get_text() + " "
        new_data += Style.RESET_ALL
    return new_data


def main_():

    try:
        while True:
            page_data = ""
            url = input()
            if url == "exit":
                exit(0)
            elif url == "back":
                try:
                    pages_stack.pop()
                    print(pages_stack.pop())
                except IndexError:
                    pass
            elif "." in url:
                if "https://" in url:
                    data = pages(url)
                else:
                    data = pages("https://" + url)
                soup = BeautifulSoup(data, "html.parser")
                content = soup.find_all(["p", "a"])
                page_data = link_highlighter(content)
                print(page_data)
                pages_stack.append(page_data)
                if ".com" in url:
                    with open("{}/{}".format(args[1], url.rstrip(".com")), "w", encoding="utf-8") as f:
                        f.write(page_data)
                elif ".org" in url:
                    with open("{}/{}".format(args[1], url.rstrip(".org")), "w", encoding="utf-8") as f:
                        f.write(page_data)
            else:
                with open("{}/{}".format(args[1], url), "r", encoding="utf-8") as file:
                    print(file.read())
    except FileNotFoundError:
        print("Error: Incorrect url")


args = sys.argv
try:
    os.mkdir(args[1])
    main_()
except FileExistsError:
    print("File already exists")
    main_()
