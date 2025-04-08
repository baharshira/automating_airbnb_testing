from datetime import datetime, timedelta
import re


def validate_search(page, params):
    destination, check_in_offset, check_out_offset, number_of_adults, number_of_children = params
    validate_destination(page,destination)
    validate_dates(page,check_in_offset,check_out_offset)
    validate_guests(page, number_of_adults, number_of_children)

def validate_destination(page, destination):
    location_element = page.query_selector('[data-testid="little-search-location"]')
    location_text = location_element.text_content().strip()
    assert destination in location_text, f"Expected location to include {destination}, but found '{location_text}'."


def validate_dates(page, check_in_offset, check_out_offset):

    formatted_check_in_date, formatted_check_out_date = format_and_normalize_dates(check_in_offset, check_out_offset)
    dates_element = page.query_selector('[data-testid="little-search-anytime"]')
    dates_text = dates_element.text_content().strip()
    normalized_dates_text = re.sub(r'\s+', ' ', dates_text.replace('–', '-')).strip()

    expected_dates_text = f"Check in / Check out{formatted_check_in_date} - {formatted_check_out_date}"
    assert expected_dates_text == normalized_dates_text, f"Expected dates to be '{expected_dates_text}', but found '{normalized_dates_text}'."

def format_and_normalize_dates(check_in_offset, check_out_offset):
    today = datetime.now()
    check_in_date = today + timedelta(days=check_in_offset)
    check_out_date = today + timedelta(days=check_out_offset)

    if check_in_date.month == check_out_date.month:
        formatted_check_in_date = check_in_date.strftime("%b %-d")
        formatted_check_out_date = check_out_date.strftime("%-d")
    else:
        formatted_check_in_date = check_in_date.strftime("%b %-d")
        formatted_check_out_date = check_out_date.strftime("%b %-d")

    return formatted_check_in_date, formatted_check_out_date

def validate_guests(page, number_of_adults, number_of_children):
    guests_element = page.query_selector('[data-testid="little-search-guests"]')
    guests_text = guests_element.text_content().strip()
    guests_text = guests_text.replace('\u00A0', ' ').strip()
    match = re.search(r'(\d+)\s+guests', guests_text, re.IGNORECASE)

    if match:
        guests_text = f"{match.group(1)} guests"
    total_guests = number_of_adults + number_of_children
    expected_guests_text = f"{total_guests} guests"
    assert guests_text == expected_guests_text, f"Expected guests to be '{expected_guests_text}', but found '{guests_text}'."

    print("All search validations passed successfully.")
