from django import forms
from .models import Ticket,Booking,Event


class TicketBookingForm(forms.ModelForm):
	'''Ticket Booking Form.Asks for no. of person for which the ticket has to be booked.'''
	class Meta:
		model = Booking
		fields = ['no_of_person']


class PaymentForm(forms.ModelForm):
	'''Payment form. It displays the total amount and asks for choice of payment'''
	payment_method = forms.ChoiceField(choices=(('Online Wallet','Online Wallet'),('Credit Card','Credit Card')))
	
	class Meta:
		model = Ticket
		fields = ['payment_method']

class EventForm(forms.ModelForm):
	'''Event vreation or updation form. Admin can use it to create or update events'''
	class Meta:
		model=Event
		fields='__all__'