

from jose import jws
from jose.constants import ALGORITHMS
from jose.exceptions import JWSError

import pytest


@pytest.fixture
def claims():
    claims = {
        'a': 'b'
    }
    return claims


class TestJWS:

    def test_unicode_token(self):
        token = u'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8'
        jws.verify(token, 'secret', ['HS256'])

    def test_not_enough_segments(self):
        token = 'eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8'
        with pytest.raises(JWSError):
            jws.verify(token, 'secret', ['HS256'])

    def test_header_invalid_padding(self):
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9A.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8'
        with pytest.raises(JWSError):
            jws.verify(token, 'secret', ['HS256'])

    def test_header_not_json(self):
        token = 'dGVzdA.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8'
        with pytest.raises(JWSError):
            jws.verify(token, 'secret', ['HS256'])

    def test_claims_invalid_padding(self):
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.AeyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8'
        with pytest.raises(JWSError):
            jws.verify(token, 'secret', ['HS256'])

    def test_claims_not_json(self):
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dGVzdA.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8'
        with pytest.raises(JWSError):
            jws.verify(token, 'secret', ['HS256'])

    def test_invalid_key(self, claims):
        with pytest.raises(JWSError):
            jws.sign(claims, 'secret', algorithm='RS256')


class TestHMAC:

    def test_cookbook(self, claims):
        token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImJpbGJvLmJhZ2dpbnNAaG9iYml0b24uZXhhbXBsZSJ9" \
            ".SXTigJlzIGEgZGFuZ2Vyb3VzIGJ1c2luZXNzLCBGcm9kbywgZ29pbmcgb3V0IHlvdXIgZG9" \
            "vci4gWW91IHN0ZXAgb250byB0aGUgcm9hZCwgYW5kIGlmIHlvdSBkb24ndCBrZWVwIHlvdXI" \
            "gZmVldCwgdGhlcmXigJlzIG5vIGtub3dpbmcgd2hlcmUgeW91IG1pZ2h0IGJlIHN3ZXB0IG9" \
            "mZiB0by4.MRjdkly7_-oTPTS3AXP41iQIGKa80A0ZmTuV5MEaHoxnW2e5CZ5NlKtainoFmKZ" \
            "opdHM1O2U4mwzJdQx996ivp83xuglII7PNDi84wnB-BDkoBwA78185hX-Es4JIwmDLJK3lfW" \
            "Ra-XtL0RnltuYv746iYTh_qHRD68BNt1uSNCrUCTJDt5aAE6x8wW1Kt9eRo4QPocSadnHXFx" \
            "nt8Is9UzpERV0ePPQdLuW3IS_de3xyIrDaLGdjluPxUAhb6L2aXic1U12podGU0KLUQSE_oI" \
            "-ZnmKJ3F4uOZDnd6QZWJushZ41Axf_fcIe8u9ipH84ogoree7vjbU5y18kDquDg"

        # jws.verify(token, key, ALGORITHMS.HS256)

    def testHMAC256(self, claims):
        token = jws.sign(claims, 'secret', algorithm=ALGORITHMS.HS256)
        assert jws.verify(token, 'secret', ALGORITHMS.HS256) == claims

    def testHMAC384(self, claims):
        token = jws.sign(claims, 'secret', algorithm=ALGORITHMS.HS384)
        assert jws.verify(token, 'secret', ALGORITHMS.HS384) == claims

    def testHMAC512(self, claims):
        token = jws.sign(claims, 'secret', algorithm=ALGORITHMS.HS512)
        assert jws.verify(token, 'secret', ALGORITHMS.HS512) == claims

    def test_wrong_alg(self, claims):
        token = jws.sign(claims, 'secret', algorithm=ALGORITHMS.HS256)
        with pytest.raises(JWSError):
            jws.verify(token, 'secret', ALGORITHMS.HS384)

    def test_wrong_key(self, claims):
        token = jws.sign(claims, 'secret', algorithm=ALGORITHMS.HS256)
        with pytest.raises(JWSError):
            jws.verify(token, 'another', ALGORITHMS.HS256)

    def test_unsupported_alg(self, claims):
        with pytest.raises(JWSError):
            jws.sign(claims, 'secret', algorithm='SOMETHING')

    def test_add_headers(self, claims):

        additional_headers = {
            'test': 'header'
        }

        expected_headers = {
            'test': 'header',
            'alg': 'HS256',
            'typ': 'JWT',
        }

        token = jws.sign(claims, 'secret', headers=additional_headers)
        header, claims, signing_input, signature = jws._load(token)
        assert expected_headers == header


rsa_private_key = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""

rsa_public_key = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtSKfSeI0fukRIX38AHlK
B1YPpX8PUYN2JdvfM+XjNmLfU1M74N0VmdzIX95sneQGO9kC2xMIE+AIlt52Yf/K
gBZggAlS9Y0Vx8DsSL2HvOjguAdXir3vYLvAyyHin/mUisJOqccFKChHKjnk0uXy
/38+1r17/cYTp76brKpU1I4kM20M//dbvLBWjfzyw9ehufr74aVwr+0xJfsBVr2o
aQFww/XHGz69Q7yHK6DbxYO4w4q2sIfcC4pT8XTPHo4JZ2M733Ea8a7HxtZS563/
mhhRZLU5aynQpwaVv2U++CL6EvGt8TlNZOkeRv8wz+Rt8B70jzoRpVK36rR+pHKl
XhMGT619v82LneTdsqA25Wi2Ld/c0niuul24A6+aaj2u9SWbxA9LmVtFntvNbRaH
XE1SLpLPoIp8uppGF02Nz2v3ld8gCnTTWfq/BQ80Qy8e0coRRABECZrjIMzHEg6M
loRDy4na0pRQv61VogqRKDU2r3/VezFPQDb3ciYsZjWBr3HpNOkUjTrvLmFyOE9Q
5R/qQGmc6BYtfk5rn7iIfXlkJAZHXhBy+ElBuiBM+YSkFM7dH92sSIoZ05V4MP09
Xcppx7kdwsJy72Sust9Hnd9B7V35YnVF6W791lVHnenhCJOziRmkH4xLLbPkaST2
Ks3IHH7tVltM6NsRk3jNdVMCAwEAAQ==
-----END PUBLIC KEY-----"""


class TestRSA:

    def test_RSA256(self, claims):
        token = jws.sign(claims, rsa_private_key, algorithm=ALGORITHMS.RS256)
        assert jws.verify(token, rsa_public_key, ALGORITHMS.RS256) == claims

    def test_RSA384(self, claims):
        token = jws.sign(claims, rsa_private_key, algorithm=ALGORITHMS.RS384)
        assert jws.verify(token, rsa_public_key, ALGORITHMS.RS384) == claims

    def test_RSA512(self, claims):
        token = jws.sign(claims, rsa_private_key, algorithm=ALGORITHMS.RS512)
        assert jws.verify(token, rsa_public_key, ALGORITHMS.RS512) == claims

    def test_wrong_alg(self, claims):
        token = jws.sign(claims, rsa_private_key, algorithm=ALGORITHMS.RS256)
        with pytest.raises(JWSError):
            jws.verify(token, rsa_public_key, ALGORITHMS.RS384)

    def test_wrong_key(self, claims):
        token = jws.sign(claims, rsa_private_key, algorithm=ALGORITHMS.RS256)
        with pytest.raises(JWSError):
            jws.verify(token, rsa_public_key, ALGORITHMS.HS256)

ec_private_key = """-----BEGIN EC PRIVATE KEY-----
MIHcAgEBBEIBzs13YUnYbLfYXTz4SG4DE4rPmsL3wBTdy34JcO+BDpI+NDZ0pqam
UM/1sGZT+8hqUjSeQo6oz+Mx0VS6SJh31zygBwYFK4EEACOhgYkDgYYABACYencK
8pm/iAeDVptaEZTZwNT0yW/muVwvvwkzS/D6GDCLsnLfI6e1FwEnTJF/GPFUlN5l
9JSLxsbbFdM1muI+NgBE6ZLR1GZWjsNzu7BOB8RMy/mvSTokZwyIaWvWSn3hOF4i
/4iczJnzJhUKDqHe5dJ//PLd7R3WVHxkvv7jFNTKYg==
-----END EC PRIVATE KEY-----"""

ec_public_key = """-----BEGIN PUBLIC KEY-----
MIGbMBAGByqGSM49AgEGBSuBBAAjA4GGAAQAmHp3CvKZv4gHg1abWhGU2cDU9Mlv
5rlcL78JM0vw+hgwi7Jy3yOntRcBJ0yRfxjxVJTeZfSUi8bG2xXTNZriPjYAROmS
0dRmVo7Dc7uwTgfETMv5r0k6JGcMiGlr1kp94TheIv+InMyZ8yYVCg6h3uXSf/zy
3e0d1lR8ZL7+4xTUymI=
-----END PUBLIC KEY-----"""


class TestEC:

    def test_EC256(self, claims):
        token = jws.sign(claims, ec_private_key, algorithm=ALGORITHMS.ES256)
        assert jws.verify(token, ec_public_key, ALGORITHMS.ES256) == claims

    def test_EC384(self, claims):
        token = jws.sign(claims, ec_private_key, algorithm=ALGORITHMS.ES384)
        assert jws.verify(token, ec_public_key, ALGORITHMS.ES384) == claims

    def test_EC512(self, claims):
        token = jws.sign(claims, ec_private_key, algorithm=ALGORITHMS.ES512)
        assert jws.verify(token, ec_public_key, ALGORITHMS.ES512) == claims

    def test_wrong_alg(self, claims):
        token = jws.sign(claims, ec_private_key, algorithm=ALGORITHMS.ES256)
        with pytest.raises(JWSError):
            jws.verify(token, rsa_public_key, ALGORITHMS.ES384)


class TestLoad:

    def test_header_not_mapping(self):
        token = 'WyJ0ZXN0Il0.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8'
        with pytest.raises(JWSError):
            jws.verify(token, 'secret', ['HS256'])

    def test_claims_not_mapping(self):
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.WyJ0ZXN0Il0.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8'
        with pytest.raises(JWSError):
            jws.verify(token, 'secret', ['HS256'])

    def test_signature_padding(self):
        token = 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJoZWxsbyI6ICJ3b3JsZCJ9.aatvagLDLoaiJKxOKqpBXSEGy7SYSifZhjntgm9ctpyj8'
        with pytest.raises(JWSError):
            jws.verify(token, 'secret', ['HS256'])
