# API

This is the server side api.  
This will be used to allow multiple pcs to send requests to avoid for multiple pcs checking the same codes.  
This is currently not in use.  

## Structure

This is the structure of the api with all of its endpoints and responses

### /GetCode

Params:  

- `DeviceId` - A UUID for your device so that the thread counts dont overlap  
- `LectureId` - The UUID for the lecture you are trying to brute force  
- `ThreadCount` - The amount of threads that will be making requests  
- `CurrentSearchValue` - The current value being searched  

Responses:  

- `Status` - Status code with 200 being succcess
- `FoundCode` - Defaults to -1 but once a code is found it will return the code to stop the user from having to search for it  
- `SearchLow` - Defaults to 000000, calculates based on the threads that are available and the amount of searched numbers already the start point for your pcs search  
- `SearchHigh` - The max point your pc should have to search for, this is used as a failsafe  

### /FoundCode

Params:  

- `DeviceId` - A UUID for your device to help verify that the correct device found the code  
- `FoundCode` - The successful jisc code  
- `LectureId` - The lectureId for the jisc code  

Responses:  

- `Status` - Status code with 200 being success  
- `FoundCode` - Defaults to null, pings the code back if successful  
