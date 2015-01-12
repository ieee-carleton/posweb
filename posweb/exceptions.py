#!/usr/bin/python
class Error(Exception):
    """Base class for exceptions in POSWeb."""
    pass

class InvalidItemError(Error):
    def __init__(self, message):
        self.message = message

class ItemLookupError(Error):
    def __init__(self, item_id):
        self.message = message