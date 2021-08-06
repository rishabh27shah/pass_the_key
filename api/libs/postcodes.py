import requests


class PostcodeAPI:
    API_BASE_URL = "https://api.postcodes.io"

    def get_neighbour(self, postcode):
        """
        get_neighbours : Used to fetch details of nearest postcodes
        """
        url = "%s/postcodes/%s/nearest" % (self.API_BASE_URL, postcode)
        response = requests.get(url)
        json_response = response.json()
        result = [[postcode], {postcode: 0}]
        if json_response["status"] != 200:
            return result

        for listing in json_response["result"]:
            fetch_postcode = listing["postcode"].replace(" ", "")
            result[0].append(fetch_postcode)
            result[1][fetch_postcode] = listing["distance"]

        return result
