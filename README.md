# auto-jisc-sign-in

Automatically signs you into your jisc lecture 

## Tutorial

You will need to manually grab the headers and save it to headers.txt.  
As long as this is done correctly you should be fine  

## Explanation

This works by brute forcing the event pin. This is because jisc uses a simple api enpoint that simply takes a lecture id and 6 digit lecture code.  
This leaves only 1 million options which we can slowly send to eventually brute force it whilst avoiding overloading the servers.  
Firstly we grab the id for the current lecture from [Jisc Lecture Endpoint](https://api.la.jisc.ac.uk/event/timetable)  
This will return a list of timestamps.  
We will then filter this for the current time and look for any that match. If we find one that matches we check for the `isCancelled` property.  
If the property is false we will then take the `eventId` property from it and subsitute this into the [Jisc Checkin Endpoint](https://api.la.jisc.ac.uk/event/lookup/000000?id=eventId)
We will then simply try all 1 million possible combinations doing 100 at a time with 1 second delays inbetween until we successfully submit it (there is probably a better way to do this as we may be able to eliminate some numbers or even fnid an endpoint which has the correct codes)  
