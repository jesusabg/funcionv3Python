
import base64
import azure.functions as func
import logging
import msal
import os 
import json
def main(req: func.HttpRequest) -> func.HttpResponse:
    Client_ID = "cf63975f-f44a-4832-ad5b-b780849b61d8"
    authority = "https://login.microsoftonline.com/42011f97-4d04-4eb4-be75-87f785064030"
    Client_Credential = "_ls8Q~OvyMNAHh~PHXbVqVcV2JfUfQKCpnpG0cvt"
    scopee =["cf63975f-f44a-4832-ad5b-b780849b61d8/.default"] 
    if req.method=="POST":
        body=req.get_json()
        usuario=str(body.get('usuario'))
        #retrieve the encrypted password from the request body
        encpassword=str(body.get('password'))
        decpassword = base64.b64decode(encpassword)
        logging.info(decpassword)
        try:
            app = msal.ClientApplication(Client_ID, authority=authority,
            client_credential=Client_Credential 
            )
            result = None
            accounts = app.get_accounts(username=usuario)
            if accounts:
                logging.info("Account(s) exists in cache, probably with token too. Let's try.")
                result = app.acquire_token_silent(scopee , account=accounts[0])
            if not result:
                logging.info("No suitable token exists in cache. Let's get a new one from AAD.") 
                result = app.acquire_token_by_username_password(usuario, decpassword, scopes=scopee)
            if "access_token" in result:
                result2 = {"access_token":result["access_token"]}
                result3=json.dumps(result)
                return func.HttpResponse(result3,status_code=200)
            else:
                return func.HttpResponse("error en tu peticion",status_code=400)

        except Exception as e:
            logging.error(e)
            return func.HttpResponse(str(e), status_code=500)
