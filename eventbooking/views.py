from django.shortcuts import render
from .models import Event


def home_page(request):
	#events=Event.object.all()
	events=None
	return render(request,'eventbooking/home.html',{"events":events})

def event_page(request,event_id):
	event= None
	for evt in events:
		print(evt)
		if evt["id"]==int(event_id):
			event=evt
	context={"event":event}
	return render(request,'eventbooking/events.html',context)