import uuid
import settings

def mj_random_ref():
    return f'{settings.INPUT_TICKET_PREFIX}-{str(uuid.uuid4()).replace("-","")[:8]}@'


def build_base_payload():
    return {
        "guild_id": settings.DISCORD_SERVER_ID,
        "channel_id": settings.DISCORD_CHANNEL_ID,
        "application_id": settings.MJD_APP_ID,
        "session_id": mj_random_ref(),
        "nonce": mj_random_ref(),
        "extras": {},
        "message_flags": 0
    }


def build_basic_doc(message):
    return {
        "content": message.content,
        "jump_url": message.jump_url,
        "created_at": message.created_at.isoformat(),
        "edited_at": message.edited_at.isoformat() if message.edited_at else None,
        "author": {
            "id": message.author.id,
            "avatar_url": message.author.avatar.url if message.author.avatar is not None else None,
            "display_name": message.author.display_name,
            "discriminator": message.author.discriminator,
            "is_bot": message.author.bot,
            "is_midjourney_official_bot": str(message.author.id) == settings.MJD_APP_ID,
        },
        "attachments": [{
            ss: getattr(a, ss)
            for ss in a.__slots__ if not ss.startswith("_")
                                          and hasattr(a, ss)
                                          and type(getattr(a, ss)) in (int, float, bool, str, type(None))
        } for a in message.attachments],
        "channel": {
            "id": message.channel.id,
            "name": message.channel.name,
            "jump_url": message.channel.jump_url
        }
    }

async def log_to_discord(channel, s):
    await channel.send(f"{settings.LOG_PREFIX} {s}")

