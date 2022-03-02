from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE , SET_NULL

# Create your models here.
class Event(models.Model):
	#event_id=models.AutoField(primary_key=True)
	name= models.CharField(max_length=200)
	summary=models.TextField(null=True,blank=True)
	seats=models.IntegerField()
	date=models.DateTimeField()
	image=models.ImageField()

	def __str__(self):
		return self.name

class Ticket(models.Model):
	event=models.ForeignKey(Event,on_delete=models.SET_NULL,null=True)
	num_of_person=models.IntegerField()
	date_booked=models.DateTimeField()
	user= models.ForeignKey(User, on_delete=models.CASCADE)
	amount=models.DecimalField(max_digits=8,decimal_places=2,)
	payment_method=models.CharField(max_length=15)

	def __str__(self):
		return self.id 
