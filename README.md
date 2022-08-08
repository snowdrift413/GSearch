
This is a python3 script to scrap data from google search engine .

Data thaht can be scrapped : 
  - URLs 
  - Domains
  - IPs (IPv4 adresses)
  - Titles 
  - Description
  
The script have two modes : _**Advanced Search**_  and _**Simple Search**_

Simple Search = in this mode the number of results is set to max (100) and the starting offset is set to 0 

Advanced Search = this modes is more professional as it includes more filters and more parameters which affect the output result 

- Filters :
    
    SafeSearch = Hide/Show explicit content results
    
    OmittedSearch = Hide/Show entries very similar to the results already displayed
    
    Personalisedsearch = Hides/Show personal results
    
    Country = search by country (ISO 3166-1 alpha-2 code !)
   
   and AdTest is set to `off` terminates connection to AdWords database
   
   
> Maximum Results of a google search is always < 250 so in a simple search mode , just 3 requests will get you literally ALL results , and if you go advanced you'll get efficient results especially if you are dorking ;)
