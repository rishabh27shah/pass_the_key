import xmltodict

from django.db.models import Avg, Count
from rest_framework import status
from rest_framework.test import APITestCase

from api.libs.postcodes import PostcodeAPI
from api.management.commands import setupdb
from .models import Listing


class APITest(APITestCase):
    """
        APITest : for testing API endpoints.
    """

    def setUp(self):
        cmd = setupdb.Command()
        cmd.handle()

    def test_outcode_list(self):
        """
        test_outcode_list : test /api/outcode/<outcode>/ endpoint
        """
        company_object = Listing.objects.all().first()
        response = self.client.get(
            "/api/outcode/" + company_object.outcode
        )
        outcode_set = Listing.objects.filter(
            outcode=company_object.outcode
        )
        average_daily_rate = "{:.2f}".format(
            outcode_set.all().aggregate(avg=Avg("daily_price"))["avg"]
        )
        self.assertEqual(
            xmltodict.parse(response.content)["outcode"][
                "@average-daily-rate"
            ],
            str(average_daily_rate),
        )
        self.assertEqual(
            xmltodict.parse(response.content)["outcode"][
                "@listing-count"
            ],
            str(outcode_set.count()),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_nearest_postcode(self):
        """
        test_nearest_postcode : test /api/nexus/<postcode>/ endpoint
        """
        response = self.client.get("/api/nexus/M46JA")
        postcodes_list, distance = PostcodeAPI().get_neighbour("M46JA")
        zipcodes = (
            Listing.objects.filter(zipcode__in=postcodes_list)
            .values("zipcode")
            .annotate(count=Count("id"))
            .annotate(average=Avg("daily_price"))
        )
        listing_count = 0
        average_daily_rate = 0
        for zipcode in zipcodes:
            listing_count += zipcode["count"]
            average_daily_rate += zipcode["average"]

        average_daily_rate = (
            0.00
            if len(zipcodes) == 0
            else "{:.2f}".format(average_daily_rate / len(zipcodes))
        )
        self.assertEqual(
            xmltodict.parse(response.content)["outcodes"][
                "@average-daily-rate"
            ],
            str(average_daily_rate),
        )
        self.assertEqual(
            xmltodict.parse(response.content)["outcodes"][
                "@listing-count"
            ],
            str(listing_count),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
