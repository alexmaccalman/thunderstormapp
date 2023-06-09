# Thunderstorm App

Below are instruction on how I built an Azure Function time trigger python app to trigger every morning and check the weather open api and send a SMS text if the forecast expects thunderstorms. 

## Instructions

Create resoruce group and stroage account.  
Retrieve Storage Connection String and store in Azure Key Vault
```
DefaultEndpointsProtocol=https;AccountName=<account-name>;AccountKey=<account-key>;EndpointSuffix=core.windows.net
```  

Step 1: Set up Azure Key Vault

Create an Azure Key Vault resource in your Azure portal.
Store your API_KEY, ACCOUNT_SID, and AUTH_TOKEN as secrets in the Azure Key Vault.
Store your storage connection string as a secret in the Azure Key Vault.
Step 2: Set up Visual Studio Code

Install the Azure Functions extension in Visual Studio Code.
Install the Azure CLI and sign in to your Azure account using the Azure CLI extension in Visual Studio Code.
Step 3: Create an Azure Function Project

Open Visual Studio Code and create a new folder for your project.
Open a terminal in Visual Studio Code and navigate to the project folder.
Run the following command to create a new Azure Function project:
```
func init MyFunctionProject --python
```  
Change to the project folder:
```
cd MyFunctionProject
```  
Step 4: Create a Time Trigger Function

Run the following command to create a new time-triggered function:
```
func new --name MyTimeTrigger --template "TimerTrigger" --python
```  
Open the MyTimeTrigger folder and replace the contents of __init__.py with your Python code that checks the weather and sends a text message. Make sure to add the necessary imports and remove the existing template code.
Step 5: Access Key Vault Secrets

Install the azure-identity package by running the following command in the terminal:
``` 
pip install azure-identity
```  
Install the azure-keyvault-secrets package by running the following command in the terminal:
```
pip install azure-keyvault-secrets
```  
Open the local.settings.json file in the root of your project and add the following settings:
```  
"Values": {
  "FUNCTIONS_WORKER_RUNTIME": "python",
  "KEYVAULT_URI": "<your-key-vault-uri>"
}
```  
Replace <your-key-vault-uri> with the URI of your Azure Key Vault.
Open the __init__.py file and replace the existing code with the following code:
```
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient

def main(mytimer: func.TimerRequest) -> None:
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=os.environ["KEYVAULT_URI"], credential=credential)
    api_key = secret_client.get_secret("API_KEY").value
    account_sid = secret_client.get_secret("ACCOUNT_SID").value
    auth_token = secret_client.get_secret("AUTH_TOKEN").value

    storage_connection_string = secret_client.get_secret("STORAGE_CONNECTION_STRING").value
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)

    # Your weather checking and SMS sending code here

```  
Replace "API_KEY", "ACCOUNT_SID", "AUTH_TOKEN", and "STORAGE_CONNECTION_STRING" with the names of your secrets in Azure Key Vault.  




In the left-hand menu, click on "Configuration" under the "Settings" section.  

In the "Application settings" section, click on the "New application setting" button.  

In the "Name" field, enter WEBSITE_TIME_ZONE.  

In the "Value" field, enter the desired time zone value. For example, if you want to set the time zone to Eastern Standard Time (EST), you can enter Eastern Standard Time as the value.  

Click the "OK" button to save the application setting.  

After saving the application setting, restart your Function App to apply the changes. You can do this by clicking on the "Overview" option in the left-hand menu and then clicking on the "Restart" button at the top of the page.  

By adding the WEBSITE_TIME_ZONE application setting with the desired time zone value, you ensure that your Function App uses the specified time zone for all time-related operations, including the trigger schedule specified in the binding configuration.  

Inside the function.json add the following binding:  
```
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "name": "mytimer",
      "type": "timerTrigger",
      "direction": "in",
      "schedule": "0 0 8 * * *",
      "timeZone": "Eastern Standard Time" 
    }
  ]
}
```  

Step 6: Deploy the Azure Function

Open the Azure Functions extension in Visual Studio Code.  
Right Click the function folder and click on the "Deploy to Function App" button in the Azure Functions sidebar.  
Follow the prompts to select your subscription, resource group, and function app.  
Once the deployment is successful, the Azure Function will be deployed and triggered based on the schedule specified in binding.

In the portal, go to the Azure Function under "Identity" under settings and turn on the System Assigned Identify.  
Then go to the Azure Key Vault and assign the system identify called thunderappfunction as a contributer.  
