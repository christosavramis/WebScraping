'''
Task: Find all the info from the seventh semester
'''

#Imports
import time
import requests
from bs4 import BeautifulSoup

# Print iterations progress https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


#User agent header
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

#Delay between page requests
request_delay = 1

def ask2():

        #Create an empty list
        urls = list()
        
        #Send the request
        time.sleep(request_delay)
        page = requests.get('https://el.wikipedia.org/wiki/%CE%94%CE%B9%CE%B5%CE%B8%CE%BD%CE%AD%CF%82_%CE%A0%CE%B1%CE%BD%CE%B5%CF%80%CE%B9%CF%83%CF%84%CE%AE%CE%BC%CE%B9%CE%BF_%CF%84%CE%B7%CF%82_%CE%95%CE%BB%CE%BB%CE%AC%CE%B4%CE%BF%CF%82',headers=header)
        
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
                                url = "https://el.m.wikipedia.org" + url

                        #urls interact with api      
                        elif url.startswith("/w/"):
                                url = "https://el.m.wikipedia.org" + url

                        #urls that like double slashes dont work :P
                        #elif url.startswith("//"):
                        #        url = url.replace("//","")

                        #url is a section or its not modified by the above        
                        else:
                                #print(url)
                                #continue so the not usabble url wont get requested
                                continue 

                        #when the url is ready append it
                        urls.append(url)
        
        #if we have more than zero valid urls get their titles
        if len(urls) > 0:
                # (1 seconds for the request to complete + the request_delay) * urls
                seconds = len(urls) * (request_delay + 1)
                print("Approximated delay " + str(seconds) )
                getTheTitles(urls, request_delay)

def getTheTitles(urls, request_delay):
        #Create an empty list
        infos = list()

        #Return the number of items in the list
        l = len(urls)

        # Initial call to print 0% progress
        printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        for i,url in enumerate(urls):

                #Send the request
                time.sleep(request_delay)
                try:
                        page = requests.get(url, headers=header)
                except:
                        #if the url trigger an exception report it and go for the next url or 404 or gets cock blocked if u are a bot
                        print("cant request the page " + url)
                        continue
                        
                #Parse the html
                soup = BeautifulSoup(page.content,'html.parser')
                title = soup.find('title')

                try:
                        #Find the Title
                        title = soup.find('title').text
                except:
                        # title is null skip it
                        continue

                #Create empty dict
                data = dict()
                
                #fill the dictionary and append it to the list
                data['title'] = title
                data['url'] = url
                infos.append(data)

                #print(url)
                # Update Progress Bar
                printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

        print("writing to file ... ")
        #Write the dictionary to the file
        writeToFile(infos)
             
def writeToFile(infos):
        #Open file in append mode
        with open('./info.txt','a') as file:
                #Loop through the info list
                for data in infos:
                        try:
                                #Loop through the dictionary
                                for key,val in data.items():
                                        #Write values to file
                                        file.write(f"{key}:{val} ")
                                file.write('\n\n')
                        except:
                                print("cant encode a character")
                                continue                       


if __name__ == "__main__":
        ask2()


