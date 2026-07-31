# This file is used to cross check and validate the input of th country code

import re


class Country:

    def __init__(self, code):
        code = code.strip().upper()  

        if not re.fullmatch(r"[A-Z]{2}", code):
            raise ValueError(f"Invalid country code '{code}'. Use a 2-letter code like NG, US, or GB.")
        # This is used to make sure it is in the correct patern like making sure the country code in 2 letters and gives a responds the input is wrong
        self.code = code
