from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page,name='home'),
    path('event/<str:event_id>',views.event_page,name='event'),
    path('ticket-book/<str:event_id>',views.ticket_booking,name="ticket_book"),
    path('payment/<str:booking_id>',views.payment,name="payment"),
    path('ticket-confirm/<str:ticket_id>',views.ticket_confirm,name="ticket_confirm"),
    path('mytickets',views.my_tickets,name='mytickets'),
    path('create-event',views.create_event,name='create_event'),
    path('update-event/<str:event_id>',views.update_event,name='update_event'),
    path('registered-events',views.registered_events,name='registered_events'),
]