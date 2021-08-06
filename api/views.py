from django.db.models import Avg, Count
from django.http import HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Listing
from api.xml_renderer import XMLGenerator
from api.libs.postcodes import PostcodeAPI


class ListingView(APIView):
    renderer_classes = (XMLGenerator,)

    def get(self, request, outcode):
        listings = Listing.objects.filter(outcode=outcode)
        if listings.count() == 0:
            return HttpResponseNotFound()
        average_daily_rate = listings.all().aggregate(
            average=Avg("daily_price")
        )["average"]
        average_daily_rate = "{:.2f}".format(average_daily_rate)
        attribute = {
            "listing-count": str(listings.count()),
            "average-daily-rate": str(average_daily_rate),
        }
        XMLGenerator.startup("outcode", "", attribute)

        return Response({"outcode": outcode})


class NeighbourListing(APIView):
    renderer_classes = (XMLGenerator,)

    def get(self, request, request_postcode):
        listing_count = 0
        average_daily_rate = 0
        nearest_postcode = {}
        result = []

        postcodes_list, distance = PostcodeAPI().get_neighbour(
            request_postcode
        )
        zipcodes = (
            Listing.objects.filter(zipcode__in=postcodes_list)
            .values("zipcode")
            .annotate(count=Count("id"))
            .annotate(average=Avg("daily_price"))
        )

        # if no listings founds, will return 404
        if len(zipcodes) == 0:
            return HttpResponseNotFound()

        for zipcode in zipcodes:
            nearest_postcode[zipcode["zipcode"]] = {
                "listing-count": str(zipcode["count"]),
                "average-daily-rate": str(
                    "{:.2f}".format(zipcode["average"])
                ),
                "distance": str(distance[zipcode["zipcode"]]),
            }
            listing_count += zipcode["count"]
            average_daily_rate += zipcode["average"]
            result.append({"zipcode": zipcode["zipcode"]})

        average_daily_rate = "{:.2f}".format(
            average_daily_rate / len(zipcodes)
        )
        attribute = {
            "nexus": request_postcode,
            "listing-count": str(listing_count),
            "average-daily-rate": str(average_daily_rate),
        }
        XMLGenerator.startup(
            "outcodes", "outcode", attribute, nearest_postcode
        )

        return Response(result)
