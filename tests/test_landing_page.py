import pytest
import random
from playwright.sync_api import Page
from datetime import date, timedelta, datetime
from pages.landing_page import LandingPage
#from tests.base_test import BaseTest

#class LandingPageTests:

def test_page_visibility(page: Page):
    """
    Wander.com landing page is visible
    """
    landing_page = LandingPage(page)
    landing_page.navigate()
    assert landing_page.page_visible() == True

def data_provider():
    return ["An arbitrary search term"]
@pytest.mark.parametrize("keyword", data_provider())
def test_search_listing_by_name(keyword, page: Page):
    """
    Searching listings by name
    """
    landing_page = LandingPage(page)
    landing_page.navigate()
    landing_page.switch_tab_to_all_locations()
    row_count = landing_page.listing_count()

    if row_count > 0:
        listing_name = landing_page.get_listing_name(1)
        print("Listing name: ", listing_name)
        landing_page.search(listing_name)
        row_count = landing_page.listing_count()

        assert row_count > 0, "No search results for listing: " + listing_name

        for item in range(1, row_count):
            name = landing_page.get_listing_name(item)
            assert name.__contains__(listing_name), "Invalid search results for listing: "+listing_name
    else:
        landing_page.search(keyword)
        row_count = landing_page.listing_count()

        for item in range(1, row_count):
            name = landing_page.get_listing_name(item)
            assert name.__contains__(keyword), "Invalid search results for listing: "+keyword

    landing_page.clear_search()

def test_filter_listings_by_available_dates(page: Page):
    """
    Searching listings by available dates
    """
    landing_page = LandingPage(page)
    landing_page.navigate()
    landing_page.switch_tab_to_all_locations()
    row_count = landing_page.listing_count()
    current_year = datetime.now().year

    if row_count > 0:
        item = random.randint(1, row_count)
        start_date, end_date = landing_page.get_listing_available_days(item)

        if end_date < start_date:
            end_date = end_date.replace(year = current_year + 1)
        else:
            end_date = end_date.replace(year=current_year)
        start_date =start_date.replace(year = current_year)

        # start_date = start_date.strftime("%b %d")
        # end_date = end_date.strftime("%b %d")
        keyword = "from " + start_date.strftime("%b %d") + " to " + end_date.strftime("%b %d")
        landing_page.search(keyword)
        assert landing_page.no_matching_results() == False, "Listings matching the available dates not displayed"
        result_count = landing_page.listing_count()

        if not landing_page.no_matching_results():
            for item in range(1, result_count):
                item_start_date, item_end_date = landing_page.get_listing_available_days(item)
                if item_end_date < item_start_date:
                    item_end_date = item_end_date.replace(year=current_year + 1)
                else:
                    item_end_date = item_end_date.replace(year=current_year)
                item_start_date = start_date.replace(year=current_year)

                assert start_date <= item_start_date <= end_date, "List availability start date is out of range."
                assert start_date <= item_end_date <= end_date, "List availability end date is out of range."
        landing_page.clear_search()

    start_date = date.today() + timedelta(days = 1)
    end_date = start_date + timedelta(days = 14)
    # from_date = str(start_date.month) + " " + str(start_date.day)
    # end_date = str(end_date.month) + " " + str(end_date.day)
    keyword = "from " + start_date.strftime("%b %d")  +" to " + end_date.strftime("%b %d")
    landing_page.search(keyword)
    if not landing_page.no_matching_results():
        result_count = landing_page.listing_count()
        for item in range(1, result_count):
            item_start_date,  item_end_date = landing_page.get_listing_available_days(item)
            if item_end_date < item_start_date:
                item_end_date.replace(year=current_year + 1)
            else:
                item_end_date.replace(year=current_year)
            item_start_date = start_date.replace(year=current_year)

            assert start_date <= item_start_date <= end_date, "List availability start date is out of range."
            assert start_date <= item_end_date <= end_date, "List availability end date is out of range."
    landing_page.clear_search()

def test_search_listings_by_location(page: Page):
    """
        Searching listings by available dates
        """
    landing_page = LandingPage(page)
    landing_page.navigate()
    landing_page.switch_tab_to_all_locations()
    row_count = landing_page.listing_count()
    current_year = datetime.now().year




def test_search_listings_by_guests_count(page: Page):
    """
    Searching listings by available guests accommodation limit
    """
    guests_count = random.randint(4, 8)
    keyword = str(guests_count) + " people"

    landing_page = LandingPage(page)
    landing_page.navigate()
    landing_page.switch_tab_to_all_locations()
    landing_page.search(keyword)
    searched_guest_count = landing_page.get_searched_guess_limit()

    assert searched_guest_count == guests_count, "Search for " + str(guests_count) + " but showing results for " +str(searched_guest_count)
    row_count = landing_page.listing_count()

    for item in range(1, row_count):
        guests_limit = landing_page.get_listing_guest_limit(item)
        assert guests_limit >= guests_count, "Search for " + str(
            guests_count) + " but listing can only accommodate " + str(guests_limit)
    landing_page.clear_search()

def test_search_listings_by_date_location_guests(page: Page):
    pass