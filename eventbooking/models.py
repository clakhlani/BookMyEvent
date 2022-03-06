from django.db import models
from user.models import User
from django.db.models.deletion import CASCADE , SET_NULL

# Create your models here.
class Event(models.Model):
	'''Model for Event Details'''
	name= models.CharField(max_length=200)
	summary=models.TextField(null=True,blank=True)
	seats=models.IntegerField()
	event_price=models.DecimalField(max_digits=8,decimal_places=2, default=00.00)
	date=models.DateField()
	time=models.TimeField()
	city=models.CharField(max_length=30)
	location=models.CharField(max_length=50)
	event_type=models.CharField(max_length=20, choices=(('Comedy','Comedy'),('Sports','Sports'),('Movie','Movie'),('Music','Music')),default=1)
	image=models.ImageField(default='default.jpg',upload_to='event_pics')

	def __str__(self):
		return self.name


class Booking(models.Model):
	'''Model for booking details'''
	amount = models.DecimalField(max_digits=8,decimal_places=2)
	no_of_person=models.IntegerField()
	event=models.ForeignKey(Event,on_delete=models.CASCADE)

class Ticket(models.Model):
	'''Model for Ticket Booked details.'''
	booking=models.ForeignKey(Booking,default=None,on_delete=models.CASCADE)
	date_booked=models.DateField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	payment_method = models.CharField(max_length=15)

	def __str__(self):
		return self.booking.event.name 