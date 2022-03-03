from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page,name='home'),
    path('event/<str:event_id>',views.event_page,name='event'),
    path('ticket-book/<str:event_id>',views.ticket_booking,name="ticket_book"),
    path('payment/<str:booking_id>',views.payment,name="payment"),
    path('ticket-confirm/<str:ticket_id>',views.ticket_confirm,name="ticket_confirm")

]