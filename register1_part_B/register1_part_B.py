import scrapy

class Register1PartB(scrapy.Spider):
    name = 'Register_1_Part_B'

    # Pointing to a local server where the HTML files are hosted
    start_urls = ['http://127.0.0.1:4243/register1_part_B/ashuti-1-maindata.html']

    def parse(self, response):
        trees = response.xpath('//center/table[2]//tr')
        i = 0
        # Initialize placeholder variables for merged cells (Head of Family, Caste, etc.)
        # These values are often omitted in subsequent rows of a family group
        head_of_family = "a"
        caste_value = "a"
        fathers_name_value = "a"
        
        for tree in trees:
            # Skip the first 3 rows (likely headers)
            if i<3:
                print('SKIPPED')
                i+=1
            else:
                # Logic for "Head of Family"
                # If the cell is empty (None), it means this row belongs to the previously encountered family.
                # We reuse the stored 'head_of_family' value.
                if tree.xpath('.//td[2]/font/b/text()').get() is None:
                    head_name = head_of_family
                else:
                    # If present, update the current head and store it for future rows
                    head_name = tree.xpath('.//td[2]/font/b/text()').get()
                    head_of_family = head_name
                
                # Logic for "Caste" (Same logic as above)
                if tree.xpath('.//td[3]/font/text()').get() is None:
                    caste = caste_value
                else:
                    caste = tree.xpath('.//td[3]/font/text()').get()
                    caste_value = caste
                
                name_of_applicant = tree.xpath('.//td[5]/font/text()').get()
                
                # Logic for "Father's Name" (Same logic as above)
                if tree.xpath('.//td[6]/font/b/text()').get() is None:
                    fathers_name = fathers_name_value
                else:
                    fathers_name = tree.xpath('.//td[6]/font/b/text()').get()
                    fathers_name_value = fathers_name
                
                gender = tree.xpath('.//td[7]/font/text()').get()
                age = tree.xpath('.//td[8]/font/text()').get()
                date_of_application = tree.xpath('.//td[9]/font/text()').get()
                jcnumber = tree.xpath('.//td[10]/font/nobr/text()').get()
                issue_date = tree.xpath('.//td[10]/font/text()').get()

                yield {
                    'head_name': head_name,
                    'caste': caste,
                    'name_of_applicant': name_of_applicant,
                    'fathers_name': fathers_name,
                    'gender': gender,
                    'age': age,
                    'date_of_application': date_of_application,
                    'jcnumber': jcnumber,
                    'issue_date': issue_date
                }