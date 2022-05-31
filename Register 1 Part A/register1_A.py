import scrapy

class Register1_A(scrapy.Spider):
    name = 'Register_1_A'

    start_urls = ['http://127.0.0.1:13739/main_data.html']

    def parse(self, response):
        tables = response.xpath('//div[3]/center/div[2]/table')
        for table in tables:
            trees = table.xpath('.//tr')
            for tree in trees:
                jcnumber = tree.xpath('.//td[2]/text()').get()
                date_of_issue_jc = tree.xpath('.//td[3]/text()').get()
                head_of_HH = tree.xpath('.//td[4]/text()[1]').get()
                Member_Name = str(tree.xpath('.//td[4]/text()[2]').get())[1:-1]
                age = tree.xpath('.//td[5]/text()[1]').get()
                gender = str(tree.xpath('.//td[5]/text()[2]').get())[1:-1]
                relationship = tree.xpath('.//td[6]/text()').get()
                caste = tree.xpath('.//td[7]/text()').get()
                apl_or_bpl = tree.xpath('.//td[8]/text()').get()
                land_holding = tree.xpath('.//td[9]/text()').get()
                bankaccount_no = tree.xpath('.//td[10]/text()').get()
                bank_name = tree.xpath('.//td[11]/text()').get()
                individual_asset = tree.xpath('.//td[12]/text()').get()

                yield {
                    'jcnumber': jcnumber,
                    'date_of_issue_jc': date_of_issue_jc,
                    'head_of_HH': head_of_HH,
                    'Member_Name': Member_Name,
                    'age': age,
                    'gender': gender,
                    'relationship': relationship,
                    'caste': caste,
                    'apl_or_bpl': apl_or_bpl,
                    'land_holding': land_holding,
                    'bankaccount_no': bankaccount_no,
                    'bank_name': bank_name,
                    'individual_asset': individual_asset
                }