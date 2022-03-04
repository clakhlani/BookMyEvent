from django import forms
from .models import Ticket,Booking,Event


class TicketBookingForm(forms.ModelForm):
	no_of_per=forms.IntegerField(initial=0)
	
	class Meta:
		model = Booking
		fields = ['no_of_per']


class PaymentForm(forms.ModelForm):
	payment_method = forms.ChoiceField(choices=(('Online Wallet','Online Wallet'),('Credit Card','Credit Card')))
	
	class Meta:
		model = Ticket
		fields = ['payment_method']

class EventForm(forms.ModelForm):
	class Meta:
		model=Event
		fields='__all__'