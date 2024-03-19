from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import json

api_id = 'your_api_id'
api_hash = 'your_api_hash'
phone = 'your_phone_number'
channels = ['channel1', 'channel2', 'channel3']  # add your channels here

client = TelegramClient(phone, api_id, api_hash)

async def dump_all_messages(channel):
    offset_id = 0
    limit = 100
    all_messages = []
    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        all_messages.extend(history.messages)
        offset_id = history.messages[len(history.messages)-1].id
    with open(f'{channel.id}.json', 'w') as outfile:
        json.dump([ob.to_dict() for ob in all_messages], outfile)

with client:
    for channel in channels:
        client.loop.run_until_complete(dump_all_messages(channel))
