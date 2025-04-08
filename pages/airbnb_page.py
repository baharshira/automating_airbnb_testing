from datetime import datetime, timedelta


class AirbnbPage:
    def __init__(self, page):
        self.page = page

    def open_homepage(self):
        self.page.goto('https://www.airbnb.com')

    def set_destination(self, destination):
        self.page.fill('input[data-testid="structured-search-input-field-query"]', destination)

    def set_dates(self, check_in_offset=0, check_out_offset=1):
        check_in_str, check_out_str = self.calculate_dates(check_in_offset, check_out_offset)

        self.page.click('div[data-testid="structured-search-input-field-split-dates-0"]')
        self.page.click(f'button[data-state--date-string="{check_in_str}"]')

        # Here I would handle a case where the checkout date isn't visible

        self.page.click(f'button[data-state--date-string="{check_out_str}"]')
        self.page.click('div[data-testid="structured-search-input-field-split-dates-1"]')

    def calculate_dates(self, check_in_offset, check_out_offset):
        today = datetime.now()
        check_in_date = today + timedelta(days=check_in_offset)
        check_out_date = today + timedelta(days=check_out_offset)
        check_in_str = check_in_date.strftime("%Y-%m-%d")
        check_out_str = check_out_date.strftime("%Y-%m-%d")

        return check_in_str, check_out_str

    def add_guests(self, number_of_adults=2, number_of_children=None):
        guest_button = self.page.locator('div[data-testid="structured-search-input-field-guests-button"]')
        guest_button.click()
        adults_increase_button = self.page.locator('button[data-testid="stepper-adults-increase-button"]')

        for _ in range(number_of_adults):
            adults_increase_button.click()

        if number_of_children is not None and number_of_children > 0:
            children_increase_button = self.page.locator('button[data-testid="stepper-children-increase-button"]')
            for _ in range(number_of_children):
                children_increase_button.click()

        # Other cases: Infants and Pets

    def perform_search(self):
        self.page.click('button[data-testid="structured-search-input-search-button"]')
