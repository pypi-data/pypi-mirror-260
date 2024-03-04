import requests
import logging

class AndromedaClient:
    

    def __init__(self, base_url, username, password):

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'}
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.headers.update(headers)

    def divide_chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]


    def paginate(self, method, url, params=None, payload=None):
        """Handle pagination for GET and POST requests."""
        if params is None:
            params = {"page": 0}
        else:
            params["page"] = 0

        result = []

        while True:
            if method.lower() == 'get':
                res = self.session.get(url, params=params)
            elif method.lower() == 'post':
                res = self.session.post(url, json=payload, params=params)
            res.raise_for_status()
            try:
                data = res.json()
            except ValueError:
                break
            result.extend(data)
            params["page"] += 1

            if len(data) < 1000:
                break

        return result

    def get(self, url_path, params=None):
        """Send a GET request and return the response data."""
        url = self.base_url + url_path
        logging.info(f"Almost-NGSI-LD: GETting from {url}")
        res = self.session.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        if isinstance(data, dict) or len(data) < 1000:
            return data
        logging.info("Too many results, start retrieving pages!")
        return self.paginate('get', url, params=params)

    def put(self, url_path, payload, params=None):
        """Send a PUT request with the given payload."""
        url = self.base_url + url_path
        if isinstance(payload, list) and len(payload) > 1000:
            logging.info(f"Almost-NGSI-LD: Payload too big, start chunking. PUTting to {url}")
            for chunk in self.divide_chunks(payload, 200):
                res = self.session.put(url, json=chunk, params=params)
                res.raise_for_status()
                logging.info(res.status_code)
                logging.info(res.text)
        else:
            logging.info(f"Almost-NGSI-LD: PUTting to {url}")
            res = self.session.put(url, json=payload, params=params)
            res.raise_for_status()
            logging.info(res.status_code)
            logging.info(res.text)

    def post(self, url_path, payload, params=None):
        """Send a POST request with the given payload and return the response data."""
        url = self.base_url + url_path
        res = self.session.post(url, json=payload, params=params)
        res.raise_for_status()
        data = res.json()
        if isinstance(data, dict) or len(data) < 1000:
            return data
        logging.info("Too many results, start retrieving pages!")
        return self.paginate('post', url, params=params, payload=payload)