from django.urls import path
from . import views

app_name = "client"

urlpatterns = [
    path("", views.index, name="home-page"),
    path("client-home/", views.display_client_home, name="client-home"),
    path("display-map/", views.display_map, name="display-map"),
    # booking
    path("make-booking/<int:pk>", views.make_booking, name="make-booking"),
    path(
        "available-handymen/", views.show_available_handyman, name="available-handymen"
    ),
    path(
        "handyman-details/<int:pk>",
        views.selected_handyman_details,
        name="handyman-details",
    ),
    # profile
    path("client-profile/<int:pk>", views.view_profile, name="client-profile"),
    # get location
    path("get-location/", views.get_location, name="get-location"),
    path("set-users-location/", views.users_location, name="set-users-location"),
    # make review
    path("make-review/<int:pk>", views.make_review, name="make-review"),
    # Bookings
    # all
    # path("all-bookings/", views.all_bookings, name="all-bookings"),
    path("pending-bookings/", views.pending_bookings, name="pending-bookings"),
    path("confirmed-bookings/", views.confirmed_bookings, name="confirmed-bookings"),
    path("cancelled-bookings/", views.cancelled_bookings, name="cancelled-bookings"),
    # project bookings
    path("project-bookings/", views.project_bookings, name="project-bookings"),
    # Search for service
    path("search-service/", views.seacrh_service, name="search-service"),
    # booking details
    path("booking-details/<int:pk>", views.booking_details, name="booking-details"),
    # update booking
    path("update-booking/<int:pk>", views.update_booking, name="update-booking"),
    path("delete-booking/<int:pk>", views.delete_booking, name="delete-booking"),
]
