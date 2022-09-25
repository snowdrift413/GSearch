
## This is a tool to scrap many types of data from Google Search .

### Scrapped Data :  
  - URLs 
  - Domains
  - IPv4 adresses
  - Titles 
  - Descriptions


### Modes :

`Simple Search` = number of results is set to max (100) and the starting offset is set to (0) 

`Advanced Search` = includes more filters + manual settings 

#### Filters :

SafeSearch = Hide/Show explicit content results
    
OmittedSearch = Hide/Show entries very similar to the results already displayed
    
Personalisedsearch = Hides/Show personal results
  
Country = search by country (ISO 3166-1 alpha-2 code)

Internationalization = I/O Encoding 
   
AdTest (default : <kbd>off</kbd> ) = terminates connection to AdWords database
   
   
> **Warning** Maximum results of a google search is always < 250 , so don't change it (you won't get more results) . 


#### TODO 
- [X] ~Bypass Rate Limiting (delayed requests)~
- [X] ~User-Agent Randomization~
- [ ] Add **all** Parameters to Advanced Mode
- [ ] Query URI Encoding
- [ ] Proxy (HTTP[S]/Socks4,5) / Tor 
- [ ] Rebuild with Args
