from datetime import datetime, date

from playwright.sync_api import Page, Locator, expect


class LandingPage:
    TIMEOUT_SHORT = 1000
    TIMEOUT_MEDIUM = 5000
    TIMEOUT_LONG = 15000

    page = None

    def __init__(self, page: Page) -> None:
        self.page = page
        self.button_date_picker = page.locator("(//input[@name='search']/../../../following-sibling::div[1]//button)[1]")
        self.text_searched_date_range = page.locator("(//input[@name='search']/../../../following-sibling::div[1]//button)[1]/span")
        self.button_location_picker = page.locator("//button[text()='Location']")
        self.text_searched_location = page.locator("(//input[@name='search']/../../../following-sibling::div[1]//button)[2]/span")
        self.button_people_picker = page.locator("//button[text()='People']")
        self.text_searched_guests = page.locator("(//input[@name='search']/../../../following-sibling::div[1]//button)[3]/span")
        self.button_filter = page.locator("//button[span[text()='Filter']]")
        self.input_search = page.locator("//input[@name='search']")
        self.button_search = page.locator("//input[@name='search']/../following-sibling::button[2]")
        self.button_clear_search_content = page.locator("//input[@name='search']/../following-sibling::button[1]")
        self.text_title = self.page.locator("//h1[text()='Find your happy place.']")

        #tabs
        self.tab_locations = page.locator("//button[@role='tab' and text()='All locations']")
        self.tab_near_me = page.locator("//button[@role='tab' and text()='Near me']")
        self.tab_ocean = page.locator("//button[@role='tab' and text()='Ocean']")

        #listings
        self.text_no_results = page.locator("//div[@id='properties-list']//h1[text()=\"We couldn't find anything\"]")
        self.text_no_match = page.locator("//div[@id='properties-list']//h2[text()='No Match']")
        self.card_listing = page.locator("//div[@id='properties-list']/a")

        self.text_searched_timeline = page.locator("//div[@id='properties-list']/h2[not(text()='Unavailable')][1]")

    def navigate(self):
        self.page.goto("https://www.wander.com/",  wait_until = "load")

    def page_visible(self) -> bool:
        expect(self.text_title).to_be_visible(timeout = self.TIMEOUT_MEDIUM)
        return self.text_title.is_visible()

    def _switch_tab(self, tab: Locator) -> None:
        selected = tab.get_attribute(name = "aria-selected", timeout = self.TIMEOUT_SHORT)
        if selected == 'true':
            return
        tab.click()
        self._no_results()

    def _is_tab_selected(self, tab: Locator) -> bool:
        selected = tab.get_attribute(name = "aria-selected", timeout = self.TIMEOUT_SHORT)
        return selected == 'true'

    def switch_tab_to_all_locations(self):
        self._switch_tab(self.tab_locations)

    def switch_tab_to_near_me(self):
        self._switch_tab(self.tab_near_me)

    def switch_tab_to_ocean(self):
        self._switch_tab(self.tab_ocean)

    def tab_all_locations_selected(self) -> bool:
        return self._is_tab_selected(self.tab_locations)

    def tab_near_me_selected(self) -> bool:
        return self._is_tab_selected(self.tab_near_me)

    def tab_ocean_selected(self) -> bool:
        return self._is_tab_selected(self.tab_ocean)

    def get_listing_location(self, id: int) -> str:
        text_location = self.page.locator("//div[@id='properties-list']//a["+str(id)+"]/div[contains(@class,'card')]/following-sibling::div/div[1]")
        return text_location.text_content() if text_location.is_visible() == True else ""

    def get_listing_name(self, id: int) -> str:
        text_name = self.page.locator("//div[@id='properties-list']//a["+str(id)+"]/div[contains(@class,'card')]/following-sibling::div/div[2]")
        return text_name.text_content() if text_name.is_visible() == True else ""

    def get_listing_available_days(self, id: int) -> {date, date}:
        text_available_days = self.page.locator("//div[@id='properties-list']//a["+str(id)+"]//span[contains(text(),'Next available:')]/following-sibling::span")
        if text_available_days.is_visible():
            available_days = text_available_days.text_content()
            if len(available_days) != 0:
                start_date_str = available_days.split(" to ",1)[0]
                end_date_str = available_days.split(" to ",1)[1]
                start_date = datetime.strptime(start_date_str, '%b %d').date()
                end_date = datetime.strptime(end_date_str, '%b %d').date()
                return {start_date, end_date}
            else:
                return None
        else:
            return None
        #return text_available_days.text_content() if text_available_days.is_visible() == True else ""

    def get_listing_bedrooms(self, id: int) -> int:
        text_bedrooms = self.page.locator("//div[@id='properties-list']//a["+str(id)+"]//span[contains(text(),'Next available:')]/following-sibling::div/span[1]")
        return int(text_bedrooms.text_content()) if text_bedrooms.is_visible() == True else -1

    def get_listing_washrooms(self, id: int) -> int:
        text_washrooms = self.page.locator("//div[@id='properties-list']//a["+str(id)+"]//span[contains(text(),'Next available:')]/following-sibling::div/span[2]")
        return int(text_washrooms.text_content()) if text_washrooms.is_visible() == True else -1

    def get_listing_guest_limit(self, id: int) -> int:
        text_guests = self.page.locator("//div[@id='properties-list']//a[" + str(
            id) + "]//span[contains(text(),'Next available:')]/following-sibling::div/span[3]")
        return int(text_guests.text_content()) if text_guests.is_visible() == True else -1

    def _no_results(self) -> bool:
        if self.text_no_results.is_visible(timeout = self.TIMEOUT_SHORT) or self.text_no_match.is_visible(timeout = self.TIMEOUT_SHORT):
            return True
        listings = self.page.locator("//div[@id='properties-list']/a").all()
        #expect(listings).not_to_have_count(0, timeout = self.TIMEOUT_LONG)
        expect(self.card_listing).not_to_have_count(0, timeout = self.TIMEOUT_LONG)
        listings = self.page.locator("//div[@id='properties-list']/a").all()
        return len(listings) == 0

    def listing_count(self):
        listings = self.page.locator("//div[@id='properties-list']/a").all()
        if len(listings) > 1:
            return len(listings)
        if self._no_results():
            return 0
        else:
            listings = self.page.locator("//div[@id='properties-list']/a").all()
            return len(listings)

    def available_listing_count(self) -> int:
        available_listings = self.page.locator("//div[@id='properties-list']/a[not(preceding-sibling::h2[text()='Unavailable'])]").all()
        if len(available_listings) > 1:
            return len(available_listings)
        if self._no_results():
            return 0
        else:
            available_listings = self.page.locator("//div[@id='properties-list']/a[not(preceding-sibling::h2[text()='Unavailable'])]").all()
            return len(available_listings)

    def unavailable_listing_count(self) -> int:
        unavailable_listings = self.page.locator(
            "//div[@id='properties-list']/h2[text()='Unavailable']/following-sibling::a").all()
        if len(unavailable_listings) > 1:
            return len(unavailable_listings)
        if self._no_results():
            return 0
        else:
            unavailable_listings = self.page.locator(
                "//div[@id='properties-list']/h2[text()='Unavailable']/following-sibling::a").all()
            return len(unavailable_listings)

    def no_matching_results(self) -> bool:
        return self.text_no_match.is_visible()

    def search(self, keyword: str) -> None:
        self.input_search.fill(keyword)
        self.page.keyboard.press("Enter")
        try:
            expect(self.card_listing).to_have_count(0, timeout=self.TIMEOUT_MEDIUM)
        except AssertionError:
            pass

        self._no_results()

    def clear_search(self):
        if self.button_clear_search_content.is_visible():
            self.button_clear_search_content.click()

    def get_searched_timeline(self) -> None:
        if self.text_searched_timeline.is_visible():
            return self.text_searched_timeline.text_content()
        return None

    def filter_by_date(self, start_date: date, end_date: date):
        pass

    def get_filter_period(self):
        pass

    def get_searched_guess_limit(self) -> int:
        if self.text_searched_guests.is_visible():
            guests_count = self.text_searched_guests.text_content().split(" ")
            return int(guests_count[0])
        else:
            return -1