# Hello There 
######################## Colors #########################
if __import__("sys").stdout.isatty():
    Fore = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m"
    }

    Back = {
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "magenta": "\033[45m",
        "cyan": "\033[46m"
    }

    Clear, Reset, Underline = "\033[K", "\033[0m", "\033[4m" 

else:

    Fore = {
        "red": "Esc[31m",
        "green": "Esc[32m",
        "yellow": "Esc[33m",
        "magenta": "Esc[35m",
        "cyan": "Esc[36m",
        "white": "Esc[37m"
    }

    Back = {
        "red": "Esc[41m",
        "green": "Esc[42m",
        "yellow": "Esc[43m",
        "magenta": "Esc[45m",
        "cyan": "Esc[46m"
    }

    Clear, Reset, Underline = "Esc[K", "Esc[0m", "Esc[4m"
#########################################################
##################### importing PYPS ####################
try:
    from urllib.parse import quote_plus
    from sys import version_info
    from requests import get
    from lxml.html import fromstring
    from socket import gethostbyname
    from time import sleep, gmtime, strftime
    from random import choice
    from signal import signal, SIGINT
except Exception:
    exit(Fore['yellow'] + '[!] install packages : \"pip3 install -r requirements.txt\"')

######## Compatibility Check ####

if version_info.major < 3:
    exit(Fore['red'] + '[X] Runs only with Python 3.x ')


######## Signal Handling #######


def handler(recvsignal, frame):
    exit(Back['yellow'] + Fore['red'] + '\n\n[#] Bye !\n')


signal(SIGINT, handler)

#################################

max_results = 250  # >num
delay = 1.5  # to avoid google temp block

try:
    with open('user_agents.txt', 'r') as uas:
        rua = uas.read().strip().splitlines()
except IndexError:
    print(Fore['red'] + '[!] "user_agents.txt" file, is empty .')
    exit(Fore['yellow'] + '[~] Add some user-agents to the file \n\t(seperated by a line feed).')
except FileNotFoundError:
    print(Fore['magenta'] + '[!!] "user_agents.txt" file , isn\'t in this directory')
    exit(Fore['yellow'] + '[~] Create a new one 0R run the script from master folder')

####################################################################################################################

print(Fore['green'] + '''
          _______      _______. _______     ___      .______        ______  __    __
         /  _____|    /       ||   ____|   /   \     |   _  \      /      ||  |  |  |
        |  |  __     |   (----`|  |__     /  ^  \    |  |_)  |    |  ,----'|  |__|  |
        |  | |_ |     \   \    |   __|   /  /_\  \   |      /     |  |     |   __   |
        |  |__| | .----)   |   |  |____ /  _____  \  |  |\  \----.|  `----.|  |  |  |
         \______| |_______/    |_______/__/     \__\ | _| `._____| \______||__|  |__|

                                                                        by @m3dy4ss3r
''')

query = quote_plus(str(input(Fore['white'] + 'Search for : ')))

print(Fore['yellow'] + '''
        [s] Simple search
        [a] Advanced search
        ''')

sg_search, ag_search = True, False
s_type = str(input(Fore['white'] + '[>] search type : ' + Fore['yellow'])).strip().lower()
if s_type == 'a': sg_search, ag_search = False, True

############################################# Google Search Types ###################################################

if sg_search: num, start = 100, 0

if ag_search:
    num = int(input(Fore['cyan'] + '\n[?] results per page (max=100): ') or 100)
    start = int(input(Fore['cyan'] + '[?] scrape from (offset) : ') or 0)

    # SafeSearch
    safe = str(input(Fore['cyan'] + '[?] enable SafeSearch ? (y/n) : ')).strip().lower()
    safe = 'active' if safe == 'y' else 'incative'
    # OmittedSearch
    omitted = str(input(Fore['cyan'] + '[?] enable OmittedSearch ? (y/n) : ')).strip().lower()
    filter = '1' if omitted == 'y' else '0'
    # PersonalizedSearch
    personalized = str(input(Fore['cyan'] + '[?] enable PersonalizedSearch ? (y/n) : ')).strip().lower()
    pws = '1' if personalized == 'y' else '0'
    # Country based search
    country = str(input(Fore['cyan'] + '[?] Search in specific Country ? (y/n) : ') or 'n').strip().lower()
    cr = 'country' + str(input(Fore['cyan'] + '[?] Country code [alpha_2] : ')).strip().upper() if country == 'y' else ''
    # Internationalization
    ie = str(input(Fore['cyan'] + '[?] Input  Char Encoding (Default = UTF8) : ') or 'utf8').strip().lower()
    oe = str(input(Fore['cyan'] + '[?] Output Char Encoding (Default = UTF8) : ') or 'utf8').strip().lower()

#####################################################################################################################

############################################# Google Extractors #####################################################


def get_urls():
    urls = tree.xpath('//div[contains(@class,"g")]/div/div/div/a/@href[starts-with(.,"http")]')
    return urls


def get_domains():
    domains = [url.split('/')[2] for url in get_urls()]
    return list(dict.fromkeys(domains))      # deduping needed *-*


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

extractors = {
    1: ['URLs', get_urls],
    2: ['Domains', get_domains],
    3: ['IPs', get_ips],
    4: ['Titles', get_titles],
    5: ['Description', get_desc]
}

print(Fore['cyan'] + '''
    - [1] urls         - [4] titles
    - [2] domains      - [5] descriptions
    - [3] IPs
    ''')

option = int(input(Fore['white'] + '[>] data type : ' + Fore['cyan']))

if option not in extractors:
    exit(Fore['red'] + '[!] For now , available options are :', '/'.join(str(key) for key in extractors))

print(Fore['green'] + '\n[+] Loading {}...\n'.format(extractors[option][0]))

page, html_pages = 1, ''

while start < max_results:

    print(Back['red'] + Fore['white'] + '[:] Waiting ' + Clear + '{} seconds'.format(delay), end='\r')
    sleep(delay)
    if sg_search:
        g_url = 'https://www.google.com/search?q=' + query + '&num=' + str(num) + '&start=' + str(start)
    if ag_search:
        g_url = 'https://www.google.com/search?q=' + query + '&num=' + str(num) + '&start=' + str(start) + '&safe=' + safe + '&filter=' + filter + '&pws=' + pws + '&cr=' + cr + '&ie=' + ie + '&oe=' + oe + '&adtest=off'
    headers = {
        'User-Agent': choice(rua),
        'Host': 'www.google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    print(Back['red'] + Fore['white'] + '[¬] Fetching page : ' + Clear + Reset, page, end='\r')
    request = get(g_url, headers=headers)
    if '?continue' in request.url:
        # print(request.headers)
        print(Back['magenta'] + Fore['white'] + '[X] Google Temporary Block :(')
        exit(Back['magenta'] + Fore['white'] + '[!] Try again later.')
    html_pages += request.text
    start += num
    page += 1

tree = fromstring(html_pages)
results = Fore['green'] + '\n'.join(extractors[option][1]())
print(results, '\n\n|Total :', len(results.split('\n')))

## Auto-Save ##
auto_save = 'Results-{}({}).txt'.format(extractors[option][0], strftime('%Y-%m-%d_%H:%M:%S', gmtime()))
try:
    with open("auto_saved/" + auto_save, 'w') as out:
        out.write(results)
except Exception:    #skip auto-saving if folder isn't there
    pass
#################

## Custom-Save ##
if str(input(Fore['white'] + '\n[>] save output ? (y/n) : ' or 'n')).strip().lower() == 'y':
    custom_save = str(input('\t[>] save as : '))
    try:
        with open(custom_save, 'w') as out:
            out.write(results)
        print(Fore['yellow'] + '\n[+] Saved to "{}"'.format(custom_save))
    except Exception as error:
        print(error)
#################

print(Fore['magenta'] + Underline + '\n\t *** This is just a BETA version ***')
print('\t\t Author : m3d_y4ss3r ^-^')
