import time
import re


def get_best_rate(page):
    time.sleep(5) # Again - not the best approach
    rating_pattern = r'\b(\d{1,2}\.\d{2})\s+\(\d+\)'
    found_ratings = re.findall(rating_pattern, page.content())
    ratings = [float(rating) for rating in found_ratings]

    if ratings:
        highest_rating = max(ratings)
        print(f"Highest rating found: {highest_rating}")
        return highest_rating
    else:
        print("No ratings were extracted.")
        return None