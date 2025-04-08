import time

def click_highest_rating(page, rating_str):
    time.sleep(2) # Same as in get price and rate - naive solution

    if rating_str:
        rating_selector = f"text='{rating_str}'"
        try:
            # Increase timeout or ensure the page has fully loaded all components
            element = page.wait_for_selector(rating_selector, state="visible", timeout=10000)
            element.click()
            print(f"Successfully clicked on the element with rating: {rating_str}")
        except Exception as e:
            print(f"Failed to click on the element with rating {rating_str}: {str(e)}")
            assert False, f"Failed to click on the element with rating {rating_str}: {str(e)}"
    else:
        print("Rating string not provided.")
        assert False, "Rating string not provided."

# It's not working, and I explained why at my PDF
# But this is the flow I would do:
# Clicking the listing with the highest rate
# Click the call-to-action button (data-testid="homes-pdp-cta-btn")
# Enter the phone number in the phone's input section (data-testid="login-signup-phonenumber")
def test_make_a_reservation(airbnb_basic_search):
    page, airbnb, browser, rate = airbnb_basic_search

    if rate:
        click_highest_rating(page, rate)
        try:
            reserve_button = page.wait_for_selector('[data-testid="homes-pdp-cta-btn"]', timeout=10000)
            reserve_button.click()
            print("Reserve button clicked successfully.")

            phone_input = page.wait_for_selector('[data-testid="login-signup-phonenumber"]', timeout=10000)
            phone_input.fill('234567890')
            print("Phone number entered successfully.")
        except Exception as e:
            print(f"Failed in the reservation process: {str(e)}")
            assert False, f"Failed in the reservation process: {str(e)}"
    else:
        print("Failed to retrieve a valid highest rating.")
        assert False, "Failed to retrieve a valid highest rating."