#!/usr/bin/env python3

"""
Perform a Globus directory sync with the Globus Python SDK, reusing refresh
tokens we've already obtained for PARSL.   The tokens can be obtained by running
the bin/parsl-globus-auth command that is provided with the parsl package and
authenticating to Globus.   parsl-globus-auth creates the TOKEN_FILE we use
here.

Note this is NOT a PARSL transfer!
"""

import os
import json
from globus_sdk import (NativeAppAuthClient, TransferClient,
                        RefreshTokenAuthorizer, TransferData)
from globus_sdk.exc import GlobusAPIError



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
    save_tokens_to_file(TOKEN_FILE, token_response.by_resource_server)



#dcde_parsl_client_id = 'e4466165-2a4c-48c9-916e-df7e4f4bd82c'
# This is (ahem!) appropriation of the PARSL client ID.  Use just for
# debugging purposes (trying to figure out my '400 invalid grant' error):
dcde_parsl_client_id = '8b8060fd-610e-4a74-885e-1051c71ad473'

# This is the token obtained by running parsl-globus-auth so that PARSL can
# authenticate to Globus:
TOKEN_FILE='/home/dcde1000006/.parsl/.globus.json'

ANL_EP = '57b72e31-9f22-11e8-96e1-0a6d4e044368'
BNL_EP = '23f78cc8-41e0-11e9-a618-0a54e005f950'
EMSL_EP = 'e133a52e-6d04-11e5-ba46-22000b92c6ec'
ORNL_EP = '57230a10-7ba2-11e7-8c3b-22000b9923ef'

BNL_EP_HOMEDIR = '/sdcc/u/dcde1000006'
ANL_EP_HOMEDIR = '/blues/gpfs/home/dcowley'


source_endpoint_id = BNL_EP
destination_endpoint_id = ANL_EP

source_dir = '/hpcgpfs01/scratch/dcde1000006/sc19-data'
dest_dir = '/blues/gpfs/home/dcowley/sc19-data'


# First authorize using those refresh tokens:

try:
    tokens = load_tokens_from_file(TOKEN_FILE)

except:
    print("Valid refresh tokens not found in {}.  Unable to authorize to Globus.  Exiting!".format(TOKEN_FILE))
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
# print(transfer)

# Now we should have auth, try setting up a transfer.

tdata = TransferData(tc, source_endpoint_id,
                     destination_endpoint_id,
                     label="DCDE Relion transfer",
                     sync_level="size")

tdata.add_item(source_dir, dest_dir,
               recursive=True)

transfer_result = tc.submit_transfer(tdata)

print("task_id =", transfer_result["task_id"])


while not tc.task_wait(transfer_result['task_id'], timeout=1200, polling_interval=10):
    print(".", end="")
print("\n{} completed!".format(transfer_result['task_id']))

os.listdir(path=dest_dir)
