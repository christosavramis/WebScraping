# ------------Goal------------------
# Συλλογή όλων των link της wikipedia
# Την εγγραφή των δεδομένων σε ένα txt αρχείο
# Μην υπάρχουν διπλότυπα links

from multiprocessing import Pool
from bs4 import BeautifulSoup
import random
import time
import requests
from collections import deque 

def random_starting_url():
    return "https://en.wikipedia.org/wiki/Mia_Khalifa"

def handle_local_links(link):
    if link.has_attr('href'):
        #get the url as string
        url = str(link['href'])

        #Canonical Wikipedia article URLs
        if url.startswith("/wiki/"):
            url = 'https://en.wikipedia.org' + url

        #Permanent links to old versions of pages  
        elif url.startswith("/w/"):
            url = 'https://en.wikipedia.org' + url
        else:
            url = ''     
        return url
    else:
        return ''


def get_links(url):
    wait = random.random()*5
    print(f"start searching links from {url} with {wait} delay")
    time.sleep(wait)
    #User agent header
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    try:
        page = requests.get(url,headers=header)
        #Parse the html
        soup = BeautifulSoup(page.content,'html.parser')

        links = []
        
        #Find all a links
        links = soup.find_all('a')
        #removes duplicates
        links = list(dict.fromkeys(links))
        #manipulates urls for requests
        links = list(handle_local_links(link) for link in links)
        #removes empty urls
        links = list(link for link in links if link !='')
        #turn them to askii
        #links = [str(link.encode("ascii")) for link in links] # it adds a b character as key
        print(f"finished searching links from {url}")

        return links
    except TypeError as e:
        # it has no links
        print(f"{e} -> {url}")
        return []
    
    except IndexError as e:
        #we didint find any usefull links
        print(f"{e} -> {url}")
        return []
    
    except AttributeError as e:
        print(f"{e} -> {url}")
        #Likely got none for links so we are throwing this
        return []
    except Exception as e:
        #in case something else fails
        print(f"{e} -> {url}")
        return []

#writes the url to the file
def writeUrlTofile(data):
        #Open file in append mode
        with open('./url.txt','w') as file:
                #Loop through the info list
                for dat in data:
                    try:
                        file.write(dat)
                        file.write('\n')
                    except:
                            print("cant encode a character")
                            return 

def main(how_many):
    data = []
    rootUrl = [random_starting_url()]
    while len(data) < how_many:
        print(f"{len(data)}/{how_many}")

        #multiprossecing module 
        p = Pool()
        data = p.map(get_links, rootUrl)
        p.close()

        #list of lists of urls to list of urls
        data = list(url for url_list in data for url in url_list)

        #removes duplicates
        data = list(dict.fromkeys(data))
        
        #if we receive no urls break
        if len(data) == 0 :
            print()
            print("No links")
            print()
            break
        #else get the next root url
        elif len(data) < how_many:
            #get the next root urls based on how many urls we are missing 
            rootUrl = list(dat for num,dat in enumerate(data) if num + len(data) < how_many)
        else:
            #remove excess data
            data = list(dat for num,dat in enumerate(data) if num  < how_many)


    writeUrlTofile(data)


if __name__ == '__main__':
    main(200)

