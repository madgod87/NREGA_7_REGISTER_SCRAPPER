import scrapy

class MaterialSpider(scrapy.Spider):
    name = "Material"

    start_urls = ['http://mnregaweb4.nic.in/netnrega/writereaddata/citizen_out/MATW_3201009009_GP__eng_2122.html']

    def parse(self, response):
        trees = response.xpath('//center[1]/table[2]//tr')
        i = 0
        for tree in trees:
            bill_date = tree.xpath('.//td[3]/text()').get()
            payment_date = tree.xpath('.//td[4]/text()').get()
            amount = tree.xpath('.//td[5]/font/text()').get()
            link = tree.xpath('.//td[2]/font/a/@href').get()
            str_link = str(link)
            new_str_link = str_link[6:]
            main_link = str("http://mnregaweb4.nic.in/netnrega/")
            final_link = f"{main_link}{new_str_link}"
            yield scrapy.Request(url = final_link, callback= self.parse_bill, meta={'bill_date': bill_date, 'payment_date': payment_date, 'amount': amount})

    def parse_bill(self, response):
        bill_date = response.request.meta['bill_date']
        payment_date = response.request.meta['payment_date']
        amount = response.request.meta['amount']
        scheme_name = str(response.xpath('//center/div/table[4]//tr[1]/td/b/text()').get())[3:]
        scheme_code = str(response.xpath('//center/div/table[4]//tr[2]/td/b/text()').get())[2:]

        yield {
            'bill_date': bill_date,
            'payment_date': payment_date,
            'amount': amount,
            'scheme_name': scheme_name,
            'scheme_code': scheme_code
        }