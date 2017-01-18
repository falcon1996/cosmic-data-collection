import datetime
from datetime import date
import requests
from bs4 import BeautifulSoup
import urllib

now = datetime.datetime.now()
current_year = now.year
current_month = now.month
current_day = now.day

earth_day_time = 23.9333
mars_day_time = 24.6500
pic_num = 1

#######################################################################
#Conversion of days to sols

d1 = date(2012,8,6)
d2 = date(current_year,current_month,current_day)

earth_days = abs(d2-d1).days

curiosity_sol = round((earth_day_time * earth_days) / mars_day_time)

########################################################################

#Specifying camera to be used

# FHAZ	              Front Hazard Avoidance Camera
# RHAZ	              Rear Hazard Avoidance Camera
# CHEMCAM	      Chemistry and Camera Complex
# MAHLI	               Mars Hand Lens Imager
# MARDI	               Mars Descent Imager
# NAVCAM	       Navigation Camera
# PANCAM	       Panoramic Camera
# MINITES	       Miniature Thermal Emission Spectrometer (Mini-TES)
# default:             all

#Specify rover to be used 

#curiosity
#opportunity
#spirit

cam_selected = "fhaz"                  #enter camera you want to use, fhaz is selected as default.
DEMO_KEY = ""                          #enter demo key.
rover_selected = "curiosity"           #enter rover you want to use, curiosity is selected as default.

link = "https://api.nasa.gov/mars-photos/api/v1/rovers/"+rover_selected+"/photos?sol="+str(curiosity_sol)+"&camera="+\
       cam_selected+"&api_key="+DEMO_KEY

def get_page(url):
    try:
        r = requests.get(url)
        soup = str(BeautifulSoup(r.content))
        return soup
    except:
        return ""


def get_next_target(page):
    start_link = page.find('c":')
    if start_link == -1:
        return None, 0
    else:
        start_quote = page.find('"', start_link+2)
        end_quote = page.find('"', start_quote + 1)
        url = page[start_quote + 1:end_quote]
        return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos: ]
        else:
            break
    return links

content = get_page(link)

print content

outlinks_of_images = get_all_links(content)
print outlinks_of_images


for image in outlinks_of_images:
    name = str(pic_num)+".jpg"
    urllib.urlretrieve(image, name)
    pic_num+=1

########################################################################

url = "https://geoiptool.com"

r = requests.get(url)
soup = str(BeautifulSoup(r.content))

start_quote = soup.find('Latitude:</span>')

end_quote = soup.find('</span>', start_quote +10)

latitude =  str(soup[start_quote+23 : end_quote])


start_quote = soup.find('Longitude:</span>')

end_quote = soup.find('</span>', start_quote+20)

longitude =  str(soup[start_quote+24 : end_quote])



link_earth = "https://api.nasa.gov/planetary/earth/imagery?lon="+str(longitude)+"&lat="+str(latitude)+"&date="+str(current_year)+"-"+str(current_month)+"-"+str(current_day)+\
       "&cloud_score=True&api_key="+str(DEMO_KEY)

print"*********************"
print link_earth
print"********************"

my_earth = requests.get(link_earth)
data_earth = str(my_earth.content)

print data_earth

start_link = data_earth.find('url": ')
start_quote = data_earth.find('"', start_link+4)

end_quote = data_earth.find('"', start_quote+1)

result = data_earth[start_quote + 1:end_quote]

print"****************************"
print result
print"****************************"

name = "earth_today.jpg"
urllib.urlretrieve(result, name)



