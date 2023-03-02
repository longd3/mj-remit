import os, json, consul
from dotenv import load_dotenv


load_dotenv()


consul_client = consul.Consul(scheme="https", port=443,
                              host=os.getenv("CONSUL_URL").split("https://")[-1],
                              token=os.getenv("CONSUL_TOKEN"))

MJR_SECRETS = json.loads(consul_client.kv.get(os.getenv('CONSUL_PREFIX'))[1].get('Value').decode('UTF-8'))

def extract_secret(key, secrets=MJR_SECRETS):
    # first priority: local env vars & .env
    # second priority: revealed by consul
    return os.getenv(key, None) or secrets.get(key, None)

# Configuration
MJD_APP_ID = extract_secret("MJD_APP_ID")
MJD_COMMAND_VERSION_ID = extract_secret("MJD_COMMAND_VERSION_ID")
MJD_DATA_COMMAND_ID = extract_secret("MJD_DATA_COMMAND_ID")
MJR_TOKEN = extract_secret("MJR_TOKEN")
IMPERSONATOR_TOKEN = extract_secret("IMPERSONATOR_TOKEN")
DISCORD_SERVER_ID = extract_secret("DISCORD_SERVER_ID")
DISCORD_CHANNEL_ID = extract_secret("DISCORD_CHANNEL_ID")
RABBITMQ_URL= extract_secret("RABBITMQ_URL")
RABBITMQ_EXCHANGE_MJ_EVENT= extract_secret("RABBITMQ_EXCHANGE_MJ_EVENT")
RABBITMQ_QUEUE_MJ_EVENT_URL= extract_secret("RABBITMQ_QUEUE_MJ_EVENT_URL")
MONGODB_URL = extract_secret("MONGODB_URL")
MONGODB_COLLECTION_RAW_RESPONSES = extract_secret("MONGODB_COLLECTION_RAW_RESPONSES")
MONGODB_COLLECTION_ARTWORKS = extract_secret("MONGODB_COLLECTION_ARTWORKS")
MONGODB_COLLECTION_MJR_LOGS = extract_secret("MONGODB_COLLECTION_MJR_LOGS")
SLOGAN = extract_secret("SLOGAN")

# Global params
BROADCAST_AND_PERSIST_ENABLED = False
USE_MESSAGED_CHANNEL = True # if True then in case of private channel: MJR has to be invited to
TARGET_ID = ""
TARGET_HASH = ""
DISCORD_INTERACTIONS_URL="https://discord.com/api/v9/interactions"
FINAL_OUTPUT_MESSAGE_SUFFIXES = ("(relaxed)", "(fast)")
INPUT_TICKET_PREFIX = "@MJR"
LOG_PREFIX = "[MJR-log]"
MJR_TARGET_MATCH = "$MJR"

