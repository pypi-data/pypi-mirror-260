import copy
import json
import sys
import hashlib
import hmac
import binascii
from datetime import datetime

import requests

if sys.version_info.major < 3:
    from urllib import quote, unquote


    def hmacsha256(key_byte, message):
        return hmac.new(key_byte, message, digestmod=hashlib.sha256).digest()


    def string_to_sign(canonical_request, t):
        bytes = hex_encode_sha256_hash(canonical_request)
        return "%s\n%s\n%s" % (ALGORITHM, datetime.strftime(t, BASIC_DATE_FORMAT), bytes)

else:
    from urllib.parse import quote, unquote


    def hmacsha256(key_byte, message):
        return hmac.new(key_byte.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()


    def string_to_sign(canonicalRequest, t):
        bytes = hex_encode_sha256_hash(canonicalRequest.encode('utf-8'))
        return "%s\n%s\n%s" % (ALGORITHM, datetime.strftime(t, BASIC_DATE_FORMAT), bytes)


def url_encode(s):
    return quote(s, safe='~')


def find_header(r, header):
    for k in r.headers:
        if k.lower() == header.lower():
            return r.headers[k]
    return None


def hex_encode_sha256_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()


# HWS API Gateway Signature
class HttpRequest:
    def __init__(self, method="", url="", headers=None, body=""):
        self.method = method
        spl = url.split("://", 1)
        scheme = 'http'
        if len(spl) > 1:
            scheme = spl[0]
            url = spl[1]
        query = {}
        spl = url.split('?', 1)
        url = spl[0]
        if len(spl) > 1:
            for kv in spl[1].split("&"):
                spl = kv.split("=", 1)
                key = spl[0]
                value = ""
                if len(spl) > 1:
                    value = spl[1]
                if key != '':
                    key = unquote(key)
                    value = unquote(value)
                    if key in query:
                        query[key].append(value)
                    else:
                        query[key] = [value]
        spl = url.split('/', 1)
        host = spl[0]
        if len(spl) > 1:
            url = '/' + spl[1]
        else:
            url = '/'

        self.scheme = scheme
        self.host = host
        self.uri = url
        self.query = query
        if headers is None:
            self.headers = {}
        else:
            self.headers = copy.deepcopy(headers)
        if sys.version_info.major < 3:
            self.body = body
        else:
            self.body = body.encode("utf-8")


BASIC_DATE_FORMAT = "%Y%m%dT%H%M%SZ"
ALGORITHM = "SDK-HMAC-SHA256"
HEADER_X_DATE = "X-Sdk-Date"
HEADER_HOST = "host"
HEADER_AUTHORIZATION = "Authorization"
HEADER_CONTENT_SHA256 = "x-sdk-content-sha256"


def normalize_request(r, signature_headers):
    """ Build a CanonicalRequest from a regular request string """
    headers = normalize_headers(r, signature_headers)
    hex_encode = find_header(r, HEADER_CONTENT_SHA256)
    if hex_encode is None:
        hex_encode = hex_encode_sha256_hash(r.body)
    return "%s\n%s\n%s\n%s\n%s\n%s" % (r.method.upper(), normalize_uri(r), normalize_query_string(r),
                                       headers, ";".join(signature_headers), hex_encode)


def normalize_uri(r):
    pattens = unquote(r.uri).split('/')
    uri = []
    for v in pattens:
        uri.append(url_encode(v))
    urlpath = "/".join(uri)
    if urlpath[-1] != '/':
        urlpath = urlpath + "/"  # always end with /
    # r.uri = urlpath
    return urlpath


def normalize_query_string(r):
    keys = []
    for key in r.query:
        keys.append(key)
    keys.sort()
    a = []
    for key in keys:
        k = url_encode(key)
        value = r.query[key]
        if type(value) is list:
            value.sort()
            for v in value:
                kv = k + "=" + url_encode(str(v))
                a.append(kv)
        else:
            kv = k + "=" + url_encode(str(value))
            a.append(kv)
    return '&'.join(a)


def normalize_headers(r, signature_headers):
    a = []
    __headers = {}
    for key in r.headers:
        key_encoded = key.lower()
        value = r.headers[key]
        value_encoded = value.strip()
        __headers[key_encoded] = value_encoded
        if sys.version_info.major == 3:
            r.headers[key] = value_encoded.encode("utf-8").decode('iso-8859-1')
    for key in signature_headers:
        a.append(key + ":" + __headers[key])
    return '\n'.join(a) + "\n"


def signed_headers(r):
    a = []
    for key in r.headers:
        a.append(key.lower())
    a.sort()
    return a


def sign_string_to_sign(string_to_be_signed, signing_key):
    """ Create the HWS Signature. """
    hm = hmacsha256(signing_key, string_to_be_signed)
    return binascii.hexlify(hm).decode()


def auth_header_value(signature, app_key, signature_headers):
    """
    Get the finalized value for the "Authorization" header.  The signature
    parameter is the output from sign_string_to_sign
    """
    return "%s Access=%s, SignedHeaders=%s, Signature=%s" % (
        ALGORITHM, app_key, ";".join(signature_headers), signature)


class Signer:
    def __init__(self):
        self.key = ""
        self.secret = ""

    def verify(self, r, authorization):
        if sys.version_info.major == 3 and isinstance(r.body, str):
            r.body = r.body.encode('utf-8')
        header_time = find_header(r, HEADER_X_DATE)
        if header_time is None:
            return False
        else:
            t = datetime.strptime(header_time, BASIC_DATE_FORMAT)

        signature_headers = signed_headers(r)
        canonical_request = normalize_request(r, signature_headers)
        signature_string = string_to_sign(canonical_request, t)
        return authorization == sign_string_to_sign(signature_string, self.secret)

    def sign(self, r):
        """ SignRequest set Authorization header """
        if sys.version_info.major == 3 and isinstance(r.body, str):
            r.body = r.body.encode('utf-8')
        header_time = find_header(r, HEADER_X_DATE)
        if header_time is None:
            t = datetime.utcnow()
            r.headers[HEADER_X_DATE] = datetime.strftime(t, BASIC_DATE_FORMAT)
        else:
            t = datetime.strptime(header_time, BASIC_DATE_FORMAT)

        have_host = False
        for key in r.headers:
            if key.lower() == 'host':
                have_host = True
                break
        if not have_host:
            r.headers["host"] = r.host
        signature_headers = signed_headers(r)
        canonical_request = normalize_request(r, signature_headers)
        signature_string = string_to_sign(canonical_request, t)
        signature = sign_string_to_sign(signature_string, self.secret)
        auth_value = auth_header_value(signature, self.key, signature_headers)
        r.headers[HEADER_AUTHORIZATION] = auth_value
        r.headers["content-length"] = str(len(r.body))
        query_string = normalize_query_string(r)
        if query_string != "":
            r.uri = r.uri + "?" + query_string


def send_signed_request(ak: str, sk: str, region: str, project_id: str, method: str, url: str,
                        body: dict = None):
    sig = Signer()
    sig.key = ak
    sig.secret = sk
    r = HttpRequest(method, url.replace(
        "$PROJECT_ID", project_id).replace("$REGION", region))
    r.body = "" if len(body.keys()) == 0 else json.dumps(body)
    r.headers = {
        "X-Project-Id": project_id,
        "Content-Type": "application/json"
    }
    sig.sign(r)
    response = requests.request(
        r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)
    if response.status_code > 299:
        raise Exception(f"Error: {response.status_code} {response.text}")
    return response
