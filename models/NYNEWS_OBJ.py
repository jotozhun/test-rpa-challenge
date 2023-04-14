from RPA.Browser.Selenium import Selenium

class NYNEWS_OBJ:
    """
    This class represents the nytimes webpage, provides methods
    for handling some of actions in this webpage
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.browser_lib = Selenium()
        self.__initialize()


    def __initialize(self):
        """
        This method opens any web browser available, recommended chrome
        """
        self.browser_lib.open_chrome_browser(self.url)
        self.browser_lib.maximize_browser_window()
        self.browser_lib.set_browser_implicit_wait(value=5.0)


    def search_for(self, word, css_exp="css:input.css-1j26cud"):
        """
        This method finds an input, enters data and presses ENTER Key
        """
        self.browser_lib.input_text(css_exp, word)
        self.browser_lib.press_keys(css_exp, "ENTER")


    def click_on_btn(self, css_exp="css:button.css-tkwi90.e1iflr850"):
        """
        This method finds a button with the css expression and performs
        the click action
        """
        self.browser_lib.click_button(css_exp)


    def click_on_element(self, css_exp: str):
        """
        This method finds any element with the css expression and performs
        the click action
        """
        self.browser_lib.click_element(css_exp)


    def quit_browsers(self):
        """
        This method closes all the active sessions of this object
        """
        self.browser_lib.close_all_browsers()


    def press_key(self, css_exp: str, key_name: str):
        """
        This method performs a key action in a specific web element
        """
        self.browser_lib.press_keys(css_exp, key_name)


    def wait_for_element_to_be_present(self, css_exp: str):
        """
        This method holds for a while until an specific element
        renders in the webpage
        """
        self.browser_lib.wait_until_element_is_visible(css_exp)
