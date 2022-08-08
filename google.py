
from requests import get
from lxml.html import fromstring
from socket import gethostbyname
from time import sleep
from random import choice 

sg_search , ag_search = False , False

max_results = 250 # >num

with open('user_agents.txt','r') as uas:
    rua = choice(uas.read().splitlines()) 

# add more User-Agents here 
# uas = [
#   "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
#   "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
#   "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
#   "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
# ]
headers = {
        'User-Agent': rua,
        'Host':'www.google.com',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br'
}
####################################################################################################################
query = str(input("Search for : "))
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

if ag_search :
    num = int(input("\n[?] results per page (max=100): ") or 100)
    start = offset = int(input("[?] scrape from (offset) : ") or 0)

    #SafeSearch
    safe = str(input("[?] enable SafeSearch ? (y/n) : ")).strip().lower()
    safe = 'active' if safe == 'y' else 'incative'
    #OmittedSearch
    omitted = str(input("[?] enable OmittedSearch ? (y/n) : ")).strip().lower()
    filter_ = '1' if omitted == 'y' else '0'
    #PersonalizedSearch
    personalized = str(input("[?] enable PersonalizedSearch ? (y/n) : ")).strip().lower()
    pws = '1' if personalized == 'y' else '0'
    #Country based search
    country = str(input("[?] Search in specific Country ? (y/n) : ") or "n").strip().lower()
    cr = "country"+str(input("[?] Country code [alpha_2] : ")).strip().upper() if country == 'y' else ''

#####################################################################################################################

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

extractors = {1:get_urls,2:get_domains,3:get_ips,4:get_titles,5:get_desc}

print("""
    - [1] urls         [4] titles
    - [2] domains      [5] descriptions
    - [3] IPs          
    """)

choice = int(input("choose : "))

if choice not in extractors : exit()

while start < max_results :
    #print("[¬] page :",page)
    if start!=0:sleep(1.5)
    if sg_search:
        request = get("https://www.google.com/search?q="+query+"&num="+str(num)+"&start="+str(start)
,headers=headers)
    if ag_search :
        request = get("https://www.google.com/search?q="+query+"&num="+str(num)+"&start="+str(start)+"&safe="+safe\
+"&filter="+filter+"&pws="+pws+"&cr="+cr+"&adtest=off",headers=headers)
    if "?continue" in request.url: print("error");exit()
    tree = fromstring(request.text)
    output = extractors[choice]()
    print('\n'.join(output))
    start += num

#footer
print("\n\t*** This is just a BETA version . ***")
print("\t\tAuthor : m3d_y4ss3r ^-^")
