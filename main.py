from fastapi import FastAPI, Request
import stripe
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

stripe.api_key = os.environ['STRIPE_API_KEY']

@app.get('/1')
async def root():
    return "Hello world!"

@app.get('/2')
async def root2():
    return "Hello world again!"

@app.post("/data")
async def post_data(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header,'whsec_hdQkx0UM1VHwaGgwj2mhcRlCjWLwlt2j'
        )
        print(event)

    except ValueError as e:
        raise e
    
    except stripe.error.SignatureVerificationError as e:
        raise e
    
    return{'status': 'success'}