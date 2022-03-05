from django.test import TestCase
from eventbooking.models import Event, Ticket

class EventModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		Event.objects.create(name= 'Test Event',
			summary="This is a dummy event",			
			seats=25,
			event_price=200.00,
			date='2022-04-05',
			time="19:00:00",
			city='Kolkata',
			location='ABC Street',
			event_type='Music',
			)

	def test_str_return(self):
		event=Event.objects.get(id=1)
		self.assertEqual(str(event),event.name)
				