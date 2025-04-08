import pytest
from pages.airbnb_page import AirbnbPage
from utils.get_best_rate import get_best_rate
from tests.test_validate_search import validate_search


@pytest.fixture(scope="function")
def airbnb_basic_search(playwright, request):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    airbnb = AirbnbPage(page)
    page, airbnb, browser, best_rate = perform_search_and_validation(browser, airbnb, page, request)

    yield page, airbnb, browser, best_rate

def perform_search_and_validation(browser, airbnb, page, request):
    destination, check_in_offset, check_out_offset, number_of_adults, number_of_children = request.param

    airbnb.open_homepage()
    airbnb.set_destination(destination)
    airbnb.set_dates(check_in_offset, check_out_offset)
    airbnb.add_guests(number_of_adults, number_of_children)
    airbnb.perform_search()
    validate_search(page, request.param)
    best_rate = get_best_rate(page)

    return page, airbnb, browser, best_rate

def pytest_generate_tests(metafunc):
    if "airbnb_basic_search" in metafunc.fixturenames:
        test_params = {
            "test_get_min_price_and_best_rate": [("Tel Aviv-Yafo", 1, 2, 2, 0)],
            "test_make_a_reservation": [("Tel Aviv-Yafo", 1, 3, 2, 1)]
        }
        function_name = metafunc.function.__name__
        params = test_params.get(function_name, [])
        metafunc.parametrize("airbnb_basic_search", params, indirect=True)
