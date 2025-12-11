# Importing Scrapy & Logging
import scrapy
import requests

# Creating Main Class
class AssetSpider(scrapy.Spider):
    name = 'work_details_wage'

    # Pointing to a LOCALLY served HTML file (127.0.0.1) as the starting point.
    # This allows the scraper to process a saved list of works without needing to
    # navigate the live website's main menu, avoiding potential timeouts/captchas.
    start_urls = ['http://127.0.0.1:5241/wage.html']

    def parse(self, response):
        trees = response.xpath('//table[2]//tr')
        for tree in trees:
            workname = tree.xpath('.//td/text()').get()
            if workname == " Work Name:":
                print('Skipped!!')
            else:
                mr_pre_number = tree.xpath('.//td[1]/font/a/text()').get()
                pay_date = tree.xpath('.//td[2]/font/text()').get()
                amount = tree.xpath('.//td[3]/font/text()').get()
                
                # Extracting link from the LOCAL file
                link = tree.xpath('.//td[1]/font/a/@href').get()
                strlink = str(link)
                # Removing relative path components (../../)
                new_str_link = strlink[6:]
                # Defining the LIVE website domain
                mainlink = str("http://mnregaweb4.nic.in/netnrega/")
                # Constructing the full URL for the LIVE website
                final_link = f"{mainlink}{new_str_link}"

                # Fetching the live detail page using synchronous 'requests' (Hybrid approach)
                # This fetches fresh details for the entry found in the local file
                request_object = requests.get(final_link, timeout=120)
                # converting the response to a Scrapy Selector for parsing
                response_object = scrapy.Selector(request_object)
                
                scheme_code = response_object.xpath('//*[@id="ContentPlaceHolder1_lblWorkCode"]/text()').get()
                scheme_name = response_object.xpath('//*[@id="ContentPlaceHolder1_lblWorkName"]/text()').get()

                yield {
                    'mr_pre_number':mr_pre_number,
                    'pay_date':pay_date,
                    'amount':amount,
                    'scheme_name': scheme_name,
                    'scheme_code': scheme_code
                }

        # Handling a second table format if present
        trees = response.xpath('//table[3]//tr')
        for tree in trees:
            mr_pre_number = tree.xpath('.//td[1]/font/a/text()').get()
            pay_date = tree.xpath('.//td[2]/font/text()').get()
            amount = tree.xpath('.//td[3]/font/text()').get()
            link = tree.xpath('.//td[1]/font/a/@href').get()
            strlink = str(link)
            new_str_link = strlink[6:]
            mainlink = str("http://mnregaweb4.nic.in/netnrega/")
            final_link = f"{mainlink}{new_str_link}"
            
            # Similar hybrid request for the second table
            request_object = requests.get(final_link, timeout=120)
            response_object = scrapy.Selector(request_object)
            scheme_code = response_object.xpath('//*[@id="ContentPlaceHolder1_lblWorkCode"]/text()').get()
            scheme_name = response_object.xpath('//*[@id="ContentPlaceHolder1_lblWorkName"]/text()').get()
            yield {
                'mr_pre_number':mr_pre_number,
                'pay_date':pay_date,
                'amount':amount,
                'scheme_name': scheme_name,
                'scheme_code': scheme_code
            }