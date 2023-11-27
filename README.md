# Python Selenium Scraper

## Overview
This project is a Python script that uses Selenium to scrape football match predictions and related data from a given website. It collects data such as league information, team names, match times, probabilities, expected scores, temperatures, odds, and match status before saving it as a JSON file.

## System Requirements
- Python 3.x
- Chrome browser
- ChromeDriver

## Installation

### Set up Python and pip
Ensure you have Python 3.x installed on your system. Python's package manager pip is also required to install dependencies.

### Virtual Environment (Optional)
It's recommended to use a virtual environment to keep dependencies required by different projects separate.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Python Dependencies
Install the necessary Python packages using pip:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should contain:
```
selenium==4.15.2
tqdm==4.66.1
```

### ChromeDriver
Download the ChromeDriver executable from the [ChromeDriver download page](https://chromedriver.chromium.org/downloads) that matches your Chrome version. Ensure it's placed in a directory that is in your system's PATH.

## Usage

### Set the Date Range
Modify the `start_date` and `end_date` variables in the script to reflect the date range you wish to scrape.

### Run the Scraper
Execute the script with Python:

```bash
python selenium_scraper.py
```

The script will scrape data for each date in the specified range and save it as a series of JSON files in the `data` directory.

## Output
- JSON files will be generated in the `data` directory, named in the format `forebet_{date}.json`.
- Each file contains the scraped data for that particular date.

## Contributing
Feel free to fork the project and submit pull requests. Contributions to improve the script or add new features are welcome.

## License
This project is released under the MIT License. See the LICENSE file in the repository for more information.