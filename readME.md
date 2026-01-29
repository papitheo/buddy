### How CORS Works
When your frontend (at http://localhost:3000) tries to fetch data from your backend API (at http://localhost:8000), the browser:

Sends a preflight request asking: "Can I access this resource?"
Your API responds with CORS headers saying: "Yes, you're allowed"
Browser allows the request to proceed
Without those CORS headers, the browser blocks the response, even if the request succeeded.