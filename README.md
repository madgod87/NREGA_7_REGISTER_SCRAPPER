# NREGA 7 Register Scraper System

## Overview
This repository contains a collection of Python scripts built using **Scrapy** and **Requests** to scrape data for various registers under the Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA). The system allows for extracting detailed information such as Asset Registers, Wage Details, Material Details, and Employment Registers (Register 1 Part A, B, C, and Register III).

## Repository Structure
The codebase is organized into directories corresponding to different registers:

*   **Fixed Asset Register/**
    *   `newFARScrapper.py`: Scrapes detailed asset reports including costs, sanctioned dates, and employment mandays.
    *   `asset_complitionDate.py`: Extracts asset completion dates and expenditure details (wages, material, skilled/semi-skilled).
    *   `asset_information.py`: Similar to `newFARScrapper.py`, but tailored for different schemes and loop conditions.
*   **NREGA_Schemetic_Register/**
    *   `scrapper.py`: Scrapes work details, including muster roll (MR) numbers, attendance, and payments.
    *   `wage_details.py`: specific scraper for wage-related data, handling local and remote data fetching.
    *   `material_details.py`: Extracts material bill dates, payment dates, and amounts.
    *   `ssk_details.py`: Scrapes Semi-Skilled and Skilled (SSK) work details.
*   **Register 1 Part A/**
    *   `register1_A.py`: Scrapes household and job card details (Register 1 Part A) from locally served files.
*   **register1_part_B/**
    *   `register1_part_B.py`: Scrapes applicant details (Register 1 Part B) from locally served files.
*   **register1_part_C/**
    *   `register1_c.py`: Scrapes employment demand/allocation details (Register 1 Part C) from locally served files.
*   **Register III/**
    *   `registerScrapper.py`: Scrapes Register III (Works Register) details including muster rolls and work execution info.

## Prerequisites
*   **Python 3.x**
*   **Scrapy**: `pip install scrapy`
*   **Requests**: `pip install requests`

## Installation
1.  Clone this repository.
2.  Install the required dependencies:
    ```bash
    pip install scrapy requests
    ```

## Usage
Most scripts are standalone Scrapy spiders. You can run them using the `scrapy runspider` command.

### Running Spiders
Navigate to the directory of the script you want to run and execute:
```bash
scrapy runspider <script_name>.py -o output.json
```
*Replace `<script_name>.py` with the actual filename and `output.json` with your desired output file (JSON, CSV, etc.).*

### Important Note on Local Servers
Several scripts (e.g., `register1_A.py`, `wage_details.py`) are configured to scrape from a local server (e.g., `http://127.0.0.1:5555/` or `http://127.0.0.1:5241/`).
*   **Why?**: This is often done to process saved HTML files offline to avoid connection timeouts, CAPTCHAs, or IP bans during heavy scraping.
*   **How to run**:
    1.  Ensure you have the required HTML files saved in a directory structure matching the script's `start_urls`.
    2.  Start a local HTTP server in that directory (e.g., using `python -m http.server 5555`).
    3.  Run the spider.

## detailed Code Explanation
For a line-by-line breakdown and logic explanation of the scripts, please refer to [CODE_EXPLANATION.md](./CODE_EXPLANATION.md).

## Disclaimer
This tool is for educational and data analysis purposes. Ensure you comply with the terms of service of the target website (nrega.nic.in) before scraping. Use responsibly.
