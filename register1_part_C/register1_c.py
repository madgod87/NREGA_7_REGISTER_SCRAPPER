import scrapy

class Register1PartB(scrapy.Spider):
    name = 'Register_1_Part_C'
    start_urls = ['http://127.0.0.1:5555/Ladhurka/quarter1.html','http://127.0.0.1:5555/Ladhurka/quarter2.html','http://127.0.0.1:5555/Ladhurka/quarter3.html','http://127.0.0.1:5555/Ladhurka/quarter4.html']

    def parse(self, response):
        tables = response.xpath('//div[3]/center/div[2]/table')
        for table in tables:
            trees = table.xpath('.//tr')
            for tree in trees:
                sl_no = tree.xpath('.//td[1]/text()').get()
                jc_number = tree.xpath('.//td[2]/text()').get()
                accept_date = tree.xpath('.//td[3]/text()').get()
                head_of_the_house = tree.xpath('.//td[4]/text()[1]').get()
                name = str(tree.xpath('.//td[4]/text()[2]').get())[1:-1]
                age = tree.xpath('.//td[5]/text()[1]').get()
                gender = str(tree.xpath('.//td[5]/text()[2]').get())[1:-1]
                relationship = tree.xpath('.//td[6]/text()').get()
                caste = tree.xpath('.//td[7]/text()').get()
                wheather_aplorbpl = tree.xpath('.//td[8]/text()').get()
                land_holding = tree.xpath('.//td[9]/text()').get()
                bank_account = tree.xpath('.//td[10]/text()').get()
                bank_name = tree.xpath('.//td[11]/text()').get()
                individual_asset_if_any = tree.xpath('.//td[12]/text()').get()

                yield {
                    'sl_no': sl_no,
                    'jc_number': jc_number,
                    'accept_date': accept_date,
                    'head_of_the_house': head_of_the_house,
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'relationship': relationship,
                    'caste': caste,
                    'wheather_aplorbpl': wheather_aplorbpl,
                    'land_holding': land_holding,
                    'bank_account': bank_account,
                    'bank_name': bank_name,
                    'individual_asset_if_any': individual_asset_if_any
                }
