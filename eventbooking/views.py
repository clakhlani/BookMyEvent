from django.shortcuts import render,redirect
from .models import Event,Booking,Ticket
from .forms import TicketBookingForm,PaymentForm,EventCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
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

@login_required(login_url='login_page')
def ticket_booking(request,event_id):

	event=Event.objects.get(id=event_id)
	if request.method=="POST":
		form=TicketBookingForm(request.POST)
		if form.is_valid():
			no_of_person=form.cleaned_data["no_of_per"]
			
			if no_of_person == 0:
				messages.error(request,'Please enter 1 or more Number Of Person')
				return redirect('ticket_book',event_id=event_id)

			if no_of_person > event.seats:
				if event.seats == 0:
					messages.error(request,'Sorry No Seats Available')
				else:
					messages.error(request,f'Please select seats upto {event.seats}.')
				return redirect('ticket_book',event_id=event_id)
			if datetime.datetime.now().time() > event.time and datetime.date.today() >= event.date :
				messages.error(request,'Booking time is over.Event started.')
				return redirect('ticket_book',event_id=event_id)
			

			
			booking=Booking.objects.create(
				amount=event.event_price* no_of_person,
				no_of_person=no_of_person,
				event=event
				)
			
			return redirect('payment',booking_id=booking.id)
	
	form=TicketBookingForm()
	context={"form":form,"event":event}
	return render(request,"eventbooking/ticket_book.html",context)


@login_required(login_url='login_page')
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


@login_required(login_url='login_page')
def ticket_confirm(request,ticket_id):
	ticket=Ticket.objects.get(id=ticket_id)
	return render(request,'eventbooking/ticket_confirm.html',{"ticket":ticket})


@login_required(login_url='login_page')
def my_tickets(request):
	tickets=Ticket.objects.filter(user=request.user)
	return render(request,'eventbooking/my_tickets.html',{"tickets":tickets})

#@login_required(login_url='login_page')
@user_passes_test(lambda user: user.is_active and user.is_superuser, login_url='logout')
def create_event(request):
	if request.method=='POST':
		form=EventCreationForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect('home')


	form = EventCreationForm()
	return render(request,'eventbooking/event_creation.html',{"form":form})


@user_passes_test(lambda user: user.is_active and user.is_superuser, login_url='logout')
def update_event(request,event_id):
	event=Event.objects.get(id=event_id)


	form=EventCreationForm(instance=event)
	return render(request,'eventbooking/event_creation.html',{'form':form})