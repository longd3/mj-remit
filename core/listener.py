import json

import pymongo
from pymongo import errors
from pika import exceptions

import settings, re, pika
from core.common import build_basic_doc, log_to_discord


async def set_mj_interaction_target(message):
    try:
        settings.TARGET_ID = str(message.reference.message_id)
        # Get the hash from the url
        settings.TARGET_HASH = str((message.reference.resolved.attachments[0].url.split("_")[-1]).split(".")[0])
    except Exception as e:
        await log_to_discord(message.channel, f"Setting target failed because {e}")
        await message.delete()
        return
    if str(message.reference.resolved.author.id) != settings.MJD_APP_ID:
        await log_to_discord(message.channel, "Use the command only when you reply to MidJourney")
        await message.delete()
        return
    await log_to_discord(message.channel, "target successfully set")
    await message.delete()
    

async def persist_message_posted_by_bot(message):
    if message.content.startswith(f"**{settings.INPUT_TICKET_PREFIX}") and \
            message.content.endswith(settings.FINAL_OUTPUT_MESSAGE_SUFFIXES) and \
            message.attachments:
        await persist_then_broadcast_artwork(message)
    await persist_full(message)

async def persist_full(message):
    document = {
        s: getattr(message, s)
        for s in message.__slots__ if not s.startswith("_")
                                   and hasattr(message, s)
                                   and type(getattr(message, s)) in (int, float, bool, str, type(None))
        } | build_basic_doc(message)
    if not settings.BROADCAST_AND_PERSIST_ENABLED: return
    with pymongo.MongoClient(settings.MONGODB_URL) as client:
        db = client.get_default_database()
        try:
            collection = settings.MONGODB_COLLECTION_MJR_LOGS if message.content.startswith(settings.LOG_PREFIX) \
                else settings.MONGODB_COLLECTION_RAW_RESPONSES
            db[collection].insert_one(document)
        except Exception as e:
            await log_to_discord(message.channel, f"Failed to persist raw response because {e}")


async def persist_then_broadcast_artwork(message):
    document = build_basic_doc(message) | {
        "ticket_id": re.search("@(.*)@(.*)@", message.content).group(1)
    }
    if not settings.BROADCAST_AND_PERSIST_ENABLED: return
    with pymongo.MongoClient(settings.MONGODB_URL) as client:
        db = client.get_default_database()
        try:
            db[settings.MONGODB_COLLECTION_ARTWORKS].insert_one(document)
            await broadcast(document | {"_id": str(document["_id"]) if document.get("_id") else None})
            await log_to_discord(message.channel, f"Successfully published to {settings.RABBITMQ_QUEUE_MJ_EVENT_URL}")
        except errors.PyMongoError as e:
            await log_to_discord(message.channel, f"Failed to persist via pymongo because {e}")
        except exceptions.AMQPError as e:
            await log_to_discord(message.channel, f"Failed to broadcast via pika-amqp because {e}")

async def broadcast(document):
    with pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))as r_conn:
        with r_conn.channel() as r_channel:
            r_channel.basic_publish(exchange='MJ_EVENT', routing_key='', body=json.dumps(document))
    # await log_to_discord(message.channel, "Publishing events to "
    #                                       "https://rabbitmq.toprate.io/#/queues/ai-creator-stg/mj_event "
    #                                       "is under construction!")