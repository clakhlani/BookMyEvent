from django.test import TestCase , Client
from eventbooking.models import Event, Booking, Ticket
from user.models import User
from django.urls import reverse
import datetime


class EventModelTest(TestCase):
	'''Test Case for Event Model'''
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
				

class TicketModelTest(TestCase):
	'''Test Case for Tickt Model'''
	@classmethod
	def setUpTestData(cls):
		event=Event.objects.create(name= 'Test Event',
			summary="This is a dummy event",			
			seats=25,
			event_price=200.00,
			date='2022-04-05',
			time="19:00:00",
			city='Kolkata',
			location='ABC Street',
			event_type='Music',
			)
		booking= Booking.objects.create(amount=6000,
			no_of_person=4,
			event=event,
			)
		user=User.objects.create(email="test@gmail.com",
			username='testuser',
			password='test@123',
			)



		Ticket.objects.create(
			booking=booking,
			date_booked='2022-03-22',
			user = user,
			payment_method = 'Credit Card',
			)

	def test_str_return(self):
		ticket=Ticket.objects.get(id=1)
		print(str(ticket))
		self.assertEqual(str(ticket),ticket.booking.event.name)



# Views Test case

class ViewFunctionsTest(TestCase):
	
	def setUp(self):
		self.client=Client()
		self.event=Event.objects.create(name= 'Test Event',
			summary="This is a dummy event",			
			seats=25,
			event_price=200.00,
			date='2022-04-05',
			time="19:00:00",
			city='Kolkata',
			location='ABC Street',
			event_type='Music',
				)



		self.event2=Event.objects.create(name= 'Test Event',
			summary="This is a dummy event",			
			seats=0,
			event_price=200.00,
			date='2022-03-20',
			time="19:00:00",
			city='Kolkata',
			location='ABC Street',
			event_type='Music',
			)


		self.event3=Event.objects.create(name= 'Test Event',
			summary="This is a dummy event",			
			seats=30,
			event_price=200.00,
			date='2022-03-05',
			time="19:00:00",
			city='Kolkata',
			location='ABC Street',
			event_type='Music',
			)
		user = User.objects.create_user(username='newuser',password='new@1234',email='newuser@email.com')
		user.save()

		admin_user=User.objects.create_superuser(email="admin@gmail.com",username='admin',password='admin@123')
		admin_user.save()


		self.booking= Booking.objects.create(amount=6000,
			no_of_person=4,
			event=self.event,
			)
		self.booking3= Booking.objects.create(amount=6000,
			no_of_person=4,
			event=self.event3,
			)

		self.ticket=Ticket.objects.create(
			booking=self.booking,
			date_booked='2022-03-22',
			user = user,
			payment_method = 'Credit Card',
			)


		self.ticket3=Ticket.objects.create(
			booking=self.booking3,
			date_booked='2022-03-22',
			user = user,
			payment_method = 'Credit Card',
			)


	def test_registration_response(self):
		'''Test for register view get method'''
		response=self.client.get(reverse('register'))

		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'user/register.html')

	

	def test_home_page_response(self):
		'''Test for home_page view get method'''
		response=self.client.get(reverse('home'))

		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'eventbooking/home.html')

	def test_home_page_post(self):
		'''Test for home_page view post method. Different filter scenarios covered'''
		response=self.client.post(reverse('home'),{"City":"Kolkata","Genre": "Music"})
		response2=self.client.post(reverse('home'),{"City":"ALL","Genre": "Music"})
		response3=self.client.post(reverse('home'),{"City":"Kolkata","Genre": "ALL"})
		response4=self.client.post(reverse('home'),{"City":"Mumbai","Genre": "ALL"})

		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'eventbooking/home.html')

		self.assertEquals(response2.status_code,200)
		self.assertTemplateUsed(response2,'eventbooking/home.html')

		self.assertEquals(response3.status_code,200)
		self.assertTemplateUsed(response3,'eventbooking/home.html')

		self.assertEquals(response4.status_code,200)
		self.assertTemplateUsed(response4,'eventbooking/home.html')

	def test_event_page_response(self):
		'''Test for event_page view get method'''		
		response=self.client.get(reverse('event',args=[self.event.id]))

		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'eventbooking/events.html')


	def test_ticket_booking_get(self):
		'''Test for ticket_booking get method'''

		login=self.client.login(username='newuser',password='new@1234')



		response=self.client.get(reverse('ticket_book',args=[self.event.id]))

		self.assertEqual(str(response.context['user']),'newuser')

		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'eventbooking/ticket_book.html')




	def test_ticket_confirm_get(self):
		'''Test for ticket_confirm view get method'''

		login=self.client.login(username='newuser',password='new@1234')



		response=self.client.get(reverse('ticket_confirm',args=[self.ticket.id]))

		self.assertEqual(str(response.context['user']),'newuser')

		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'eventbooking/ticket_confirm.html')



	def test_my_ticket_get(self):
		'''Test for my_tickets view get method'''

		login=self.client.login(username='newuser',password='new@1234')



		response=self.client.get(reverse('mytickets'))

		self.assertEqual(str(response.context['user']),'newuser')

		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'eventbooking/my_tickets.html')


	def test_registered_events_get(self):
		'''test for registered_events view get method'''
		login=self.client.login(username='newuser',password='new@1234')



		response=self.client.get(reverse('registered_events'))

		self.assertEqual(str(response.context['user']),'newuser')

		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'eventbooking/registered_events.html')


	def test_crete_event_get(self):
		'''Test for create_event view get method'''
		
		login=self.client.login(username='admin',password='admin@123')



		response=self.client.get(reverse('create_event'))

		

		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'eventbooking/event_create_update.html')



	def test_event_create_post(self):
		'''Test for create_event view post method'''
		
		login=self.client.login(username='admin',password='admin@123')
		response=self.client.post(reverse('create_event'),{'name': 'Test Event2',
			'summary':'This is a dummy event2',			
			'seats':30,
			'event_price':200.00,
			'date': datetime.date.today(),
			'time':datetime.datetime.now().time(),
			'city':'Kolkata',
			'location':'ABC Street',
			'event_type':'Music'})


		

		self.assertEquals(response.status_code,302)
	



	def test_update_event_get(self):
		'''Test for update_event view get method'''
		login=self.client.login(username='admin',password='admin@123')



		response=self.client.get(reverse('update_event',args=[self.event.id]))

		

		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'eventbooking/event_create_update.html')


	def test_event_update_post(self):
		'''Test for update_event view post method'''
		login=self.client.login(username='admin',password='admin@123')
		response=self.client.post(reverse('update_event',args=[self.event.id]),{'name': 'Test Event3',
			'summary':'This is a dummy event2',			
			'seats':30,
			'event_price':200.00,
			'date': datetime.date.today(),
			'time':datetime.datetime.now().time(),
			'city':'Kolkata',
			'location':'ABC Street',
			'event_type':'Music'})


		

		self.assertEquals(response.status_code,302)
		

	def test_payment_get(self):
		'''Test for payment view get method'''
		login=self.client.login(username='newuser',password='new@1234')

		response=self.client.get(reverse('payment',args=[self.booking.id]))

		self.assertEqual(str(response.context['user']),'newuser')

		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'eventbooking/payment.html')



	def test_payment_post(self):
		'''Test for payment view post method'''

		user =User.objects.get(username='newuser')
		login=self.client.login(username='newuser',password='new@1234')
		response=self.client.post(reverse('payment',args=[self.booking.id]),{'booking':self.booking,
			'date_booked': datetime.date.today(),
			'user' : user,
			'payment_method' : 'Credit Card'})

		

		self.assertEquals(response.status_code,302)
	

	def test_ticket_cancel_get(self):
		'''Test for cancel_ticket get method. All different restrictioin scenarios covered.''' 
		login=self.client.login(username='newuser',password='new@1234')

		response=self.client.get(reverse('cancel_ticket',args=[self.ticket.id]))
		response2=self.client.get(reverse('cancel_ticket',args=[2]))
		response3=self.client.get(reverse('cancel_ticket',args=[self.ticket3.id]))


		self.client.login(username='admin',password='admin@123')

		response4=self.client.get(reverse('cancel_ticket',args=[self.ticket.id]))

		

		self.assertEqual(str(response.context['user']),'newuser')

		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,'eventbooking/cancel_ticket.html')

		self.assertEquals(response2.status_code,200)
		self.assertTemplateUsed(response2,'eventbooking/cancel_ticket.html')

		self.assertEquals(response3.status_code,200)
		self.assertTemplateUsed(response3,'eventbooking/cancel_ticket.html')

		self.assertEquals(response4.status_code,200)
		self.assertTemplateUsed(response4,'eventbooking/cancel_ticket.html')



	def test_ticket_cancel_post(self):
		'''Test for cancel_ticket view post method'''
		
		login=self.client.login(username='newuser',password='new@1234')
		response=self.client.post(reverse('cancel_ticket',args=[self.ticket.id]),{})

		

		self.assertEquals(response.status_code,302)



	def test_ticket_booking_post(self):
		'''Test for  ticket_booking view post method.All seat booking scearios covered.'''
		login=self.client.login(username='newuser',password='new@1234')
		response=self.client.post(reverse('ticket_book',args=[self.event.id]),{'amount':800.00,'no_of_person':4,'event':self.event})
		response2=self.client.post(reverse('ticket_book',args=[self.event.id]),{'amount':800.00,'no_of_person':0,'event':self.event})
		response3=self.client.post(reverse('ticket_book',args=[self.event.id]),{'amount':800.00,'no_of_person':40,'event':self.event})
		response3=self.client.post(reverse('ticket_book',args=[self.event2.id]),{'amount':800.00,'no_of_person':2,'event':self.event2})
		response3=self.client.post(reverse('ticket_book',args=[self.event3.id]),{'amount':800.00,'no_of_person':2,'event':self.event3})
		

		self.assertEquals(response.status_code,302)


	def test_logout_get(self):
		'''Test for logout view get method'''
		login=self.client.login(username='newuser',password='new@1234')

		response=self.client.get(reverse('logout'))

		self.assertEquals(response.status_code,302)

	