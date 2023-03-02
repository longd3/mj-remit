import settings
import requests

from core.common import mj_random_ref, build_base_payload


def imagine(prompt: str):
    base_payload = build_base_payload()
    nonce = base_payload.get("nonce", mj_random_ref())
    payload = base_payload | {
        "type": 2,
        "data": {
            "version": settings.MJD_COMMAND_VERSION_ID,
            "id": settings.MJD_DATA_COMMAND_ID,
            "name": "imagine",
            "type": 1,
            "options": [
                {
                    "type": 3,
                    "name": "prompt",
                    "value": f"{nonce}\n{prompt}"
                }
            ],
            "application_command": {
                "id": settings.MJD_DATA_COMMAND_ID,
                "application_id": settings.MJD_APP_ID,
                "version": settings.MJD_COMMAND_VERSION_ID,
                "default_permission": True,
                "default_member_permissions": None,
                "type": 1,
                "nsfw": False,
                "name": "imagine",
                "description": settings.SLOGAN,
                "dm_permission": True,
                "options": [
                    {
                        "type": 3,
                        "name": "prompt",
                        "description": "The prompt to imagine",
                        "required": True
                    }
                ]
            },
            "attachments": []
        }
    }

    header = {
        'authorization': settings.IMPERSONATOR_TOKEN
    }
    response = requests.post(settings.DISCORD_INTERACTIONS_URL,
                             json=payload, headers=header)
    return response


def upscale(index: int, message_id: str, message_hash: str):
    payload = build_base_payload() | {
        "type": 3,
        "message_id": message_id,
        "data": {
            "component_type": 2,
            "custom_id": f"MJ::JOB::upsample::{index}::{message_hash}"
        }
    }
    header = {
        'authorization': settings.IMPERSONATOR_TOKEN
    }
    response = requests.post(settings.DISCORD_INTERACTIONS_URL,
                             json=payload, headers=header)
    return response


def upscale_max(message_id: str, message_hash: str):
    payload = build_base_payload() | {
        "type": 3,
        "message_id": message_id,
        "data": {
            "component_type": 2,
            "custom_id": f"MJ::JOB::upsample_max::1::{message_hash}::SOLO"
        }
    }
    header = {
        'authorization': settings.IMPERSONATOR_TOKEN
    }
    response = requests.post(settings.DISCORD_INTERACTIONS_URL,
                             json=payload, headers=header)
    return response

def reroll(message_id: str, message_hash: str):
    payload = build_base_payload() | {
        "type": 3,
        "message_id": message_id,
        "data": {
            "component_type": 2,
            "custom_id": f"MJ::JOB::reroll::0::{message_hash}::SOLO"
        }
    }
    header = {
        'authorization': settings.IMPERSONATOR_TOKEN
    }
    response = requests.post(settings.DISCORD_INTERACTIONS_URL,
                             json=payload, headers=header)
    return response

def variate(index: int, message_id: str, message_hash: str):
    payload = build_base_payload() | {
        "type": 3,
        "message_id": message_id,
        "data": {
            "component_type": 2,
            "custom_id": f"MJ::JOB::variation::{index}::{message_hash}"
        }
    }
    header = {
        'authorization': settings.IMPERSONATOR_TOKEN
    }
    response = requests.post(settings.DISCORD_INTERACTIONS_URL,
                             json=payload, headers=header)
    return response


