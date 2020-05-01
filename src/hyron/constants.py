PROTOCOLS = {
    1: 'ICMP',
    4: 'TUNIP4',
    6: 'TCP',
    17: 'UDP',
    41: 'TUNIP6',
    47: 'GRE',
    132: 'SCTP'
}

AWS_IP_RANGES = "https://ip-ranges.amazonaws.com/ip-ranges.json"

ACTION_PERMIT = "permit"
ACTION_REJECT = "reject"
ACTION_IGNORE = "ignore"

ACTIONS = [
    ACTION_PERMIT,
    ACTION_REJECT,
    ACTION_IGNORE
]

DICT = "dict"
XDICT = {
    "name": "dict",
    "exclusive": True,
}

LOADER_SCHEMA = {
    "meta": XDICT,
    "artifacts": XDICT,
    "rules": DICT,
    "rulesets": DICT,
    "objects": DICT,
}

DEF_ENCODING = "utf8"
