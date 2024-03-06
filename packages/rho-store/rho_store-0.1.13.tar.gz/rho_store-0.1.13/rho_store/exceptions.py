
class RhoStoreError(Exception):
    """ Base exception """
    pass


class NotFound(Exception):
    pass


class RhoApiError(RhoStoreError):
    pass


class InvalidApiKey(RhoStoreError):
    pass
