### How CORS Works
When your frontend (at http://localhost:3000) tries to fetch data from your backend API (at http://localhost:8000), the browser:

- Sends a preflight request asking: "Can I access this resource?"
- Your API responds with CORS headers saying: "Yes, you're allowed"
- Browser allows the request to proceed
- Without those CORS headers, the browser blocks the response, even if the request succeeded.

### GET Request 
- is used to retrieve data from the server
- When root (/) path is checked, it is not making a request for some data, rather it is checking if the API is alive 

### POST request
- Used to send data to the server
- send user's message + history, so use POST with data in the body