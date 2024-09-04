import logging
import pyshorteners
import pdfkit
import scrapy
import requests
import time
from urllib.parse import quote

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path)

options = {
    'page-size': 'A4',
    'javascript-delay': 10000,
    'no-stop-slow-scripts': '',
    'enable-local-file-access': ''
}

class WorkRegister(scrapy.Spider):
    name = "WorkRegister_PartB"
    start_urls = ['http://127.0.0.1:5500/index20-21.html']

    def parse(self, response):
        trees = response.xpath('//div[3]//div[2]/table//tr')
        all_links = []
        skipped_urls = []

        for tree in trees:
            if (tree.xpath('.//td[6]/text()').get()).strip() == "Gram Panchayat":
                front_url = 'https://nregastrep.nic.in/netnrega/'
                scraped_link = str(tree.xpath('.//td[2]/a/@href').get())
                new_url = f"{front_url}{scraped_link}"
                # Encode URL
                encoded_url = quote(new_url, safe=':/?&=')
                shortener = pyshorteners.Shortener()

                attempt = 0
                while True:
                    try:
                        logging.info(f"Attempting to shorten URL: {encoded_url} (Attempt {attempt + 1})")
                        shortened_url = shortener.tinyurl.short(encoded_url)
                        all_links.append(shortened_url)
                        logging.info(f"Successfully shortened URL: {shortened_url}")
                        break
                    except Exception as e:
                        attempt += 1
                        logging.error(f"Error shortening URL {encoded_url} on attempt {attempt}: {e}")
                        backoff_time = 5 * attempt
                        logging.info(f"Retrying after {backoff_time} seconds...")

        valid_links = []
        for url in all_links:
            try:
                response = requests.get(url, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    valid_links.append(url)
                    logging.info(f"URL is reachable: {url}")
                else:
                    logging.warning(f"URL is not reachable (Status code: {response.status_code}): {url}")
            except requests.RequestException as e:
                logging.error(f"Error checking URL {url}: {e}")
                skipped_urls.append(url)

        logging.info("All valid URLs: %s", valid_links)
        logging.info("Skipped URLs: %s", skipped_urls)
        logging.info(f"Total skipped URLs: {len(skipped_urls)}")

        if valid_links:
            retries = 3
            for attempt in range(retries):
                try:
                    pdfkit.from_url(valid_links, r"./Register_4_Part_B_20-21.pdf", configuration=config, options=options)
                    logging.info("PDF successfully created!")
                    break
                except Exception as e:
                    logging.error(f"Error creating PDF on attempt {attempt + 1}: {e}")
                    time.sleep(5 * (attempt + 1))
                    if attempt == retries - 1:
                        logging.error("Failed to create PDF after multiple attempts.")
        else:
            logging.error("No valid URLs found. Skipping PDF creation.")
