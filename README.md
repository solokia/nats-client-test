# nats-client-test
nats.io client in python to be deployed in k8 for testing.

# Integration with FastAPI
What is done is to just set the connection to nats.io during the startup of fastAPI using the decorator `@app.on_event("startup")`  

Tried to use asyncio to set a loop for sub or connection but did not work since uvicorn probably already has a loop going on.

Alternatives that may work but have no time to test
1. subprocesses - running subs in a subprocess on its own and run the loop.
2. multithreading - starting a thread to loop before starting uvicorn in app.