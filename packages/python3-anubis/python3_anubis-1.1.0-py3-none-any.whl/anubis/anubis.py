from json import loads
import requests
import httpx
import re

class AnubisDB(object):
    def __init__(self, domain):
        self.domain = domain 
        self.url = "https://jonlu.ca/anubis/subdomains/{domain}".format(domain=self.domain)
        self.subdomains = []
        self.headers = {}
        
    async def search(self):
        """Search request to perform httpx search"""
        try:
            async with httpx.AsyncClient(verify=False) as client:
                resp = await client.get(self.url)
                if resp.status_code == 200:
                    subs = loads(resp.text)
                    for sub in subs:
                        if(sub not in self.domain):
                            self.subdomains.append(sub)
                else:
                    print("HTTP STATUS in [AnubisDB] Wrong Http status return", resp.status_code)
                    
            return self.subdomains 
        except Exception as e:
            print("ERROR in [AnubisDB] ", e)
            return []
            
    def search_req(self):
        """Search request to perform requests search"""
        try:
            with requests.Session() as client:
                resp = client.get(self.url)
                if resp.status_code == 200:
                    subs = loads(resp.text)
                    for sub in subs:
                        if(sub not in self.domain):
                            self.subdomains.append(sub)
                else:
                    print("HTTP STATUS in [AnubisDB] Wrong Http status return", resp.status_code)
                    
            return self.subdomains 
        except Exception as e:
            print("ERROR in [AnubisDB] ", e)
            return []

class AnubisCRT(AnubisDB):
    """Responsible for finding subdomains from crt"""
    def __init__(self, domain):
        super(AnubisCRT, self).__init__(domain)
        self.domain = domain 
        self.params = (('q', '%.' + self.domain),)
        self.headers = {'authority': 'crt.sh',
             'cache-control': 'max-age=0',
             'upgrade-insecure-requests': '1',
             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36',
             'sec-metadata': 'cause=forced, destination=document, site=cross-site',
             'sec-origin-policy': '0', 'dnt': '1',
             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'accept-encoding': 'gzip, deflate, br',
             'accept-language': 'en-US,en;q=0.9,it;q=0.8,la;q=0.7', }
        
        self.url = "https://crt.sh/"
        self.subdomains = []
        
    async def search(self):
        """Perform a search"""
        try:
            async with httpx.AsyncClient(verify=False) as client:
                resp = await client.get('https://crt.sh/', headers=self.headers, params=self.params)
                scraped = resp.text
                subdomain_finder = re.compile('<TD>(.*\.' + self.domain + ')</TD>')
                links = subdomain_finder.findall(scraped)
                parsed_links = self._clean_links(links)

                for domain in parsed_links:                    
                    if domain.strip() not in self.domain and self.domain.endswith(self.domain):
                        self.subdomains.append(domain.strip())
                    
            return list(set(self.subdomains))
            
        except Exception as e:
            print("ERROR in [AnubisCRT] ", e)
            return []
            
    def search_req(self):
        """Perform a search"""
        try:
            with requests.Session() as client:
                resp =  client.get('https://crt.sh/', headers=self.headers, params=self.params)
                scraped = resp.text
                subdomain_finder = re.compile('<TD>(.*\.' + self.domain + ')</TD>')
                links = subdomain_finder.findall(scraped)
                parsed_links = self._clean_links(links)

                for domain in parsed_links:                    
                    if domain.strip() not in self.domain and self.domain.endswith(self.domain):
                        self.subdomains.append(domain.strip())
                    
            return list(set(self.subdomains))
            
        except Exception as e:
            print("ERROR in [AnubisCRT] ", e)
            return []
    
    def _clean_links(self, links):
        deduped = set()
        for domain in links:
            lower = (domain or '').lower()
            split = lower.split('<br>')
            for full_domain in split:
                deduped.add(full_domain.strip())
        return list(deduped)
  
class AnubisDNSDumpster(AnubisCRT):
    """Searchs dnsdumpster"""
    def __init__(self, domain):
        super(AnubisDNSDumpster, self).__init__(domain)
        self.domain = domain 
        self.headers = {'Pragma': 'no-cache', 'Origin': 'https://dnsdumpster.com',
                 'Accept-Encoding': 'gzip, deflate, br',
                 'Accept-Language': 'en-US,en;q=0.9,it;q=0.8',
                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                 'Content-Type': 'application/x-www-form-urlencoded',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                 'Cache-Control': 'no-cache',
                 'Referer': 'https://dnsdumpster.com/',
                 'Connection': 'keep-alive', 'DNT': '1', }
        self.url="https://dnsdumpster.com/"
        self.csrf_token = None
        self.subdomains = []
        
    async def search(self):
        """Perform a search"""
        try:
            async with httpx.AsyncClient(verify=False) as client:
                csrf_resp = await client.get(self.url, headers=self.headers)
                
                try:
                    self.csrf_token = csrf_resp.headers['Set-Cookie']
                    self.csrf_token = self.csrf_token[10:]
                    self.csrf_token = self.csrf_token.split(";")[0]
                except Exception as e:
                    print("ERROR in [AnubisDNSDumpster] Retrieving CSRF Token for DNSDumpster failed", e)
            
            async with httpx.AsyncClient(verify=False) as client:
                cookies = {'csrftoken': self.csrf_token, }
                data = {'csrfmiddlewaretoken':self.csrf_token, 'targetip':self.domain,'user':'free'}
                resp = await client.post(self.url, headers=self.headers,cookies=cookies, data=data)
                
                try:
                    scraped = resp.text
                    subdomain_finder = re.compile('\">(.*\.' + self.domain + ')<br>')
                    links = subdomain_finder.findall(scraped)
                    for domain in links:
                        if domain.strip() not in self.domain and domain.endswith(self.domain):
                            self.subdomains.append(domain.strip())
                            
                except Exception as e:
                    print("ERROR in [AnubisDNSDumpster] after post", e)
            return list(set(self.subdomains))
            
        except Exception as e:
            print("ERROR in [AnubisDNSDumpster] ", e)
            return []
            
    def search_req(self):
        """Perform a search"""
        try:
            with requests.Session() as client:
                csrf_resp = client.get(self.url, headers=self.headers)
                
                try:
                    self.csrf_token = csrf_resp.headers['Set-Cookie']
                    self.csrf_token = self.csrf_token[10:]
                    self.csrf_token = self.csrf_token.split(";")[0]
                except Exception as e:
                    print("ERROR in [AnubisDNSDumpster] Retrieving CSRF Token for DNSDumpster failed", e)
            
            with requests.Session() as client:
                cookies = {'csrftoken': self.csrf_token, }
                data = {'csrfmiddlewaretoken':self.csrf_token, 'targetip':self.domain,'user':'free'}
                resp = client.post(self.url, headers=self.headers,cookies=cookies, data=data)
                
                try:
                    scraped = resp.text
                    subdomain_finder = re.compile('\">(.*\.' + self.domain + ')<br>')
                    links = subdomain_finder.findall(scraped)
                    for domain in links:
                        if domain.strip() not in self.domain and domain.endswith(self.domain):
                            self.subdomains.append(domain.strip())
                            
                except Exception as e:
                    print("ERROR in [AnubisDNSDumpster] after post", e)
            return list(set(self.subdomains))
            
        except Exception as e:
            print("ERROR in [AnubisDNSDumpster] ", e)
            return []

class AnubisHackerTarget(AnubisDNSDumpster):
    def __init__(self, domain):
        super(AnubisHackerTarget, self).__init__(domain)
        self.domain = domain
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36', }
        self.url="https://api.hackertarget.com/hostsearch/?q={domain}".format(domain=self.domain)
        self.subdomains = []
        
    async def search(self):
        try:
            async with httpx.AsyncClient(verify=False) as client:
                resp = await client.get(self.url,headers=self.headers)
                if(resp.status_code == 200):
                    response = resp.text
                    hostnames = [result.split(",")[0] for result in response.split("\n")]

                    for hostname in hostnames:
                        if (hostname) and (self.domain in hostname):
                            self.subdomains.append(hostname)
            return list(set(self.subdomains))
            
        except Exception as e:
            print("ERROR in [AnubisHackerTarget] ", e)
            return []
            
    def search_req(self):
        try:
            with requests.Session() as client:
                resp = client.get(self.url,headers=self.headers)
                if(resp.status_code == 200):
                    response = resp.text
                    hostnames = [result.split(",")[0] for result in response.split("\n")]

                    for hostname in hostnames:
                        if (hostname) and (self.domain in hostname):
                            self.subdomains.append(hostname)
            return list(set(self.subdomains))
            
        except Exception as e:
            print("ERROR in [AnubisHackerTarget] ", e)
            return []

class Anubis(object):
    """Call other methods to perform search"""
    def __init__(self, domain):
        self.domain = domain 
        
    async def search(self):
        anubisdb = AnubisDB(self.domain)
        anubis_crt = AnubisCRT(self.domain)
        anubis_dns = AnubisDNSDumpster(self.domain)
        anubis_ht = AnubisHackerTarget(self.domain)
        
        print("[AnubisDB] Searching AnubisDB")
        subdomains = await anubisdb.search()
        
        print("[AnubisCRT] Searching AnubisCRT")
        subdomains += await anubis_crt.search()
        
        print("[AnubisDNSDumpster] Searching AnubisDNSDumpster")
        subdomains += await anubis_dns.search()
        
        print("[AnubisHackerTarget] Searching AnubisHackerTarget")
        subdomains += await anubis_ht.search()
        
        # Remove duplicate
        subdomains = list(set(subdomains))
        return subdomains
        
    def search_req(self):
        anubisdb = AnubisDB(self.domain)
        anubis_crt = AnubisCRT(self.domain)
        anubis_dns = AnubisDNSDumpster(self.domain)
        anubis_ht = AnubisHackerTarget(self.domain)
        
        print("[AnubisDB] Searching AnubisDB")
        subdomains = anubisdb.search_req()
        
        print("[AnubisCRT] Searching AnubisCRT")
        subdomains += anubis_crt.search_req()
        
        print("[AnubisDNSDumpster] Searching AnubisDNSDumpster")
        subdomains += anubis_dns.search_req()
        
        print("[AnubisHackerTarget] Searching AnubisHackerTarget")
        subdomains += anubis_ht.search_req()
        
        # Remove duplicate
        subdomains = list(set(subdomains))
        return subdomains
