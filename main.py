from fastapi import FastAPI, Request
import stripe

app = FastAPI()
stripe.api_key = 'sk_test_51JuKP4IoVeovnndhM4s9HIZEbpy0OZfR2YWYaD4ZANEYkDgbiInDzCIPFROcHqhbrN18ciglpl6UR0Y7ThbL7wkd00ujB8BeL1'

@app.get('/')
async def root():
    return "Hello world!"

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