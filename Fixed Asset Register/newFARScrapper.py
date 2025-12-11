import scrapy
import requests

class AssetSpider(scrapy.Spider):
    name = 'asset'
    # Start URL for the Asset Report Page
    start_urls = ['http://mnregaweb4.nic.in/netnrega/asset_report_dtl.aspx?lflag=eng&state_name=WEST%20BENGAL&state_code=32&district_name=PASCHIM%20MEDINIPUR&district_code=3210&block_name=KHARAGPUR-I&block_code=&panchayat_name=BARKOLA&panchayat_code=3210009002&fin_year=2022-2023&source=national&Digest=3uj6lSl1B82CIUczI//zQQ']

    def parse(self, response):
        # Initialize row counter starting at 4 (skipping headers)
        i = 4
        # Loop to iterate through rows in the table (limit set to 4000 to prevent infinite loops)
        while i<4000:
            # Extracting basic asset details from the main list table using XPath with dynamic index 'i'
            assetid = response.xpath('//table[2]//tr[$i]/td[2]/text()', i=i).get()
            assetname = response.xpath('//table[2]//tr[$i]/td[3]/text()', i=i).get()
            schemecode = response.xpath('//table[2]//tr[$i]/td[5]/text()', i=i).get()
            schemename = response.xpath('//table[2]//tr[$i]/td[7]/text()', i=i).get()
            classofasset = response.xpath('//table[2]//tr[$i]/td[8]/text()', i=i).get()
            
            # Extract the relative link to the asset details
            link = response.xpath('//table[2]//tr[$i]/td[6]/a/@href', i=i).get()
            strlink = str(link)
            urlid = "http://mnregaweb4.nic.in/netnrega/"
            strurl = str(urlid)
            # Construct the absolute URL for the detail page
            absoluteurl = f"{strurl}{strlink}"

            # Make a Synchronous request to the detail page (Blocking call)
            # This fetches the detail page immediately to extract nested data
            request_object = requests.get(absoluteurl)
            # Create a Scrapy Selector from the response text to use XPath on the new page
            response_object = scrapy.Selector(request_object)

            # Conditional check for table structure variations (some pages have an extra row)
            if response_object.xpath("//table[3]//tr[7]/td[1]/nobr/p/font[2]/text()").get() is None:
                # Structure A: Data located at specific rows
                sanctiondate = response_object.xpath("//table[3]//tr[6]/td[1]/nobr/p/font[2]/text()").get()
                wage = response_object.xpath("//table[3]//tr[10]/td/table//tr[2]/td[1]/font/text()").get()
                semiskilled = response_object.xpath("//table[3]//tr[10]/td/table//tr[2]/td[2]/font/text()").get()
                skilled = response_object.xpath("//table[3]//tr[10]/td/table//tr[2]/td[3]/font/text()").get()
                material = response_object.xpath("//table[3]//tr[10]/td/table//tr[2]/td[4]/font/a/text()").get()
                contingency = response_object.xpath("//table[3]//tr[10]/td/table//tr[2]/td[5]/font/text()").get()
                total = response_object.xpath("//table[3]//tr[10]/td/table//tr[2]/td[6]/font/text()").get()
                mandays = response_object.xpath('//table[3]//tr[11]/td/table//tr[2]/td[2]/font/text()').get()

            else:
                # Structure B: Data shifted by one row due to extra content
                sanctiondate = response_object.xpath("//table[3]//tr[7]/td[1]/nobr/p/font[2]/text()").get()
                wage = response_object.xpath("//table[3]//tr[11]/td/table//tr[2]/td[1]/font/text()").get()
                semiskilled = response_object.xpath("//table[3]//tr[11]/td/table//tr[2]/td[2]/font/text()").get()
                skilled = response_object.xpath("//table[3]//tr[11]/td/table//tr[2]/td[3]/font/text()").get()
                material = response_object.xpath("//table[3]//tr[11]/td/table//tr[2]/td[4]/font/a/text()").get()
                contingency = response_object.xpath("//table[3]//tr[11]/td/table//tr[2]/td[5]/font/text()").get()
                total = response_object.xpath("//table[3]//tr[11]/td/table//tr[2]/td[6]/font/text()").get()
                mandays = response_object.xpath('//table[3]//tr[12]/td/table//tr[2]/td[2]/font/text()').get()
            
            # Yield the combined data from the main list and the detail page
            yield {
                'assetid': assetid,
                'schemename': schemename,
                'schemecode': schemecode,
                'assetname': assetname,
                'classofasset': classofasset,
                'sanctiondate': sanctiondate,
                'wage': wage,
                'semiskilled': semiskilled,
                'skilled': skilled,
                'material': material,
                'contingency': contingency,
                'total': total,
                'mandays': mandays       
            }
 
            # Increment counter to process next row
            i += 1