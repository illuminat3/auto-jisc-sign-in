# auto-jisc-sign-in

Automatically signs you into your jisc lecture  

## Tutorial

Create a `.env` file in the root of the project  
In here create 3 values  

``` env
STUDENTUSERNAME = ""
PASSWORD = ""
EMAIL = ""
```

This will then allow for `selenium` to automatically login for you.  
This extracts the token cookie which allows for requests to the jisc API.  
The program will then start brute forcing the outcome.  

## Explanation

This works by brute forcing the event pin. This is because jisc uses a simple api enpoint that simply takes a lecture id and 6 digit lecture code.  
This leaves only 1 million options which we can send to eventually brute force it.  
From testing this will make the api run about 10 times slower per 40 requests per second.  
This doesn't appear to have any negative impacts as the api is very solid.  
So to do this we grab the id for the current lecture from [Jisc Lecture Endpoint](https://api.la.jisc.ac.uk/event/timetable)  
This will return a list of timestamps.  
We will then filter this for the current time and look for any that match. If we find one that matches we check for the `isCancelled` property.  
If the property is false we will then take the `eventId` property from it and subsitute this into the [Jisc Checkin Endpoint](https://api.la.jisc.ac.uk/event/lookup/000000?id=eventId)
We will then simply try all 1 million possible combinations doing 100 at a time with 1 second delays inbetween until we successfully submit it (there is probably a better way to do this as we may be able to eliminate some numbers or even fnid an endpoint which has the correct codes)  
