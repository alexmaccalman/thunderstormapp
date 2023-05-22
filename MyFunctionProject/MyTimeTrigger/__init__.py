import datetime
#import pytz
import requests
from twilio.rest import Client
import os
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import azure.functions as func

OWM_ENDPOINT = "https://api.openweathermap.org/data/3.0/onecall"

# Azure Function entry point
def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    logging.info(f"Python timer trigger function ran at {utc_timestamp}")
    if mytimer.past_due:
        logging.info('The timer is past due!')

    # Check if the current time is 08:00 Eastern Time
    # current_time = datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%H:%M')
    # if current_time != '12:59':
    #     logging.info('The function is triggered, but it is not 08:00 Eastern Time yet.')
    #     return

    # Retrieve secrets from Azure Key Vault
    keyvault_url = "https://resumekeyvaultadm.vault.azure.net/"
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=keyvault_url, credential=credential)

    api_key = secret_client.get_secret("API-KEY").value
    account_sid = secret_client.get_secret("ACCOUNT-SID").value
    auth_token = secret_client.get_secret("AUTH-TOKEN").value
    #storage_connection_string = secret_client.get_secret("STORAGE-CONNECTION-STRING").value

    # Your weather checking code
    weather_params = {
        "lat": 39.56633021926093,
        "lon": -76.33500179850502,
        "appid": api_key,
        "exclude": "current,minutely,daily"
    }
    response = requests.get(OWM_ENDPOINT, params=weather_params)
    response.raise_for_status()
    weather_data = response.json()

    will_rain = False
    weather_slice = weather_data["hourly"][:12]
    for hour_data in weather_slice:
        condition_code = hour_data["weather"][0]["id"]
        if int(condition_code) < 300: # less than 300 means thunderstorm
            will_rain = True
            break

    if will_rain:
        # Your SMS sending code
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="It's going to thunderstorm today.⚡ Get Zoey Ready.🐶",
            from_='+18445040783',
            to='+19107977144'
        )
        logging.info(f'SMS sent with message SID: {message.sid}')

    logging.info('Azure Function executed successfully.')
