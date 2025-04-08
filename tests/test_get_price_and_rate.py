import re
import time


def get_minimal_price(page):
    time.sleep(5)
    # I wanted to wait for the full page to get loaded. Definitely not a best practice approach!
    # Further explanation and better approach under the "Further Improvements" section of my PDF file
    page.wait_for_selector('[data-testid="price-availability-row"]')
    price_elements = page.query_selector_all('[data-testid="price-availability-row"]')
    prices = extract_prices(price_elements)

    if prices:
        min_price = min(prices)
        print(f"The minimal price is: ${min_price}")
    else:
        print("No prices were extracted.")

def extract_prices(price_elements):
    prices = []
    price_pattern = r'\$\d+\s'

    for element in price_elements:
        text_content = element.text_content()
        if text_content:
            found_prices = re.findall(price_pattern, text_content.strip())
            cleaned_prices = [int(price.replace('$', '').replace('\xa0', '').strip()) for price in found_prices]
            prices.extend(cleaned_prices)

    return prices

def test_get_min_price_and_best_rate(airbnb_basic_search):
    page, airbnb, browser, _ = airbnb_basic_search
    get_minimal_price(page)


