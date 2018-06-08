class Exchange:

    def __init__(self, endpoint, api_key, api_secret):
        """
        constructor
        :param endpoint: general address of api requests
        :param api_key: account api key
        :param api_secret: account api secret
        """
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_secret = api_secret
