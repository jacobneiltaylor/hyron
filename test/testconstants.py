import os

TEST_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

PREFIX_LIST_TESTS = {
    "cloudflare": {
        "contains": ["104.16.0.0/32", "2400:cb00::/128"]
    },
    "fullbogons": {
        "contains": ["10.20.30.40/32", "::1/128"],
        "not": ["8.8.8.8/32"]
    },
    "any": {
        "contains": ["1.1.1.1/32", "ff80::1111/128"]
    },
    "aws": {
        "contains": ["18.232.234.12/32"]
    },
    "aws-sydney-ec2": {
        "contains": ["13.236.45.1/32"],
        "not": ["18.232.234.12/32"]
    }
}
