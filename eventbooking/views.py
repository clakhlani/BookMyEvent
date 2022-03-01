from django.shortcuts import render

events=[
{"id": 1 , "name": "Standup"},
{"id": 2 , "name": "Sports"},
{"id": 3 , "name": "Drama"},
{"id": 4 , "name": "Fair"},
]


def home_page(request):
	return render(request,'eventbooking/home.html',{"events":events})

def event_page(request,event_id):
	event= None
	for evt in events:
		print(evt)
		if evt["id"]==int(event_id):
			event=evt
		context={"event":event}
	return render(request,'eventbooking/events.html',context)