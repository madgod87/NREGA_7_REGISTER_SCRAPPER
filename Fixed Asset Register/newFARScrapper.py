import scrapy
import requests

class AssetSpider(scrapy.Spider):
    name = 'asset'
    start_urls = ['http://mnregaweb4.nic.in/netnrega/asset_report_dtl.aspx?lflag=eng&state_name=WEST%20BENGAL&state_code=32&district_name=PASCHIM%20MEDINIPUR&district_code=3210&block_name=KHARAGPUR-I&block_code=&panchayat_name=BARKOLA&panchayat_code=3210009002&fin_year=2022-2023&source=national&Digest=3uj6lSl1B82CIUczI//zQQ']

    def parse(self, response):
        i = 4
        while i<4000:
            assetid = response.xpath('//table[2]//tr[$i]/td[2]/text()', i=i).get()
            assetname = response.xpath('//table[2]//tr[$i]/td[3]/text()', i=i).get()
            schemecode = response.xpath('//table[2]//tr[$i]/td[5]/text()', i=i).get()
            schemename = response.xpath('//table[2]//tr[$i]/td[7]/text()', i=i).get()
            classofasset = response.xpath('//table[2]//tr[$i]/td[8]/text()', i=i).get()
            link = response.xpath('//table[2]//tr[$i]/td[6]/a/@href', i=i).get()
            strlink = str(link)
            urlid = "http://mnregaweb4.nic.in/netnrega/"
            strurl = str(urlid)
            absoluteurl = f"{strurl}{strlink}"

            request_object = requests.get(absoluteurl)
            response_object = scrapy.Selector(request_object)

            if response_object.xpath("//table[3]//tr[7]/td[1]/nobr/p/font[2]/text()").get() is None:
                sanctiondate = response_object.xpath("//table[3]//tr[6]/td[1]/nobr/p/font[2]/text()").get()
                wage = response_object.xpath("//table[3]//tr[10]/td/table//tr[2]/td[1]/font/text()").get()
                semiskilled = response_object.xpath("//table[3]//tr[10]/td/table//tr[2]/td[2]/font/text()").get()
                skilled = response_object.xpath("//table[3]//tr[10]/td/table//tr[2]/td[3]/font/text()").get()
                material = response_object.xpath("//table[3]//tr[10]/td/table//tr[2]/td[4]/font/a/text()").get()
                contingency = response_object.xpath("//table[3]//tr[10]/td/table//tr[2]/td[5]/font/text()").get()
                total = response_object.xpath("//table[3]//tr[10]/td/table//tr[2]/td[6]/font/text()").get()
                mandays = response_object.xpath('//table[3]//tr[11]/td/table//tr[2]/td[2]/font/text()').get()

            else:
                sanctiondate = response_object.xpath("//table[3]//tr[7]/td[1]/nobr/p/font[2]/text()").get()
                wage = response_object.xpath("//table[3]//tr[11]/td/table//tr[2]/td[1]/font/text()").get()
                semiskilled = response_object.xpath("//table[3]//tr[11]/td/table//tr[2]/td[2]/font/text()").get()
                skilled = response_object.xpath("//table[3]//tr[11]/td/table//tr[2]/td[3]/font/text()").get()
                material = response_object.xpath("//table[3]//tr[11]/td/table//tr[2]/td[4]/font/a/text()").get()
                contingency = response_object.xpath("//table[3]//tr[11]/td/table//tr[2]/td[5]/font/text()").get()
                total = response_object.xpath("//table[3]//tr[11]/td/table//tr[2]/td[6]/font/text()").get()
                mandays = response_object.xpath('//table[3]//tr[12]/td/table//tr[2]/td[2]/font/text()').get()
            
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
 
            i += 1