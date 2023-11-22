import requests
from project.settings import GOOGLE_MAPS_API_KEY
from django.shortcuts import render, redirect
from users.models import (
    Handyman,
    HandymanProfile,
    Client,
    ClientProfile,
    Location,
    Schedule,
    Booking,
)
from users.forms import BookingForm, GetLocationForm, MakeRatingForm, UpdateBookingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

# Search imports
from geopy.distance import geodesic
# import geopy
import folium
import geocoder
from folium.plugins import LocateControl


# Create your views here.

API_KEY = GOOGLE_MAPS_API_KEY


# main home
def index(request):
    context = {
        "title": "Home",
    }
    return render(request, "base/index/index.html", context)


test = [
    {"description": "test data", "date": "2023-08-01"},
    {"description": "test2", "date": "2023-08-06"},
]


@login_required
# client home
def display_client_home(request):
    bookings_list = (
        Booking.objects.all().filter(client=request.user).values("description", "date")
    )

    events = []
    for description, date in bookings_list:
        events.append(
            {
                "title": description,
                "start": date,
            }
        )

    all_bookings = Booking.objects.all().filter(client=request.user).count()
    pending_bookings = Booking.objects.filter(
        client=request.user, status="Pending"
    ).count()
    cancelled_bookings = Booking.objects.filter(
        client=request.user, status="Cancelled"
    ).count()
    confirmed_bookings = Booking.objects.filter(
        client=request.user, status="Confirmed"
    ).count()

    context = {
        "title": "Home",
        "all": all_bookings,
        "pending": pending_bookings,
        "cancelled": cancelled_bookings,
        "confirmed": confirmed_bookings,
        "events": events,
    }
    return render(request, "client/dashboard.html", context)


# show available handymen
@login_required
def show_available_handyman(request):
    handymen = Handyman.objects.all()

    if handymen is None:
        messages.warning(request, "There no available handymen in your region")
    else:
        context = {"title": "Handyman List", "handymen": handymen}
        return render(request, "client/handyman_list.html", context)


@login_required
# Show selected handyman details
def selected_handyman_details(request, pk):
    handyman = Handyman.objects.get(pk=pk)
    profile = HandymanProfile.objects.get(user=handyman.pk)

    context = {"title": "Details", "handyman": handyman, "profile": profile}
    return render(request, "client/handman_details.html", context)


# display map
@login_required
def display_map(request):
    # get handymen lcoations
    locations = list(Location.objects.values("latitude", "longitude"))

    address = geocoder.osm("Kampala")
    latitude = address.lat
    longitude = address.lng

    # Using folium
    m = folium.Map(location=[0.347596, 32.582520], zoom_start=16)
    folium.Marker([latitude, longitude], tolltip="Click for more").add_to(m)

    for location in locations:
        folium.Marker(
            [location["latitude"], location["longitude"]], tolltip="Click for more"
        ).add_to(m)

    folium.plugins.LocateControl().add_to(m)

    # new_location =

    # Get HTML representation
    m = m._repr_html_()
    # m = save()

    context = {"title": "Map", "m": m}
    return render(request, "client/map.html", context)


# create make a booking
@login_required
def make_booking(request, pk):
    handyman = Handyman.objects.get(pk=pk)
    profile = HandymanProfile.objects.get(user=handyman)
    schedule = Schedule.objects.get(handyman=handyman)

    if request.method == "POST":
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.date = request.POST["date"]

            # Convert date into datetime object
            booking_date = datetime.strptime(booking.date, "%Y-%m-%d").date()

            # Check if the schedule exists.
            if schedule is None:
                messages.warning(request, "The handyman is not available for booking")
            else:
                # Check if thee booking date is within the handyman's schedule start & end dates
                start = schedule.start_date <= booking_date
                end = schedule.end_date >= booking_date
                if start and end:
                    bookings = Booking.objects.filter(
                        date=booking.date, schedule=schedule
                    )
                    # Check if date is already booked
                    if len(bookings) == 0:
                        booking.service = profile.service
                        booking.schedule = schedule
                        booking.client = request.user.client
                        booking.handyman = handyman
                        booking.save()
                        messages.success(request, "Booking successfully made!")
                        return redirect("client:client-home")
                    else:
                        messages.warning(
                            request,
                            "Booking date is already taken, Please choose another date",
                        )
                        return redirect("client:available-handymen")
                else:
                    messages.warning(
                        request,
                        "Booking date is not available, Please choose another date within this week",
                    )
                    return redirect("client:available-handymen")

    else:
        form = BookingForm()

    context = {"title": "Booking", "form": form}
    return render(request, "client/make_booking.html", context)


# Profile
@login_required
def view_profile(request, pk):
    client = Client.objects.get(pk=pk)
    profile = ClientProfile.objects.get(user=client)

    context = {"title": "Profile", "profile": profile}
    return render(request, "users/profile/client.html", context)


# display the users location
@login_required
def users_location(request):
    context = {
        "title": "Location",
    }
    return render(request, "client/set_location.html", context)


# get users location
@login_required
def get_location(request):
    # Make a request to the Google Maps Geolocation API
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key={}".format(API_KEY)

    response = requests.post(url)

    # Check for errors
    if response.status_code != 200:
        messages.warning(request, "Error getting lcoation")
        raise Exception("Error getting location: {}".format(response.status_code))

    # Parse the response
    data = response.json()
    latitude = data["location"]["lat"]
    longitude = data["location"]["lng"]
    # accuracy = data["accuracy"]

    # Save to database the coordinates
    location = Location.objects.create(longitude=longitude, latitude=latitude)
    location.save()

    messages.success(request, "Your location has been saved successfully!")

    context = {
        "latitude": latitude,
        "longitude": longitude,
    }
    return render(request, "client/get_location.html", context)


# make a review
@login_required
def make_review(request, pk):
    handyman = Handyman.objects.get(pk=pk)
    handyman_profile = HandymanProfile.objects.get(user=handyman)

    if request.method == "POST":
        form = MakeRatingForm(request.POST)
        if form.is_valid():
            pre_form = form.save(commit=False)
            pre_form.handyman = handyman_profile
            pre_form.client = request.user.client
            pre_form.save()
            messages.success(request, "You have succeffully Reviews the handyman")
            return redirect("client:available-handymen")
    else:
        form = MakeRatingForm()

        context = {"title": "Make Review", "form": form}
        return render(request, "client/make_review.html", context)


@login_required
def pending_bookings(request):
    bookings = Booking.objects.filter(client=request.user, status="Pending")
    context = {"title": "Pending Bookings", "pending_bookings": bookings}
    return render(request, "client/pending_bookings.html", context)


@login_required
def confirmed_bookings(request):
    bookings = Booking.objects.filter(client=request.user, status="Confirmed")
    context = {"title": "Confirmed Bookings", "confirmed_bookings": bookings}
    return render(request, "client/confirmed_bookings.html", context)


@login_required
def cancelled_bookings(request):
    bookings = Booking.objects.filter(client=request.user, status="Cancelled")
    context = {"title": "Confirmed Bookings", "cancelled_bookings": bookings}
    return render(request, "client/cancelled_bookings.html", context)


@login_required
def project_bookings(request):
    bookings = Booking.objects.filter(client=request.user)
    context = {"title": "Project bookings", "bookings": bookings}
    return render(request, "client/project_bookings.html", context)


@login_required
def seacrh_service(request):
    # Handles the request from the user
    if request.method == "POST":
        search = request.POST["search"]

        # Client location
        client_profile = ClientProfile.objects.get(user=request.user)
        client_location = (client_profile.location.latitude, client_profile.location.longitude)

        # first service = FK in handyman profile, second __service = Char field in Service Model & __icontains is to make partial queries [not exact match]
        handymen = HandymanProfile.objects.filter(service__service__icontains=search)

        # code that determines handymen providing a service within a 5km radius of the client goes here
        nearby_handymen =[]
        for handyman_profile in handymen:
            handyman_location = (handyman_profile.location.latitude, handyman_profile.location.longitude)
            distance_to_client = geodesic(client_location, handyman_location).kilometers

            if distance_to_client <= 2:
                nearby_handymen.append(handyman_profile)

        # Generate folium map with markers for nearby handymen
        m = folium.Map(location=client_location, zoom_start=20)
        folium.Marker(client_location, popup=client_profile.user.username).add_to(m)


        for handyman_profile in nearby_handymen:
            handyman_location = (handyman_profile.location.latitude, handyman_profile.location.longitude)
            folium.Marker(handyman_location, popup=handyman_profile.user.username).add_to(m)

        # Get HTML representation
        m = m._repr_html_()

        # Notifies the user incase their is no hadyman
        if not handymen:
            messages.warning(
                request, "Sorry, Their is no handyman providing this service"
            )

        context = {"title": "Seacrh for service", "handymen": handymen, 'm':m, 'nearby_handymen':nearby_handymen}
        return render(request, "client/new_project_booking.html", context)

    else:
        return render(
            request, "client/new_project_booking.html", {"title": "Search for service"}
        )


@login_required
def booking_details(request, pk):
    booking = Booking.objects.get(pk=pk)

    context = {"title": "Booking Details", "booking": booking}
    return render(request, "client/booking_details.html", context)


@login_required
def update_booking(request, pk):
    booking = Booking.objects.get(pk=pk)

    if request.method == "POST":
        form = UpdateBookingForm(request.POST, request.FILES, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your booking has been successfully updated")
            return redirect("client:booking-details", booking_id=booking.id)
        else:
            messages.warning(
                request, f"Failed to update booking details, Please try again"
            )
    else:
        form = UpdateBookingForm(instance=booking)

    context = {"title": "Update Booking", "form": form}
    return render(request, "client/update_booking.html", context)


@login_required
def delete_booking(request, pk):
    booking = Booking.objects.get(pk=pk)

    booking.delete()
    messages.success(request, "Booking successfully deleted")
    return redirect("client:project-bookings")
