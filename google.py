
from requests import get
from lxml.html import fromstring
from socket import gethostbyname
from time import sleep

query = str(input("Search for : "))
sg_search , ag_search = False , False
max_results = 250

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Host':'www.google.com',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br'
}
####################################################################################################################
print("""
        [s] Simple search
        [a] Advanced search
        """)
s_type = str(input("search type : ")).strip().lower()
if s_type == 'a':
    ag_search = True
else:
    sg_search = True
############################################# Google Search Types ###################################################

if sg_search:
    num,start = 100,0
    url = "https://www.google.com/search?q="+query+"&num="+str(num)+"&start="+str(start)

if ag_search :
    num = int(input("\n[?] results per page (max=100): ") or 100)
    start = offset = int(input("[?] scrape from (offset) : ") or 0)

    #SafeSearch
    safe = str(input("[?] enable SafeSearch ? (y/n) : ")).strip().lower()
    safe = 'active' if safe == 'y' else 'incative'
    #OmittedSearch
    omitted = str(input("[?] enable OmittedSearch ? (y/n) : ")).strip().lower()
    filter = '1' if omitted == 'y' else '0'
    #PersonalizedSearch
    personalized = str(input("[?] enable PersonalizedSearch ? (y/n) : ")).strip().lower()
    pws = '1' if personalized == 'y' else '0'
    #Country based search
    country = str(input("[?] Search in specific Country ? (y/n) : ") or "n").strip().lower()
    cr = "country"+str(input("[?] Country code [alpha_2] : ")).strip().upper() if country == 'y' else ''

    url = "https://www.google.com/search?q="+query+"&num="+num+"&start="+start+"&safe="+safe\
+"&filter="+filter+"&pws="+pws+"&cr="+cr+"&adtest=off"

#####################################################################################################################
print(url);input()
#while start < max_results :
if start!=0:sleep(1.5)
request = get(url,headers=headers)
if "?continue" in request.url: print("error");exit()
tree = fromstring(request.text)
#start += num

############################################# Google Extractors #####################################################

def get_urls():
    urls = tree.xpath("//div[contains(@class,'g')]/div/div/div/a/@href")
    return urls

def get_domains():
    domains = [url.split('/')[2] for url in get_urls()]
    return domains

def get_ips():
    ips = [gethostbyname(domain.split(":")[0]) for domain in get_domains()]
    return ips

def get_titles():
    titles = tree.xpath("//div[contains(@class,'g')]/div/div/div/a/h3/text()")
    return titles

def get_desc():
    description = tree.xpath("//div[contains(@class,'g')]/div/div[2]/div/span/text()")
    return description

#####################################################################################################################

extracters = {1:get_urls,2:get_domains,3:get_ips,4:get_titles,5:get_desc}

print("""
    - [1] urls         [4] titles
    - [2] domains      [5] descriptions
    - [3] IPs          [6] .
    """)

choice = int(input("choose : "))

if choice not in extracters : exit()

output = extracters[choice]()
print("\n".join(output))
print("\n|Total : ",len(output))

#footer
print("\n\t*** This is just a BETA version . ***")
print("\t\tAuthor : m3d_y4ss3r ^-^")
