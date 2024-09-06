from socket import timeout
import pyshorteners
import pdfkit
import scrapy

path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf = path)
options = {'page-size': 'A4'}

class WorkRegister(scrapy.Spider):
    name = "WorkRegister_PartB"
    start_urls = ['http://127.0.0.1:5500/Register_4_Part_B/index20-21.html']

    def parse(self, response):
        trees = response.xpath('//div[3]//div[2]/table//tr')
        all_links = []
        for tree in trees:
            if (tree.xpath('.//td[6]/text()').get()).strip()=="Gram Panchayat":
                print('true...............')
                front_url = 'https://mnregaweb2.nic.in/netnrega/'
                scraped_link = str(tree.xpath('.//td[2]/a/@href').get())
                new_url = f"{front_url}{scraped_link}"
                shortener = pyshorteners.Shortener(timeout=120)
                shortened_url = shortener.tinyurl.short(new_url)
                all_links.append(shortened_url)

        for i, link in enumerate(all_links):
            pdfkit.from_url(link, f"./Register_4_Part_B_20-21_{i}.pdf", configuration=config, options=options)