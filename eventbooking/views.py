from django.shortcuts import render,redirect
from .models import Event,Booking,Ticket
from .forms import TicketBookingForm,PaymentForm
import datetime

def home_page(request):
	events=Event.objects.all()
	cities=Event.objects.values('city').distinct()
	context={"events":events,"cities":cities}
	return render(request,'eventbooking/home.html',context)

def event_page(request,event_id):
	event= Event.objects.get(id=event_id)
	context={"event":event}

	return render(request,'eventbooking/events.html',context)


def ticket_booking(request,event_id):

	event=Event.objects.get(id=event_id)
	if request.method=="POST":
		form=TicketBookingForm(request.POST)
		if form.is_valid():
			no_of_person=form.cleaned_data["no_of_per"]
			booking=Booking.objects.create(
				amount=event.event_price* no_of_person,
				no_of_person=no_of_person,
				event=event
				)
			
			return redirect('payment',booking_id=booking.id)
	
	form=TicketBookingForm()
	context={"form":form,"event":event}
	return render(request,"eventbooking/ticket_book.html",context)

def payment(request,booking_id):
	booking=Booking.objects.get(id=booking_id)

	if request.method=="POST":
		form=PaymentForm(request.POST)
		if form.is_valid():
			payment_method=form.cleaned_data['payment_method']
			ticket=Ticket.objects.create(
				booking=booking,
				date_booked=datetime.date.today(),
				user = request.user,
				payment_method = payment_method
				)
			event_seat=Event.objects.get(id=booking.event.id).seats
			event_seat=event_seat-booking.no_of_person
			Event.objects.filter(id=booking.event.id).update(seats=event_seat)
				
			return redirect('ticket_confirm',ticket_id=ticket.id)
	
	form=PaymentForm()
	context={"form":form,"booking":booking}
	return render(request,'eventbooking/payment.html',context)


def ticket_confirm(request,ticket_id):
	ticket=Ticket.objects.get(id=ticket_id)
	return render(request,'eventbooking/ticket_confirm.html',{"ticket":ticket})