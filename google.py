from requests import get
from lxml.html import fromstring
from socket import gethostbyname
from time import sleep
from random import choice 
from signal import signal, SIGINT

######## Signal Handling #######
def handler(recvsignal, frame):
    exit('\n\t[#] Bye !')
signal(SIGINT, handler)
#################################

sg_search , ag_search = False , False

max_results = 250 # >num
delay = 1.5 #to avoid google temp block 

try :
    with open('user_agents.txt','r') as uas:
        rua = choice(uas.read().strip().splitlines()) 
except IndexError:
    print('[!] "user_agents.txt" file, is empty .')
    exit( '[~] Add some user-agents to the file \n\t(seperated by a line feed).')
except FileNotFoundError: 
    print('[!!] "user_agents.txt" file , isn\'t in this directory') 
    exit('[~] Create a new one 0R run the script from master folder')
    
engine = 'https://www.google.com/search?q='  
headers = {
        'User-Agent': rua,
        'Host':'www.google.com',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br'
}
####################################################################################################################
query = str(input('Search for : '))
print('''
        [s] Simple search
        [a] Advanced search
        ''')

s_type = str(input('search type : ')).strip().lower()

if s_type == 'a':
    ag_search = True
else:
    sg_search = True
############################################# Google Search Types ###################################################

if sg_search : num,start = 100,0

if ag_search :
    num = int(input('\n[?] results per page (max=100): ') or 100)
    start = int(input('[?] scrape from (offset) : ') or 0)

    #SafeSearch
    safe = str(input('[?] enable SafeSearch ? (y/n) : ')).strip().lower()
    safe = 'active' if safe == 'y' else 'incative'
    #OmittedSearch
    omitted = str(input('[?] enable OmittedSearch ? (y/n) : ')).strip().lower()
    filter_ = '1' if omitted == 'y' else '0'
    #PersonalizedSearch
    personalized = str(input('[?] enable PersonalizedSearch ? (y/n) : ')).strip().lower()
    pws = '1' if personalized == 'y' else '0'
    #Country based search
    country = str(input('[?] Search in specific Country ? (y/n) : ') or 'n').strip().lower()
    cr = 'country'+str(input('[?] Country code [alpha_2] : ')).strip().upper() if country == 'y' else ''

#####################################################################################################################

############################################# Google Extractors #####################################################

def get_urls():
    urls = tree.xpath('//div[contains(@class,"g")]/div/div/div/a/@href')
    return urls

def get_domains():
    domains = [url.split('/')[2] for url in get_urls()]
    return domains

def get_ips():
    ips = [gethostbyname(domain.split(':')[0]) for domain in get_domains()]
    return ips

def get_titles():
    titles = tree.xpath('//div[contains(@class,"g")]/div/div/div/a/h3/text()')
    return titles

def get_desc():
    description = tree.xpath('//div[contains(@class,"g")]/div/div[2]/div/span/text()')
    return description

#####################################################################################################################

extractors = {1:['URLs',get_urls],2:['Domains',get_domains],3:['IPs',get_ips],4:['Titles',get_titles],5:['Description',get_desc]}

print('''
    - [1] urls         - [4] titles
    - [2] domains      - [5] descriptions
    - [3] IPs          
    ''')

choice = int(input('choose : '))

if choice not in extractors : 
    exit('[!] For now , available choices are :','/'.join(str(key) for key in extractors))

print('[+] Loading {}...'.format(extractors[choice][0]))

page , results = 0 , ''
while start < max_results :
    print('[¬] Fetching page : ',page+1)
    sleep(delay)
    if sg_search:
        request = get(engine+query+'&num='+str(num)+'&start='+str(start),headers=headers)
    if ag_search :
        request = get(engine+query+'&num='+str(num)+'&start='+str(start)+'&safe='+safe
                      +'&filter='+filter_+'&pws='+pws+'&cr='+cr+'&adtest=off',headers=headers)
    if '?continue' in request.url: 
        print('[X] Google Temporary Block :(')
        exit('[!] Try again later.')
    tree = fromstring(request.text)
    results += '\n'.join(extractors[choice][1]())
    start += num

print(results)

if str(input('\n[>] save output ? (y/n) : 'or 'n')).strip().lower() =='y':
   save_file = 'Results-{}({}).txt'.format(query.strip(),extractors[choice][0])
   with open(save_file,'w') as out:
        out.write(results)
    print('[+] Saved to "{}"'.format(save_file))
#footer
print('\n\t*** This is just a BETA version . ***')
print('\t\tAuthor : m3d_y4ss3r ^-^')
