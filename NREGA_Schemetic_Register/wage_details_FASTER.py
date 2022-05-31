
import scrapy
import requests

class AssetSpider(scrapy.Spider):
    name = 'work_details_wage'

    start_urls = ['http://mnregaweb4.nic.in/netnrega/writereaddata/citizen_out/MW_3201009009_GP_2122_eng.html']

    def parse(self, response):
        trees = response.xpath('//table[2]//tr')
        scheme_data = 'a'
        for tree in trees:
            workname = tree.xpath('.//td/text()').get()
            if workname == " Work Name:":
                scheme = tree.xpath('.//td/font/text()').get()
                scheme_data = scheme
            else:
                mr_pre_number = tree.xpath('.//td[1]/font/a/text()').get()
                pay_date = tree.xpath('.//td[2]/font/text()').get()
                amount = tree.xpath('.//td[3]/font/text()').get()

                yield {
                    'scheme_name': scheme_data,
                    'scheme_code': scheme_data,
                    'mr_pre_number':mr_pre_number,
                    'pay_date':pay_date,
                    'amount':amount
                }

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
            request_object = requests.get(final_link, timeout=120)
            response_object = scrapy.Selector(request_object)
            scheme_code = response_object.xpath('//*[@id="ContentPlaceHolder1_lblWorkCode"]/text()').get()
            scheme_name = response_object.xpath('//*[@id="ContentPlaceHolder1_lblWorkName"]/text()').get()
            
            yield {
                'scheme_name': scheme_name,
                'scheme_code': scheme_code,
                'mr_pre_number':mr_pre_number,
                'pay_date':pay_date,
                'amount':amount
            }