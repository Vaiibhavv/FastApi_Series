## FastApi Notes

- What is the difference between ASGI and WSGI

| Feature                | WSGI (Web Server Gateway Interface)                                       | ASGI (Asynchronous Server Gateway Interface)                               |
| ---------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Purpose                | Standard interface between web server and synchronous Python applications | Standard interface between web server and asynchronous Python applications |
| Supports               | Synchronous (Blocking) code                                               | Synchronous and Asynchronous code                                          |
| Execution Model        | One request is processed at a time per worker                             | Multiple requests can be processed concurrently without blocking           |
| Concurrency            | Achieved using multiple threads or processes                              | Achieved using Python's `async` and `await` (event loop)                   |
| Async Support          | ❌ No native support                                                       | ✅ Native support                                                           |
| Performance            | Good for CPU-bound or simple applications                                 | Better for I/O-bound applications with many concurrent requests            |
| WebSockets             | ❌ Not supported                                                           | ✅ Fully supported                                                          |
| Long-lived Connections | Poor support                                                              | Excellent support                                                          |
| Server Examples        | Gunicorn, uWSGI, mod_wsgi                                                 | Uvicorn, Hypercorn, Daphne                                                 |
| Framework Examples     | Flask, Pyramid, older Django                                              | FastAPI, Starlette, Quart, modern Django (ASGI mode)                       |
| Request Handling       | Blocks until request completes                                            | Can pause one request while waiting and serve others                       |
| Best Use Cases         | Traditional CRUD web apps                                                 | APIs, chat apps, streaming, real-time systems, microservices               |
