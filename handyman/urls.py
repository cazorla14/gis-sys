from django.urls import path
from . import views

app_name = "handyman"

urlpatterns = [
    path("handyman-home/", views.handyman_home, name="handyman-home"),
    path("display-map/", views.display_map, name="display-map"),
    path("handyman-dashboard", views.handyman_dashboard, name="handyman-dashboard"),
    # bookings list or all bookings
    path("bookings-list/", views.all_bookings, name="bookings-list"),
    path("booking-details/<int:pk>", views.booking_details, name="booking-details"),
    path("handyman-profile/<int:pk>", views.view_profile, name="handyman-profile"),
    # ====================================================== Bookings ======================================================
    # Accept booking
    path("accept-booking/<int:pk>", views.accept_booking, name="accept-booking"),
    # Decline booking
    path("decline-booking/<int:pk>", views.decline_booking, name="decline-booking"),
    # Pending bookings
    path("pending-bookings/", views.pending_bookings, name="pending-bookings"),
    # confirmed bookings
    path("confirmed-bookings/", views.confirmed_bookings, name="confirmed-bookings"),
    # declined bookings
    path("cancelled-bookings/", views.cancelled_bookings, name="cancelled-bookings"),
    # client details
    path("client-details/<int:pk>", views.client_details, name="client-details"),
    # create schedule
    path('create-schedule/', views.create_schedule,name='create-schedule'),
    # view schedule
    # path('view-schedule/<int:pk>', views.calendar_schedule, name='view-schedule')
]
