import requests
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import nats
from nats.aio.client import Client as NATS
# from nats.errors import ConnectionClosedError, TimeoutError, NoServersError
import os
from dotenv import load_dotenv
from pydantic import BaseModel
class Item(BaseModel):
    sub : str
    msg : str
    
load_dotenv()
port = os.getenv("NATS_PORT",4222)
host = os.getenv("NATS_HOST", "127.0.0.1")
print("host : {host}".format(host=host))

nc= NATS()

router = APIRouter(
    prefix='/esb',
    tags=['esb'],
    responses={
        404: {'description': 'Not found'}
        }
)

async def doSomethingRandom():
    url = 'https://coffee.alexflipnote.dev/random.json'
    try:
        print("test function.")
        x = requests.get(url)
        print("request responded.")
    except Exception as e:
        print(e)
    #print the response text (the content of the requested file):
    else:
        print(x.json)
        return x.text
    
@router.get("/")
async def get_test():
    print("get request")
    return await doSomethingRandom()

@router.post("/pub")
async def publish_message(item:Item):
    if(nc.is_connected):
        #message needs to be in bytes.
        await nc.publish(item.sub, item.msg.encode(encoding = 'UTF-8'))
        return 200
    else:
         raise HTTPException(
            status_code=400, detail="no nc"
        )


# args for swagger
app = FastAPI(title='FastAPI', description='description', version='0.1')

origins = [
    '*'
]
# CORS - Cross origin resource sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*']
)


app.include_router(router)


@app.on_event("startup")
async def run():
    print("startup")
    async def disconnected_cb():
        print("Got disconnected...")

    async def reconnected_cb():
        print("Got reconnected...")

    await nc.connect("nats://{host}:{port}".format(host=host,port=port),reconnected_cb=reconnected_cb,
                     disconnected_cb=disconnected_cb,
                     max_reconnect_attempts=-1)   

    # the function for callback.
    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    # Simple publisher and async subscriber via coroutine.
    sub = await nc.subscribe("foo", cb=message_handler)

# if __name__ == 'main':

    # All of these doesn't work. uvicorn sets an async loop already.
    # asyncio.create_subprocess_exec(run())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(run(loop))
    # loop.run_forever()
    
    # loop.close()
