import scrapy
import logging

class MRSpider(scrapy.Spider):
    name = "MR Details"

    start_urls = ['http://mnregaweb4.nic.in/netnrega/citizen_html/Musternew.aspx?lflag=eng&state_name=WEST+BENGAL&district_name=24+PARGANAS+SOUTH&block_name=BISHNUPUR-I&id=1&Panchayat_name=BHANDARIA+KASTEKUMARI&Panchayat_code=3216004003&workcode=3216004003%2fWC%2f321002040898643&Msrno=22483&finyear=2020-2021&dtfrm=02%2f03%2f2021&dtto=16%2f03%2f2021&wn=RESTORATION+OF+POND+OF+KASHINATH+MONDAL+AND+SIXTEEN+OTHERS+AT+SANSAD+VIII&Digest=3JgRukpYM2b4VROfZLo7sQ']

    def parse(self, response):
# Declaring All Tree Elements
        child_trees = response.xpath('//*[@id="ContentPlaceHolder1_grdShowRecords"]//tr')
# Looping Over All Tree Elements
        for child_tree in child_trees:
# Creating Iterable Item for Checking Attendance Value
            attendence = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
# Checking Attendance Value
            for j in attendence:
                attendence_check = child_tree.xpath('.//th[$j]//text()', j=j).get()
                if attendence_check == "Total Attendance":
# Assigning & Declaring Global Attendance Value
                    global i
                    i = j
# Declaring Name Value
            name = child_tree.xpath('.//td[2]//text()').get()
# Checking & Skipping Unwanted Name Values
            if name is None or name == "Daily Attendence":
                print('REJECTED')
# Assigning Other Values with Global Attendance Value
            else:
# Declaring Values of New Page
                demanded_days = i-5
                mr_number = response.xpath('//*[@id="ContentPlaceHolder1_lblMsrNo2"]/text()').get()
                start_date = response.xpath('//*[@id="ContentPlaceHolder1_lbldatefrom"]/text()').get()
                end_date = response.xpath('//*[@id="ContentPlaceHolder1_lbldateto"]/text()').get()
                as_approve_number = response.xpath('//*[@id="ContentPlaceHolder1_lblSanctionno"]/text()').get()
                as_approval_date = response.xpath('//*[@id="ContentPlaceHolder1_lblSanctionDate"]/text()').get()
                scheme_code = response.xpath('//*[@id="ContentPlaceHolder1_lblWorkCode"]/text()').get()
                scheme_name = response.xpath('//*[@id="ContentPlaceHolder1_lblWorkName"]/text()').get()
                mb_number = response.xpath('//*[@id="ContentPlaceHolder1_mbno"]/text()').get()
                mb_page_number = response.xpath('//*[@id="ContentPlaceHolder1_page_no"]/text()').get()
                jc_number = child_tree.xpath('.//td[2]//a/text()').get()
                total_md = str((child_tree.xpath('.//td[$i]//text()', i=i).get()).split()[0])
                wage_per_day = child_tree.xpath('.//td[$i+1]//text()', i=i).get()
                total_amount = str((child_tree.xpath('.//td[$i+2]//text()', i=i).get()).split()[0])
                wagelist_number = str((child_tree.xpath('.//td[$i+9]//text()', i=i).get()).split()[0])
# Providing Output
                yield {
                    'jc_number':jc_number,
                    'name':name,
                    'demanded_days':demanded_days,
                    'scheme_code':scheme_code,
                    'mr_number':mr_number,
                    'start_date':start_date,
                    'end_date':end_date,
                    'total_md':total_md,
                    'total_amount':total_amount,
                    'scheme_name':scheme_name,
                    'as_approve_number':as_approve_number,
                    'as_approval_date':as_approval_date,
                    'mb_number':mb_number,
                    'mb_page_number':mb_page_number,
                    'wage_per_day':wage_per_day,
                    'wagelist_number':wagelist_number
                    }
