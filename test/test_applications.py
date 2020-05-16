import pytest
import hyron
from testconstants import TEST_NONEXIST_APP


def _get_builtin_app_config():
    return hyron.helpers.load_yaml(
        hyron.helpers.get_builtin_filename("apps"))


def _get_app_loader():
    config = _get_builtin_app_config()["objects"]["appdefs"]
    return hyron.apps.ApplicationLibraryLoader().load(config)


def _get_ssh_app():
    return hyron.apps.PortApplication.tcp_port(22)


def _get_dns_app():
    return hyron.apps.PortApplication.tcp_port(53)


def _get_icmp4_app():
    return hyron.apps.Application(1)


def _get_anytcp_app():
    return hyron.apps.PortApplication.tcp_port_range(1, 65535)


def _get_anyudp_app():
    return hyron.apps.PortApplication.tcp_port_range(1, 65535)


def _get_demon_app():
    return hyron.apps.Application(666)


def test_builtin_apps_set_access():
    ldr = _get_app_loader()

    assert("any" in ldr.appgroups)
    assert("any-tcp" in ldr.apps)
    assert("any-udp" in ldr.apps)


def test_builtin_apps_nonexist():
    ldr = _get_app_loader()

    with pytest.raises(KeyError):
        ldr[TEST_NONEXIST_APP]


def test_builtin_names():
    ldr = _get_app_loader()

    names = list(ldr.apps) + list(ldr.appgroups)

    for name in names:
        assert(ldr[name].name == name)


def test_deterministic_names():
    answers = [
        (_get_ssh_app(), "protocol_tcp_port_22"),
        (_get_icmp4_app(), "protocol_icmp"),
        (_get_anytcp_app(), "protocol_tcp_ports_1_to_65535"),
        (_get_demon_app(), "protocol_666")
    ]

    names = []
    apps = []

    for obj, answer in answers:
        apps.append(obj)
        names.append(answer)
        assert(obj.name == answer)
        assert(hash(obj) == hash(answer))

    group = hyron.apps.ApplicationGroup(apps)
    names = ','.join(names)

    assert(group.name == f"group({names})")


def test_comparisons():
    assert(_get_icmp4_app() == _get_icmp4_app())
    assert(53 in _get_dns_app())
    assert(_get_ssh_app() <= _get_anytcp_app())
