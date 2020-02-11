import requests 
from bs4 import BeautifulSoup   

#Load the page from the web
page = requests.get("https://www.iee.ihu.gr/udg_courses/")
#Transform string to nodes
soup = BeautifulSoup(page.content, 'lxml') 

#Find all the td elements starting with Κωδικός Μαθήματος: 17
table = soup.findAll('td', attrs = {'title': lambda L: L and L.startswith('Κωδικός Μαθήματος: 17')})
#This string will hold the information about the cources
courceString ="-----------------------------------------------"+"\n"
#for each of the above elements
for courceCode in table:
    #Find all it's sibblings through the parent
    cource = courceCode.parent.findAll('td')
    #Do some basic formating and isolate the information
    courceString += "Κωδ " + str(cource[0].find('a').contents[0]) +"\n"
    courceString += "Τίτλος " + str(cource[1].find('a').contents[0]) +"\n"
    courceString += "Είδος " + str(cource[2].contents[0]) +"\n"
    courceString += "Ώρες Θ " + str(cource[3].contents[0]) +"\n"
    #Sometimes Ώρες Θ might be null so change it to 0
    try:
        courceString += "Ώρες Ε " + str(cource[4].contents[0]) +"\n"
    except:
        courceString += "Ώρες Ε 0"  +"\n"
    courceString += "Π.Μ.ECTS " + str(cource[5].contents[0]) +"\n"  
    courceString += "-----------------------------------------------" +"\n"

#Write a cool name for the txt file
file = open("Test1Data.txt","w+")
#Write the information inside the file
file.write("        Classified Information"+"\n" +courceString+"         Classified Information")
#close the file
file.close()