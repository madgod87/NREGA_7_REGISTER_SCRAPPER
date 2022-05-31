import scrapy

class SSKSpider(scrapy.Spider):
    name = "SSK"

    start_urls = ['http://mnregaweb4.nic.in/netnrega/writereaddata/citizen_out/MWSK_3201009009_GP_2122_eng.html']

    def parse(self, response):
        trees = response.xpath('//table[2]//tr')
        schemename = 'a'
        schemecode = 'a'
        for tree in trees:
            workname = tree.xpath('.//td/text()').get()
            if workname == " Work Name:":
                scheme_name = str(tree.xpath('.//td/font/text()').get()).split('(')[0]
                scheme_code = str(tree.xpath('.//td/font/text()').get()).split('(')[1]
                schemename = scheme_name
                schemecode = scheme_code
            else:
                mr_number = tree.xpath('.//td[1]/font/a/text()').get()
                amount = tree.xpath('.//td[2]/font/text()').get()

                yield {
                    'schemename': schemename,
                    'schemecode': schemecode,
                    'mr_number': mr_number,
                    'amount': amount
                }