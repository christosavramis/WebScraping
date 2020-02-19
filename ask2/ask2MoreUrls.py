#Imports
import time
import requests
from bs4 import BeautifulSoup




def main(rootUrl):
    sleep_rate = 2
    while 1:
        #create a url List
        time.sleep(sleep_rate)
        urls = getTheUrls(rootUrl)

        #loop through the urls
        for url in urls:
            #wait before requestign
            time.sleep(sleep_rate)
            data = getTheData(url)
            print(data)

            #save info in the file
            writeInfoToFile(data)

            #save url to the file
            writeUrlTofile(data)

        #pop the top url
        rootUrl = popUrlFromFile()
        print(rootUrl)
        #if the file returns no url then break
        if rootUrl == "" or rootUrl == None:
            break


#pops the first url in the file
def popUrlFromFile():
    with open('./url.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('./url.txt', 'w') as fout:
        fout.writelines(data[1:])
    return data[0]


#writes the url to the file
def writeUrlTofile(data):
        #Open file in append mode
        with open('./url.txt','a') as file:
                #Loop through the info list
                
                        try:
                            file.write(data['url'])
                            file.write('\n')
                        except:
                                print("cant encode a character")
                                return 

#writes the data to the file
def writeInfoToFile(data):
        print("hello")
        #Open file in append mode
        with open('./data.txt','a') as file:
                #Loop through the info list
                        try:
                                #Loop through the dictionary
                                for key,val in data.items():
                                        #Write values to file
                                        file.write(f"{key}:{val} ")
                                file.write('\n\n')
                        except:
                                print("cant encode a character")
                                return                

def getTheUrls(rootUrl):
    #User agent header
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    #Create an empty list
    urls = list()
        
    #Send the request
    page = requests.get(rootUrl,headers=header)
         
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
                        
                        #urls that work without adding prefix
                        if url[0] == "h" or url[0] == "w":
                                #Ingore the if statement - skip to append
                                pass
                        #urls within the domain
                        elif url.startswith("/wiki/"):
                                url = urlDomain + url

                        #urls interact with api      
                        elif url.startswith("/w/"):
                                url = urlDomain + url

                        #url is a section or its not modified by the above        
                        else:
                                #print(url)
                                #continue so the not usabble url wont get requested
                                continue 

                        #when the url is ready append it
                        urls.append(url)
    return urls    
        



def getTheData(url):
    
    #User agent header
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    try:
        page = requests.get(url, headers=header)
    except:
        #if the url trigger an exception report it and go for the next url or 404 or gets cock blocked if u are a bot
        print("cant request the page " + url)
        return
                        
    #Parse the html
    soup = BeautifulSoup(page.content,'html.parser')
    title = soup.find('title')

    try:
        #Find the Title
        title = soup.find('title').text
    except:
        # title is null skip it
        return None

    #Create empty dict
    data = dict()
                
    #fill the dictionary and append it to the list
    data['title'] = title
    data['url'] = url

    #save the title and the url
    return data

if __name__ == "__main__":
        main("https://en.wikipedia.org/wiki/International_Hellenic_University")

