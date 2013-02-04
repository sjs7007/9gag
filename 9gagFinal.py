import os
import urllib2

number=1
nextLink="http://9gag.com/"
pageNumber=1

def FindLinks(): #required for getting page source of base page that is then passed to FindLinks2
 os.system("echo Start|cat>>log")
 base_link="http://9gag.com/"
 base_contents=urllib2.urlopen(base_link).read()
 FindLinks2(base_contents)


def FindLinks2(base_contents):  #find links like http://9gag.com/gag/6482858 that can be passed to the Extract Image Function
 global number
 initial=0
 breakval=0
 for i in range (0,100): #keep on finding links until the next link is not equal to first one
  start_link=base_contents.find('data-url="',initial)+10
  end_link=base_contents.find('" data-text',start_link)
  link=base_contents[start_link:end_link]
  initial=end_link
  if (i==0):
   breakval=initial
  if (initial==breakval and i!=0):
   print "break!"
   break
  temp=str(number)+". "+link
  print temp
  os.system("echo %s|cat>>log" %temp)
  ExtractImage(link)
  number=number+1

def ExtractImage(inputUrl): #Will extract image from a page like http://9gag.com/gag/6482858
 Page_contents=urllib2.urlopen(inputUrl).read()
 image_link_start=Page_contents.find('<img src=')
 image_link_end=Page_contents.find('"/>',image_link_start)
 temp=Page_contents[image_link_start:image_link_end]
 start_actual_link=temp.find("//")+2
 end_actual_link=temp.find('.jpg',start_actual_link)+4
 actual_link=temp[start_actual_link:end_actual_link]
 
 title_of_image=FindTitle(temp)
 print title_of_image
 os.system("echo %s|cat>>log" %title_of_image)
 print
 print
 os.system("echo|cat>>log")
 os.system("echo|cat>>log")
 os.system("wget %s >/dev/null 2>&1" %actual_link)
 Rename(actual_link,FindTitle(temp))

def FindTitle(temp): #Find title of image to be downloaded
 start_title_of_image=temp.find('alt="')+5
 end_title_of_image=temp.find('"', start_title_of_image)
 title_of_image=temp[start_title_of_image:end_title_of_image]
 return title_of_image

def Rename(actual_link,toName): #Give the downloaded file a more meaningful name
 fromName=actual_link[actual_link.find("photo/")+6:]
 toName=toName+".jpg"
 #however if there are space in between it will lead to problem hence replace all spaces in toName to '_'
 toName=toName.replace(' ','_')
 os.system("mv %s %s" %(fromName,toName))

def FindLinks3(base_link): #find page source of next hot page and return it 
 global nextLink
 base_contents=urllib2.urlopen(base_link).read()
 start_link=base_contents.find("hot?id")
 end_link=base_contents.find('"',start_link)
 link="http://9gag.com/"+base_contents[start_link:end_link]
 if(nextLink==link):
  start_link=base_contents.find("hot?id",end_link)
  end_link=base_contents.find('"',start_link)
  link="http://9gag.com/"+base_contents[start_link:end_link]  

 nextLink=link
 print link
 pageSource=urllib2.urlopen(link).read()
 return pageSource

os.system("clear")
n=input("Enter no. of pages : ")
nextPageSource=urllib2.urlopen("http://9gag.com/").read()
for i in range (0,n):
 if(i==0):
  os.system("clear")
  os.system("echo Page Number : %d |cat>>log" %pageNumber)
  FindLinks()
 else:
  os.system("clear")
  os.system("echo Page Number : %d |cat>>log" %pageNumber)
  nextPageSource=FindLinks3(nextLink)
  FindLinks2(nextPageSource)
 pageNumber=pageNumber+1

number=number-1 
os.system("echo End|cat>>log")
os.system("echo Total Images downloaded : %d | cat>>log" %number)
os.system("echo ------------------------------------------|cat>>log")
os.system("echo|cat")

