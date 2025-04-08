import pytest

from src.pages.airbnb_page import AirbnbPage
from src.tests.test_get_rates import test_get_rates
from src.tests.test_make_a_reservation import test_make_a_reservation


@pytest.fixture(scope="function")
def airbnb_setup_search(playwright, request):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    airbnb = AirbnbPage(page)

    destination, check_in_offset, check_out_offset, number_of_adults, number_of_children, test_function = request.param

    airbnb.open_homepage()
    airbnb.set_destination(destination)
    airbnb.set_dates(check_in_offset, check_out_offset)
    airbnb.add_guests(number_of_adults, number_of_children)
    airbnb.perform_search()

    yield page, airbnb

    browser.close()

def pytest_generate_tests(metafunc):
    if "airbnb_setup_search" in metafunc.fixturenames:
        metafunc.parametrize(
            "airbnb_setup_search",
            [
                ("Tel Aviv-Yafo, Israel", 0, 1, 2, None, test_get_rates),
                ("Tel Aviv-Yafo, Israel", 1, 3, 2, 1, test_make_a_reservation)
            ],
            indirect=True
        )
