from django.shortcuts import render, redirect
from users.models import (
    Booking,
    HandymanProfile,
    Handyman,
    Client,
    ClientProfile,
    Schedule,
)
from django.contrib.auth.decorators import login_required
from users.forms import CreateScheduleForm, UpdateScheduleForm
from django.contrib import messages
from datetime import datetime

# calender


# Create your views here.
@login_required
def handyman_home(request):
    context = {
        "title": "Home",
    }
    return render(request, "handyman/dashboard.html", context)


@login_required
def display_map(request):
    context = {
        "title": "Map",
    }
    return render(request, "handyman/map.html", context)


@login_required
def handyman_dashboard(request):
    pending_bookings = Booking.objects.filter(
        handyman=request.user, status="Pending"
    ).count()
    all_booking = Booking.objects.filter(handyman=request.user).count()
    confirmed_bookings = Booking.objects.filter(
        handyman=request.user, status="Confirmed"
    ).count()
    cancelled_bookings = Booking.objects.filter(
        handyman=request.user, status="Cancelled"
    ).count()

    context = {
        "title": "Dashboard",
        "pending": pending_bookings,
        "all": all_booking,
        "confirmed": confirmed_bookings,
        "cancelled": cancelled_bookings,
        # 'booking_list' : booking_list
    }
    return render(request, "handyman/dashboard.html", context)


@login_required
def all_bookings(request):
    # booking.client = request.user.client

    bookings = Booking.objects.filter(handyman=request.user)

    context = {"title": "Bookings", "bookings": bookings}
    return render(request, "handyman/bookings_list.html", context)


@login_required
def booking_details(request, pk):
    booking = Booking.objects.get(pk=pk)

    context = {"title": "Booking details", "booking": booking}
    return render(request, "handyman/booking_details.html", context)


@login_required
def view_profile(request, pk):
    handyman = Handyman.objects.get(pk=pk)
    profile = HandymanProfile.objects.get(user=handyman)

    context = {"title": "Profile", "profile": profile}
    return render(request, "users/profile/handyman.html", context)


@login_required
def accept_booking(request, pk):
    # getting booking
    booking = Booking.objects.get(pk=pk)

    booking.status = "Confirmed"
    booking.save()
    messages.success(request, "Booking has been approved. Proceed to do the task")
    return redirect("handyman:bookings-list")


@login_required
def decline_booking(request, pk):
    # get handyman
    handyman = Handyman.objects.get(pk=request.user.id)
    # get handyman schedule
    schedule = Schedule.objects.get(handyman=handyman)
    booking = Booking.objects.get(pk=pk, schedule=schedule)

    booking.status = "Cancelled"
    # remove booking from Schedule
    booking.schedule = None
    messages.success(
        request, "Booking has been successfully declined & removed from your schedule"
    )
    booking.save()

    return redirect("handyman:bookings-list")


# pending bookings
@login_required
def pending_bookings(request):
    bookings = Booking.objects.filter(handyman=request.user, status="Pending")
    context = {"title": "Pending Bookings", "bookings": bookings}
    return render(request, "handyman/pending_bookings.html", context)


# accepted bookings
@login_required
def confirmed_bookings(request):
    bookings = Booking.objects.filter(handyman=request.user, status="Confirmed")
    context = {"title": "Confirmed Bookings", "bookings": bookings}
    return render(request, "handyman/confirmed_bookings.html", context)


# declined bookings
@login_required
def cancelled_bookings(request):
    bookings = Booking.objects.filter(handyman=request.user, status="Cancelled")
    context = {"title": "cancelled Bookings", "bookings": bookings}
    return render(request, "handyman/cancelled_bookings.html", context)


# client details
@login_required
def client_details(request, pk):
    client = Client.objects.get(pk=pk)
    profile = ClientProfile.objects.get(user=client)
    context = {"title": "Client Details", "client": client, "profile": profile}
    return render(request, "handyman/client_details.html", context)


@login_required
def create_schedule(request):
    if request.method == "POST":
        form = CreateScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.handyman = request.user.handyman
            schedule.save()

            messages.success(request, "Schedule successfully created!")
        else:
            messages.warning(request, "Invalid dates, pleases select another date")
    form = CreateScheduleForm()

    context = {"title": "Create Schedule", "form": form}
    return render(request, "handyman/create_schedule.html", context)


@login_required
def update_schedule(request, pk):
    schedule = Schedule.objects.get(pk=pk)

    if request.method == "POST":
        form = UpdateScheduleForm(request.POST, instance=schedule)

        if form.is_valid():
            form.save()
            messages.success(request, "Schedule has been successfully updated")
            # to be changed
            return redirect('handyman:bookings-list')
        else:
            messages.warning(request, 'Failed to update the schedule, Please Try again')
    else: 
        form = UpdateScheduleForm(instance=schedule)

    context = {"title": "Update Schedule"}
    return render(request, "handyman/update_schedule.html", context)


