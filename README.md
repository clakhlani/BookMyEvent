# BookMyEvent

This is a django project on Event Management System. Users and go through the list of events and book for the events they want to. Users can book events befor th events starts. User also has option to cancel the booked tickets. But they can only do so 24 hours before the respective events starts.
Admin user has special  privilages. They can create new events and update the existing once.If during event creation a image for the event is not uploaded then default image is used.

All the uploaded images are stored in media/event_pics directory. While the default image is present at media/default.jpg

The project has two apps:
1. eventbooking : This app is responsible for displaying all the events, Booking of events, Display respective users tickets, display respective user registered events, cancel tickets.
There are various checks applied depending on the avaibility of seats for the event while booking a ticket for it. Similarly checks are applied while cancelling tickets.

2. user: This app is responsible for creating new users and allowing existings users to signin. It asks for email username and password while signing up. For login username and password are to be provided.

Test coverage reports for the project are present in htmlcov directory. All the test cases are present in eventbooking/tests.py. Test Case for models and views coverage are added in the file.

Documentation for the project is present in docs/build/html/index.html. The documentation icludes the description of all the models,forms and views used in the project and detail about its respective parameters.  

