from django.urls import path

from rest_framework_swagger.views import get_swagger_view

from api.views import ListingView, NeighbourListing

schema_view = get_swagger_view(title="Pass the Key API")

urlpatterns = [
    path("outcode/<str:outcode>", ListingView.as_view()),
    path("nexus/<str:request_postcode>", NeighbourListing.as_view()),
    path("swagger/", schema_view),
]
