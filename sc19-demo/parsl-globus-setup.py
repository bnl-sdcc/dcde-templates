import subprocess
import json
from globus_sdk import (NativeAppAuthClient, TransferClient,
                        RefreshTokenAuthorizer, TransferData)
from globus_sdk.exc import GlobusAPIError

authout = subprocess.run(['/usr/local/anaconda3/bin/parsl-globus-auth'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print (authout.stdout)
print (authout.stderr)
# Perform a Globus directory transfer, reusing refresh tokens we've already obtained for PARSL.
# Note this is NOT a PARSL transfer


def load_tokens_from_file(filepath):
    """Load a set of saved tokens."""
    with open(filepath, 'r') as f:
        tokens = json.load(f)

    return tokens

def save_tokens_to_file(filepath, tokens):
    """Save a set of tokens for later use."""
    with open(filepath, 'w') as f:
        json.dump(tokens, f)


def update_tokens_file_on_refresh(token_response):
    """
    Callback function passed into the RefreshTokenAuthorizer.
    Will be invoked any time a new access token is fetched.
    """
    save_tokens_to_file(globus_tokens, token_response.by_resource_server)

dcde_parsl_client_id = '8b8060fd-610e-4a74-885e-1051c71ad473'

globus_tokens='/home/dcde1000006/.parsl/.globus.json'

# First authorize using those refresh tokens:

try:
    tokens = load_tokens_from_file(globus_tokens)

except:
    print("Valid refresh tokens not found in {}.  Unable to authorize to Globus.  Exiting!".format(globus_tokens))
    sys.exit(-1)


transfer_tokens = tokens['transfer.api.globus.org']

try:
    auth_client = NativeAppAuthClient(client_id=dcde_parsl_client_id)
except:
    print ("ERROR: Globus NativeAppAuthClient() call failed!  Unable to obtain a Globus authorizer!")
    sys.exit(-1)

authorizer = RefreshTokenAuthorizer(
    transfer_tokens['refresh_token'],
    auth_client,
    access_token=transfer_tokens['access_token'],
    expires_at=transfer_tokens['expires_at_seconds'],
    on_refresh=update_tokens_file_on_refresh)

try:
    tc = TransferClient(authorizer=authorizer)
except:
    print ("ERROR: TransferClient() call failed!  Unable to call the Globus transfer interface with the provided auth info!")
    sys.exit(-1)


"""
Now we should have a transfer client with auth, We can set up one or many transfers.
Remember each TransferData object has a specific src/dest, and we need to build in a
list of files/dirs with add_item()
"""
