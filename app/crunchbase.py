import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


async def get_overview_html(mylink):
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        
        
        page = await browser.new_page()
        
        # await page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"})
        
        await page.goto(mylink)
        
        html=await page.inner_html('row-card.overview-card')
        
        await browser.close()
        return html
    
async def get_data(mylink):
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        
        
        page = await browser.new_page()
        
        # await page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"})
        
        await page.goto(mylink)

        overview=await page.inner_html('row-card.overview-card')

        name=await page.inner_html('h1.profile-name')
        html=await page.inner_html('span.description')
        
        # Getting the Adress
        adresshtml=await page.inner_html('identifier-multi-formatter.ng-star-inserted')
        soup=BeautifulSoup(adresshtml,'html.parser')
        parts=soup.find_all('a',{'class':'ng-star-inserted'})
        adress=parts[0].text+", "+parts[1].text+", "+parts[2].text
        
        #get the numberof employees
        soup=BeautifulSoup(overview,'lxml')
        num_employ = soup.find(
        'a', class_="component--field-formatter field-type-enum link-accent ng-star-inserted")
        num_empoyees=num_employ.text
        
        #get the stock symbol
        stock_symbol=soup.find(
        'blob-formatter', class_="ng-star-inserted"    
        ).text

        #Get the website
        website=soup.find(
        'a', class_="component--field-formatter link-accent ng-star-inserted"    
        ).text

        data=[name,html,adress,num_empoyees,stock_symbol,website]
        await browser.close()
        return data    
