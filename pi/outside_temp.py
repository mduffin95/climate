import requests
import re
from bs4 import BeautifulSoup
import logging.config

logging.config.fileConfig('outside_temp.conf')
# set up logger
logger = logging.getLogger('outsideTemp')

def scrape_temperature():
    url = "https://www.woodingdeanweather.net/index.php?lang=en-uk&units=uk&theme=user"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the span tag containing the text "Temperature °C"
        temperature_div = soup.find('div', id='position11')

        if temperature_div:
            # Get the parent div of the span tag
            div_module_content = temperature_div.find('div', class_='PWS_module_content')

            div_middle = div_module_content.find('div', class_='PWS_middle')
            div_left = div_module_content.find('div', class_='PWS_left')

            temperature_text = div_middle.text.strip()

            left_text = div_left.text.strip()

            humidity_pattern = re.compile('Humidity(\d+\.\d+)%')
            match = humidity_pattern.search(left_text)
            humidity = None
            if match:
                humidity = match.group(1)

            match = re.search("^[\d.]+", temperature_text)
            temperature = None
            if match:
                temperature = float(match.group())

            return temperature, humidity

        else:
            logger.error("Temperature element not found on the page.")
    else:
        logger.error(f"Failed to retrieve the web page.")

    return None

if __name__ == "__main__":
    temp, humidity = scrape_temperature()
    if temp:
        logger.info("Reading taken", extra={ "temperature" : temp, "humidity": humidity })

