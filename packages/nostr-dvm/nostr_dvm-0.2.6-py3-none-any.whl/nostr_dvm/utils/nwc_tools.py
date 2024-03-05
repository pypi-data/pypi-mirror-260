import json
import os

import requests
from nostr_sdk import Keys, PublicKey, Client, nip04_encrypt, EventBuilder, Tag, NostrSigner

from nostr_dvm.utils.dvmconfig import DVMConfig
from nostr_dvm.utils.nostr_utils import check_and_set_private_key
from nostr_dvm.utils.zap_utils import zaprequest


def nwc_zap(connectionstr, bolt11, keys):
    target_pubkey, relay, secret = parse_connection_str(connectionstr)
    SecretSK = Keys.parse(secret)

    content = {
        "method": "pay_invoice",
        "params": {
            "invoice": bolt11
        }
    }

    signer = NostrSigner.keys(keys)
    client = Client(signer)
    client.add_relay(relay)
    client.connect()

    client_public_key = PublicKey.from_hex(target_pubkey)
    encrypted_content = nip04_encrypt(SecretSK.secret_key(), client_public_key, json.dumps(content))

    pTag = Tag.parse(["p", client_public_key.to_hex()])
    event = EventBuilder(23194, encrypted_content,
                         [pTag]).to_event(keys)

    event_id = client.send_event(event)
    print(event_id.to_hex())


def parse_connection_str(connectionstring):
    split = connectionstring.split("?")
    targetpubkey = split[0].split(":")[1]
    split2 = split[1].split("&")
    relay = split2[0].split("=")[1]
    relay = relay.replace("%3A%2F%2F", "://")
    secret = split2[1].split("=")[1]
    return targetpubkey, relay, secret


def make_nwc_account(identifier, nwcdomain):
    pubkey = Keys.parse(os.getenv("DVM_PRIVATE_KEY_" + identifier.upper())).public_key().to_hex()
    data = {
        'name': identifier,
        'host': os.getenv("LNBITS_HOST"),
        'key': os.getenv("LNBITS_ADMIN_KEY_" + identifier.upper()),
        'pubkey': pubkey,
    }

    try:
        url = nwcdomain
        header = {"content-type": "application/json"}
        res = requests.post(url, headers=header, json=data)
        obj = json.loads(res.text)
        if obj['params']['connectionURI'] != "Users already exists":
            return obj['params']['connectionURI']
        else:
            return ""

    except Exception as e:
        print(e)
        return ""


def nwc_test(nwc_server):
    connectionstring = make_nwc_account("test", nwc_server + "/api/new")
    print(connectionstring)
    #  TODO Store the connection string in a db, use here if you already have one
    # connectionstring = "nostr+walletconnect:..."
    if connectionstring != "":
        # we use the keys from a test user
        keys = Keys.parse(check_and_set_private_key("test"))

        # we zap npub1nxa4tywfz9nqp7z9zp7nr7d4nchhclsf58lcqt5y782rmf2hefjquaa6q8's profile 21 sats and say Cool stuff
        pubkey = PublicKey.from_bech32("npub1nxa4tywfz9nqp7z9zp7nr7d4nchhclsf58lcqt5y782rmf2hefjquaa6q8")
        bolt11 = zaprequest("hype@bitcoinfixesthis.org", 21, "Cool Stuff", None,
                            pubkey, keys, DVMConfig.RELAY_LIST)

        nwc_zap(connectionstring, bolt11, keys)
