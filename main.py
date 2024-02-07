from fastapi import FastAPI, Request, status
import stripe
from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse

app = FastAPI()
load_dotenv()

stripe.api_key = os.environ['STRIPE_API_KEY']
stripe_endpoint_key = os.environ['ENDPOINT_SECRET_KEY']

@app.get('/')
async def root():
    return "Hello world!"

@app.post("/stripe-data")
async def post_stripe_data(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_endpoint_key
        )
        print(event)

    except ValueError as e:
        raise e
    
    except stripe.error.SignatureVerificationError as e:
        raise e
    
    return{'status': 'success'}

@app.post('/quickbooks-data')
async def post_quickbooks_data(request: Request):
    payload = await request.json()

    try:
        print('data received', payload)
    except ValueError as e:
        raise e
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Webhook received"})

@app.get('/quickbooks-data')
async def get_quickbooks_code(request: Request):
    challenge_token = request.query_params.get("challenge_token")
    print(challenge_token)
    return challenge_token