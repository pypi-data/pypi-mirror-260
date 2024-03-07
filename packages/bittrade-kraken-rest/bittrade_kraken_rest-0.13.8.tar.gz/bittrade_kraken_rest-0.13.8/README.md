# ELM Bittrade's Kraken REST package & optional CLI

## Install

`pip install bittrade-kraken-rest` or `poetry add bittrade-kraken-rest`

Not all Kraken endpoints are implemented yet.

# Public endpoints

```python
from bittrade_kraken_rest import get_server_time

server_time = get_server_time().run()
print(server_time) # GetServerTimeResult(unixtime=1673053481, rfc1123='Sat, 07 Jan 23 01:04:41 +0000')
```

*The above example is complete, it should run as is*

Bring Your Own ~~Credentials~~ Signature (Private endpoints)
---

TLDR; Don't agree to pass your API secret to third-party code; instead sign the requests yourself, with your own code. It's safer.

This library doesn't want to ever access your Kraken secret keys.

Most libraries expect you to provide your api key and secret. I'm not comfortable doing that with third-party code, even open sourced.

Here instead, the library prepares the request, which you then sign using your own code and the library finishes the job. It has NO access to your secret.

Thankfully this is quite straightforward: you need to implement a `sign(x: tuple[PreparedRequest, str, dict[str, Any]]) -> PreparedRequest` method which sets the correct headers. Below is an example of such a signature function:

```python
from os import getenv
import urllib, hmac, base64, hashlib
from pathlib import Path

# Taken from https://docs.kraken.com/rest/#section/Authentication/Headers-and-Signature
def generate_kraken_signature(urlpath, data, secret):
    post_data = urllib.parse.urlencode(data)
    encoded = (str(data["nonce"]) + post_data).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    signature_digest = base64.b64encode(mac.digest())
    return signature_digest.decode()

# Here the key/secret are loaded from a .gitignored folder, but you can use environment variables or other method of configuration
def sign(x: tuple[PreparedRequest, str, dict[str, Any]]):
    request, url, data = x
    request.headers["API-Key"] = Path("./config_local/key").read_text()
    request.headers["API-Sign"] = generate_kraken_signature(
        url, data, Path("./config_local/secret").read_text()
    )
    return request

```

With that in place, a observable pipe will get you the result you need:


```python
from bittrade_kraken_rest import get_websockets_token_request, get_websockets_token_result
from reactivex import operators

result = get_websockets_token_request().pipe(
    operators.map(sign),
    get_websockets_token_result()
).run()
```

### Full example with signature function

```python
from os import getenv
import urllib, hmac, base64, hashlib
from pathlib import Path
from bittrade_kraken_rest import get_websockets_token_request, get_websockets_token_result
from reactivex import operators

# Taken from https://docs.kraken.com/rest/#section/Authentication/Headers-and-Signature
def generate_kraken_signature(urlpath, data, secret):
    post_data = urllib.parse.urlencode(data)
    encoded = (str(data["nonce"]) + post_data).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    signature_digest = base64.b64encode(mac.digest())
    return signature_digest.decode()

# Here the key/secret are loaded from a .gitignored folder, but you can use environment variables or other method of configuration
def sign(x: tuple[PreparedRequest, str, dict[str, Any]]):
    request, url, data = x
    request.headers["API-Key"] = Path("./config_local/key").read_text()
    request.headers["API-Sign"] = generate_kraken_signature(
        url, data, Path("./config_local/secret").read_text()
    )
    return request

result = get_websockets_token_request().pipe(
    operators.map(sign),
    get_websockets_token_result()
).run()

```

*The above example is complete, it should run as is*

### Observables

The above examples use `.run()` to trigger the observable subscription but Observables make it very easy to create pipes, retries and more. All operators can be found on the [RxPy read the docs](https://rxpy.readthedocs.io/en/latest/).

## Tests

```
pytest
```

Note that integration tests require a valid key/secret pair saved as `key` and `secret` files in a `.config_local` folder placed at the root of the repo.

## CLI


The CLI has been moved to [its own repo](https://github.com/TechSpaceAsia/bittrade-kraken-cli)
