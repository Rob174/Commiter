from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import json
from typing import Optional


class Status:
    config_path = Path(__file__).parent.parent.joinpath(
        'data', 'config.json')

    @staticmethod
    def get_iterable(specific_id: Optional[str] = None) -> list:
        """Get the keys of dict with specific id type. Leave none for deafault config.json status keys."""
        with open(Status.config_path, encoding='utf-8') as f:
            dico = json.load(f)
        if specific_id is not None:
            return [dico["status"][k][specific_id] for k in dico["status"].keys()]
        return list(dico["status"].keys())

    @staticmethod
    def get(identifier: str, specific_id: Optional[str] = None) -> dict:
        """Get the status dict from the config file. The user can indeferently specify a key as presented in the config files under status 
        or directly according to the additionnal identifiers specified in the config file (under status.identifiers)
        """
        with open(Status.config_path, encoding='utf-8') as f:
            dico_name = json.load(f)
        dico_id_possible = {
            "default": {mainkey: {"default": mainkey, **detail} for mainkey, detail in dico_name["status"].items()},
            **{
                main_key: {
                    v[main_key]:
                    {"default": k,
                     **{kdetail: vdetail for kdetail, vdetail in v.items()}
                     }
                    for k, v in dico_name["status"].items()
                }
                for main_key in dico_name["status.identifiers"]
            }
        }
        if specific_id is not None:
            return dico_id_possible[specific_id][identifier]
        for name_dico, dico in dico_id_possible.items():
            if identifier in dico:
                return dico[identifier]
        raise KeyError(
            f"{identifier} is not a valid identifier in config.json (tested on name key (original key), {', '.join(dico_name['status.identifiers'])} keys)")

    @staticmethod
    def get_default_status():
        with open(Status.config_path, encoding='utf-8') as f:
            dico_name = json.load(f)
        if dico_name["status.default"] not in dico_name["status"]:
            raise KeyError(
                f"{dico_name['status.default']} is not in config.json keys under 'status' field. Keys present: {list(dico_name['status'])}")
        return Status.get(dico_name["status.default"], specific_id="default")
