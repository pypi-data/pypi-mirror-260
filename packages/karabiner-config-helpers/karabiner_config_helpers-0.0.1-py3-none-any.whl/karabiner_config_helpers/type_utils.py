#!/usr/bin/env python3
import sys
from typing import Optional, Union
# local
from .keyboard_base import KeyResolver, NoKeyMappingFoundError, shift, normal

def string_to_keymap_json(string_to_type: str, move_cursor_backwards: int, key_resolver: KeyResolver) -> list[dict]:
    list_of_keystrokes: list[dict] = []
    for character in string_to_type:
        try:
            list_of_keystrokes += key_resolver.get_to_keys_for_char(character)
        except NoKeyMappingFoundError as ex:
            try:
                print(ex, file=sys.stderr)
                list_of_keystrokes += key_resolver.get_to_keys_for_char("?")
            except NoKeyMappingFoundError:
                list_of_keystrokes += shift("x")
                print("Meta-Error: Failed to resolve '?' character to signify failed resolve", file=sys.stderr)

    if move_cursor_backwards < 0:
        raise Exception(f"Cursor backwards count can not be a negative number, but is {move_cursor_backwards}")
    elif move_cursor_backwards > 0:
        list_of_keystrokes += [normal("left_arrow")] * move_cursor_backwards
    return list_of_keystrokes


def create_manipulators(string_to_type: str, move_cursor_backwards: int, from_key: str, from_modifiers: list[str], key_resolver: KeyResolver, parallels_key_resolver: Optional[KeyResolver]) -> list[dict]:
    from_dict: dict[str,Union[list,dict,str]] = {
        "modifiers": {
            "mandatory": from_modifiers,
            "optional": [
                "caps_lock"
            ]
        }
    }
    if from_key.startswith("button"):
        # This is a mouse button, use the correct key
        from_dict = {
            "pointing_button": from_key
        }
    else:
        # Will probably be a normal key
        from_dict["key_code"] = from_key

    if parallels_key_resolver:
        return [
            {
                "type": "basic",
                "from": from_dict,
                "to": string_to_keymap_json(string_to_type, move_cursor_backwards, parallels_key_resolver),
                "conditions": [
                    {
                        "type": "frontmost_application_if",
                        "bundle_identifiers": ["^com\\.parallels\\.desktop\\.console$"]
                    }
                ]
            },
            {
                "type": "basic",
                "from": from_dict,
                "to": string_to_keymap_json(string_to_type, move_cursor_backwards, key_resolver),
                "conditions": [
                    {
                        "type": "frontmost_application_unless",
                        "bundle_identifiers": ["^com\\.parallels\\.desktop\\.console$"]
                    }
                ]
            }
        ]
    else:
        return [
            {
                "type": "basic",
            "from": from_dict,
            "to": string_to_keymap_json(string_to_type, move_cursor_backwards, key_resolver)
          }
        ]

def type_text_main(string_to_type: str, description: str, move_cursor_backwards: int, from_key_combos: list[str], key_resolver: KeyResolver, parallels_key_resolver: Optional[KeyResolver]) -> dict:
    manipulators = []

    for key_combo in from_key_combos:
        parts = key_combo.split("+")
        from_key = parts[-1]
        from_modifiers = parts[:-1]
        manipulators += create_manipulators(string_to_type, move_cursor_backwards, from_key, from_modifiers, key_resolver, parallels_key_resolver)

    return {
        "description": description,
        "manipulators": manipulators,
    }

