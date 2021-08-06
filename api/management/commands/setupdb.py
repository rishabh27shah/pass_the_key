import csv
import os

from django.core.management.base import BaseCommand

from api.models import Listing


class Command(BaseCommand):
    def handle(self, *args, **options):
        listing_list = []
        with open(os.environ.get("RESOURCE_PATH"), "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            column_names = []
            for row in csv_reader:
                column_names = row
                break
            next(csv_reader, None)  # skip the headers
            for row in csv_reader:
                listing_id, name, profile_url, street, zipcode, weekly_price = (
                    row[0],
                    row[4],
                    row[7],
                    row[46],
                    row[49],
                    row[57],
                )

                # Data cleaning process, skipped rows with blank entries of weekly_price and zipcode.
                if weekly_price == "" or zipcode == "":
                    continue
                weekly_price = float(weekly_price.replace(",", "")[1:])

                # if price coulmn exist in csv, we will use it, else store weekly_price / 7
                daily_price = (
                    float(
                        row[column_names.index("price")].replace(
                            ",", ""
                        )[1:]
                    )
                    if "price" in column_names
                    else weekly_price / 7
                )
                postcode = zipcode.replace(" ", "")
                outcode = zipcode.split(" ")[0]
                listing_list.append(
                    Listing(
                        listing_id=listing_id,
                        name=name,
                        profile_url=profile_url,
                        street=street,
                        zipcode=postcode,
                        outcode=outcode,
                        daily_price=daily_price,
                        weekly_price=weekly_price,
                    )
                )
            Listing.objects.bulk_create(
                listing_list, ignore_conflicts=True
            )
