# ------------Goal------------------
# Συλλογή όλων των link της wikipedia
# Την εγγραφή των δεδομένων σε ένα txt αρχείο
# Μην υπάρχουν διπλότυπα links

#Imports
import time
import requests
from collections import deque 
from bs4 import BeautifulSoup


#writes the url to the file
def writeUrlTofile(data):
        #Open file in append mode
        with open('./url.txt','a') as file:
                #Loop through the info list
                for dat in data:
                    try:
                        file.write(dat)
                        file.write('\n')
                    except:
                            print("cant encode a character")
                            return 

def extractUrls(rootUrl):
    #User agent header
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    #Create an empty list
    urls = list()

    #if we cant reach the site dont include it
    try:
        #Send the request
        page = requests.get(rootUrl,headers=header)
    except:
        return 1 # error

    #find the urlDomain
    urlDomain = rootUrl.replace("https://","")
    urlDomain = "https://" + urlDomain.partition("/")[0]
        
    #Parse the html
    soup = BeautifulSoup(page.content,'html.parser')

    #Find all a links
    links = soup.find_all('a')

    #For each link find the appropriate url
    for link in links:
            if link.has_attr('href'):
                #get the url as string
                url = str(link['href'])

                #Canonical Wikipedia article URLs
                if url.startswith("/wiki/"):
                    url = urlDomain + url

                #Permanent links to old versions of pages  
                elif url.startswith("/w/"):
                    url = urlDomain + url     
                else:
                    continue 

                urls.append(url)

    #Create a dictionary, using the List items as keys. This will automatically remove any duplicates because dictionaries cannot have duplicate keys.
    urls = list( dict.fromkeys(urls))
    return urls    

def main(seedUrl, urlCounter):
    
    #holds crawled websites
    crawledUrlList = []

    # returns the next url we are going to search
    urlQueue = deque()

    # Initial call to print 0% progress
    pI = 0
    while len(crawledUrlList) < urlCounter + 1:
        print(f"iteration [{pI}]")
        print(f"Queue status : {len(urlQueue)}/{urlCounter}")
        print(f"Crawled status : {len(crawledUrlList)}/{urlCounter}")
        pI+=1

        time.sleep(2)
        newUrls = extractUrls(seedUrl)

        # if the url cant be reached
        if newUrls == 1 :
            #if we got no more urls to search end the loop
            if len(urlQueue) == 0:
                print(f"we couldnt find {urlCounter} urls")
                break
            #else get the next url from the list and continue to the next iteration
            else:
                seedUrl = urlQueue.popleft()
        else:
            #add the tested seed url in the crawledList
            crawledUrlList.append(seedUrl)


            #removes all coppies of a url in the newUrls
            for crawledUrl in crawledUrlList:
                while crawledUrl in newUrls:
                    newUrls.remove(crawledUrl)

            #fill the queue if needed
            for newUrl in newUrls:
                if len(urlQueue) < urlCounter:
                    urlQueue.append(newUrl)
                else:
                    break
            seedUrl = urlQueue.popleft()
    return crawledUrlList



if __name__ == "__main__":
    data = main("https://en.wikipedia.org/wiki/Mia_Khalifa",200)
    print("write to file")
    writeUrlTofile(data)

