#!/usr/bin/python
class Error(Exception):
    """Base class for exceptions in POSWeb."""
    pass

class InvalidItemError(Error):
    def __init__(self):
        self.message = "Invalid item specified"
		self.id = -2
		
class ItemLookupError(Error):
    def __init__(self):
        self.message = "Error looking up an item"
		self.id = -3
		
class DiscountCodeError(Error):
    def __init__(self, code):
        self.message = "Invalid discount code" % code
		self.id = -4