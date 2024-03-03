# Import everything that someone else may want to use
from .keyboard_base import KeyResolver, NoKeyMappingFoundError, CharRequiresMultipleKeys
from .keyboard_us import RESOLVER_US_MAC, RESOLVER_US_LINUX
from .rules import helper_insert_rule_into_config


_RESOLVERS: dict[str,KeyResolver] = {
    "us_mac": RESOLVER_US_MAC,
    "us_linux": RESOLVER_US_LINUX,
}

class NoResolverWithName(Exception):
    pass

def get_resolver(name: str) -> KeyResolver:
    if result := _RESOLVERS.get(name):
        return result
    else:
        raise NoResolverWithName(f"No resolver/keyboard layout with the value '{name}' found. Valid values are {', '.join(_RESOLVERS.keys())}")


