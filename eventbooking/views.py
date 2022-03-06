from django.shortcuts import render,redirect
from .models import Event,Booking,Ticket
from .forms import TicketBookingForm,PaymentForm,EventForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
import datetime 

def home_page(request):
	'''View for homepage. Displays all the events.No login is required to view home page.
		User can click on events to get more details. User can also filter events depending on City and Genre.'''
	events=Event.objects.all()                                               #Getting all events from Database.
	cities=Event.objects.values('city').distinct()                           
	genres=Event.objects.values('event_type').distinct()                     #Getting distinct city and genre for particular events to be viewed.

	selected_city='ALL'
	selected_genre='ALL'

	if request.method=='POST':                                               #Getting the filter query					

		city=request.POST.get("City")
		genre=request.POST.get("Genre")

		if city !="ALL" and genre == "ALL":                                  #Different test cases for city and genre selected.   
			events=Event.objects.filter(city=city)
			selected_city=city

		elif genre != "ALL" and city == "ALL":
			events=Event.objects.filter(event_type=genre)
			selected_genre=genre

		elif city != "ALL" and genre != "ALL":
			events=Event.objects.filter(city=city).filter(event_type=genre)
			selected_city=city
			selected_genre=genre

	if events.count()==0:                                                    #If no matching events for city and genre selected show message. 
		messages.info(request,f'No Matching Events...')	
	context={"events":events,"cities":cities,"genres":genres,"selected_city":selected_city,"selected_genre":selected_genre}
	return render(request,'eventbooking/home.html',context)                   


def event_page(request,event_id):
	'''View to display all the information for the particular event selected.
		User also has option to Book the event . But login is required for it.
		Admin user can update events.'''
	event= Event.objects.get(id=event_id)            #Getting the event selected.
	context={"event":event}

	return render(request,'eventbooking/events.html',context)

@login_required(login_url='login_page')
def ticket_booking(request,event_id):
	'''View to book tickets for the event selected.
		User neds to enter the no of persons for the booking.
		Checks present if booking done for 0 person , no of person > seats available,all seats booked and booking window closed.
		Login is required.''' 
	event=Event.objects.get(id=event_id)

	if request.method=="POST":
		form=TicketBookingForm(request.POST)
		if form.is_valid():
			no_of_person=form.cleaned_data["no_of_person"]                               #Getting the no of persons entred by user
			
			if no_of_person == 0:                                                        #Checks for value entered.
				messages.error(request,'Please enter 1 or more Number Of Person')
				return redirect('ticket_book',event_id=event_id)

			if no_of_person > event.seats:
				if event.seats == 0:
					messages.error(request,'Sorry No Seats Available')
				else:
					messages.error(request,f'Please select seats upto {event.seats}.')
				return redirect('ticket_book',event_id=event_id)
			if (datetime.date.today() > event.date)   or (datetime.date.today()==event.date and datetime.datetime.now.time()> event.time):
				messages.error(request,'Booking time is over.Event started.')
				return redirect('ticket_book',event_id=event_id)
			
                                                                        
																		#If checks pased create a Booking entry
			booking=Booking.objects.create(
				amount=event.event_price* no_of_person,
				no_of_person=no_of_person,
				event=event
				)
			
			return redirect('payment',booking_id=booking.id)             #Redirect to payment page.
	
	form=TicketBookingForm()
	context={"form":form,"event":event}
	return render(request,"eventbooking/ticket_book.html",context)


@login_required
def cancel_ticket(request,ticket_id):
	'''View to cancel ticket. User can cancel tickt 24 hours before the event.
		Only user those whose bought the ticket can cancel it
		User asked before cancellation if they are sure they want to cancel ticket.
		Login is required.'''
	tickets = Ticket.objects.filter(id=ticket_id)                       #Getting the ticket to be cancelled.


	if tickets.count() == 0:											#Checks for verification
		messages.error(request,f'No Ticket Available !!!!')
		return render(request,'eventbooking/cancel_ticket.html')

	ticket=tickets.first()
			
	if request.user != ticket.user:
		messages.error(request,f'Unauthorized Access !!!!')
		return render(request,'eventbooking/cancel_ticket.html')

	timenow=datetime.datetime.now().time()
	daybefore=ticket.booking.event.date - datetime.timedelta(days=1)
	if (datetime.date.today() >= ticket.booking.event.date)   or (timenow > ticket.booking.event.time and datetime.date.today() == daybefore ):
		messages.error(request,f'Ticket cannot be cancelled. Less than 24 hours for the event.')
		return render(request,'eventbooking/cancel_ticket.html')
	
	
	
	if request.method=='POST':												#If user approves then ticket is cancelled.	
		event=Event.objects.get(id=ticket.booking.event.id)
		seats=ticket.booking.no_of_person
		event.seats=event.seats+seats
		event.save()
		ticket.delete()

		return redirect('mytickets')                                       #Redirect to my tickets page after cancellation.
	
	return render(request,'eventbooking/cancel_ticket.html',{"tickets": tickets}) 


@login_required(login_url='login_page')
def payment(request,booking_id):
	'''View for the payment of tickets for the event selected.
		User displayed details about the event and total amount to be paid.
		User is given a option to select from Online Wallet or Credit Card for payment.
		Login is required.'''
	booking=Booking.objects.get(id=booking_id) 
 
	if request.method=="POST":                                  #After payment is done by user a ticket is created.
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
				
			return redirect('ticket_confirm',ticket_id=ticket.id)      #Redirct to ticket booked confirmation page.
	
	form=PaymentForm()
	context={"form":form,"booking":booking}
	return render(request,'eventbooking/payment.html',context)


@login_required(login_url='login_page')
def ticket_confirm(request,ticket_id):
	'''View that displays a confirmation after ticket is booked.'''
	ticket=Ticket.objects.get(id=ticket_id)
	return render(request,'eventbooking/ticket_confirm.html',{"ticket":ticket})


@login_required(login_url='login_page')
def my_tickets(request):
	'''View that displays tickets booked by the user logged in.
	Only ticket belonging to the user is displayed.
	Users are given option to cancel the ticket if event time left is more than 24 hours''
	Login is required.'''
	tickets=Ticket.objects.filter(user=request.user)                         #Getting all the tickets
	
	if tickets.count() >0:
		ticket=tickets.first()
		today=datetime.date.today()                                            #Getting date and time to decide wether to display cancel button or not.
		daybefore_event=ticket.booking.event.date-datetime.timedelta(days=1)
		timenow=datetime.datetime.now().time()
		context={'tickets':tickets,'today':today,'timenow':timenow,'daybefore_event':daybefore_event}
	else:
		context={'tickets':tickets}
	return render(request,'eventbooking/my_tickets.html',context)

#@login_required(login_url='login_page')
@user_passes_test(lambda user: user.is_active and user.is_superuser, login_url='logout')
def create_event(request):
	'''View to create events.
	Only admin user can create events. other user restricted.'''
	if request.method=='POST':
		form=EventForm(request.POST,request.FILES)                         #Getting details submited by admin and creating event.
		if form.is_valid():
			form.save()
			return redirect('home')


	form = EventForm()
	return render(request,'eventbooking/event_create_update.html',{"form":form})


@user_passes_test(lambda user: user.is_active and user.is_superuser, login_url='logout')
def update_event(request,event_id):
	'''View to update events.
		Only Admin user can update an event.'''
	event=Event.objects.get(id=event_id)

	if request.method=='POST':                                          #Getting details submited by user and updating the event. 
		form = EventForm(request.POST,request.FILES)
		if form.is_valid():
			event.name= request.POST.get('name')
			event.summary=request.POST.get('summary')			
			event.seats=request.POST.get('seats')
			event.event_price=request.POST.get('event_price')
			event.date=request.POST.get('date')
			event.time=request.POST.get('time')
			event.city=request.POST.get('city')
			event.location=request.POST.get('location')
			event.event_type=request.POST.get('event_type')
			if request.POST.get('image') != '':
				event.image=request.POST.get('image')
	 		
			event.save()
			
			return redirect('event', event_id=event_id)


	form=EventForm(instance=event)
	return render(request,'eventbooking/event_create_update.html',{'form':form})


@login_required(login_url='login_page')
def registered_events(request):
	'''View to display the registered vents for which tickets are bought.
		Login is required.'''
	tickets=Ticket.objects.filter(user=request.user)                 #Getting events based on tickets booked.
	
	return render(request,'eventbooking/registered_events.html',{"tickets":tickets})