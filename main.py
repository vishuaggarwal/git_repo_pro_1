# This code is essentially processing and storing Telegram 
# messages continuously. It first checks if it's the first run, and 
# if so it fetches the initial set of messages from the Telegram channels. 
# Then it continues to process incoming messages in real-time.

################################################################

# main.py
# Importing necessary libraries such as argparse, asyncio, sqlalchemy, and telethon
import argparse
import asyncio
import datetime
from datetime import datetime, timedelta, timezone
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from telethon import events
from sqlalchemy import not_, and_, delete, func, false, text
from db.models import Base, TelegramChannel, TelegramMessage as Message, TelegramSentimentMessage as SNTMSG
from db.models import TelegramSentimentMessageHistory as SNTMSG_HIST, TelegramMessageHistory as Message_HIST
from telegram.client import init_telegram_client
from telegram.scraper import scrape_history
from telegram.filters import filter_messages
from db.db_tasks import daily_tasks
from db.models import Database
import datetime



# Import logger from log_config
from log_config import configure_logger

main_logger = configure_logger('main', 'main.log')
handler_logger = configure_logger('handler', 'handler.log')
save_message_logger = configure_logger('save_message', 'save_message.log')
check_duplicate_logger = configure_logger('check_duplicate', 'duplicate_message.log')

# Initialising the database
database = Database()

# Asynchronous function to fetch and process messages from various Telegram channels


async def main():
    client = await init_telegram_client()
    Session = sessionmaker(database.engine, expire_on_commit=False, class_=AsyncSession)
    daily_tasks_coroutine = daily_tasks(Session)
    asyncio.create_task(daily_tasks_coroutine)

    check_dup_task = asyncio.create_task(check_for_duplicates(Session))
    client.add_event_handler(handler, events.NewMessage())
    await client.start()
    while True:
        print(f"################## DEBUGGING STARTED ##################")
        async with Session() as session:
            async with session.begin():
                channel_ids_result = await session.execute(select(TelegramChannel.chnl_id))
                channel_ids = {row for row in channel_ids_result.scalars().all()}

        for channel_id in channel_ids:
            print(f"DEBUG: Processing channel ID: {channel_id}")
            async with Session() as session:
                async with session.begin():
                    print(f"DEBUG: Scraping history messages for channel ID: {channel_id}")
        #
        #            # Define the offset_date for scraping
        #            offset_date = datetime.datetime.now() - datetime.timedelta(days=60)
        #
        #            messages = await scrape_history(client, channel_id, offset_date=offset_date)
        #
        #            print(f"DEBUG: Scraped {len(messages)} messages for channel ID: {channel_id}")
        #
        #            if messages:
        #                filtered_messages, plain_messages = filter_messages(messages)
        #                if filtered_messages:
        #                    for msg in filtered_messages:
        #                        await save_message(msg, Session)
        #                if plain_messages:
        #                    for msg in plain_messages:
        #                        await save_sentiment_message(msg, Session)

        #print("############# Sleeping for 60 seconds... ##############")
        await asyncio.sleep(60)

    daily_tasks_coroutine.cancel()
    daily_tasks_coroutine = daily_tasks(Session)
    asyncio.create_task(daily_tasks_coroutine)
    await client.run_until_disconnected()
# Function to act according to the incoming events
async def handler(event):
    Session = sessionmaker(database.engine, expire_on_commit=False, class_=AsyncSession)
    try:
        message = event.message
        msg_data = {
            "id": message.id,
            "text": message.text,
            "chat_id": message.chat_id,
            "date": message.date
        }

        async with Session() as session:
            async with session.begin():
                today_query = await session.execute(
                    select(func.max(Message.msg_id)).where(Message.chnl_id == message.chat_id)
                )
                sentiment_today_query = await session.execute(
                    select(func.max(SNTMSG.msg_id)).where(SNTMSG.chnl_id == message.chat_id)
                )
                last_msg_id_today = func.max(
                    today_query.scalar_one_or_none(),
                    sentiment_today_query.scalar_one_or_none()
                )

        # Only handle new messages that are not yet in today's tables
        if message.id > last_msg_id_today:
            filtered_messages, plain_messages = filter_messages([msg_data])
            if filtered_messages:
                for msg in filtered_messages:
                    await save_message(msg, Session, Message)
            if plain_messages:
                for msg in plain_messages:
                    await save_sentiment_message(msg, Session, SNTMSG)
    except Exception as e:
        handler_logger.error("Error in handler function: ", exc_info=True)


def get_current_date_in_ist():
    offset = timedelta(hours=5, minutes=30)
    ist = timezone(offset)
    return datetime.datetime.now(ist)

def convert_date_to_ist(date):
    offset = timedelta(hours=5, minutes=30)
    ist = timezone(offset)
    return date.astimezone(ist)

def get_data_from_index(dict_obj, key, index):
    try:
        return dict_obj.get(key, [])[index]
    except IndexError:
        return None

async def save_sentiment_message(msg, Session):
    date = get_current_date_in_ist()
    table = SNTMSG if convert_date_to_ist(msg['date']).date() == date.date() else SNTMSG_HIST
    try:
        utc_offset_sec = 5.5 * 60 * 60
        offset = timedelta(seconds=utc_offset_sec)

        async with Session() as session:
            async with session.begin():
                session.add(table(
                    msg_id=msg['id'],
                    message=msg['text'],
                    chnl_id=msg['chat_id'],
                    msg_date=msg['date'] + offset
                ))
    except Exception as e:
        save_message_logger.error("Error in save_sentiment_message function: ", exc_info=True)



async def save_message(msg, Session):
    date = get_current_date_in_ist()
    table = Message if convert_date_to_ist(msg['date']).date() == date.date() else Message_HIST

    try:
        utc_offset_sec = 5.5 * 60 * 60
        offset = timedelta(seconds=utc_offset_sec)

        async with Session() as session:
            async with session.begin():
                session.add(table(
                    msg_id=msg['id'],
                    chnl_id=msg['channel_id'],
                    lev_val=get_data_from_index(msg, 'lev_val', 0),
                    lev_type=get_data_from_index(msg, 'lev_type', 0),
                    pos_type=get_data_from_index(msg, 'position_type', 0),
                    ticker=get_data_from_index(msg, 'coin', 0),
                    msg_date=msg['date'] + offset,
                    ent_1=get_data_from_index(msg, 'entry', 0),
                    ent_2=get_data_from_index(msg, 'entry', 1),
                    ent_3=get_data_from_index(msg, 'entry', 2),
                    tar_1=get_data_from_index(msg, 'tar', 0),
                    tar_2=get_data_from_index(msg, 'tar', 1),
                    tar_3=get_data_from_index(msg, 'tar', 2),
                    tar_4=get_data_from_index(msg, 'tar', 3),
                    tar_5=get_data_from_index(msg, 'tar', 4),
                    tar_6=get_data_from_index(msg, 'tar', 5),
                    tar_7=get_data_from_index(msg, 'tar', 6),
                    tar_8=get_data_from_index(msg, 'tar', 7),
                    tar_9=get_data_from_index(msg, 'tar', 8),
                    stop=get_data_from_index(msg, 'stop', 0),
                ))
    except Exception as e:
        save_message_logger.error("Error in save_message function: ", exc_info=True)


async def check_for_duplicates(Session):
    utc_offset_sec = 5.5 * 60 * 60
    offset = timedelta(seconds=-utc_offset_sec)

    while True:
        try:
            async with Session() as session:
                async with session.begin():
                    print("################ Checking for duplicates... ################")
                    check_time = datetime.now() + offset - timedelta(hours=24)

                    # Condition 1: Delete rows with duplicate ent_1, ent_2, tar_1, tar_2, stop, chnl_id, msg_id, and time_stamp based on id
                    condition_1_dups_stmt = select(Message).\
                        where(Message.msg_date > check_time).\
                        group_by(Message.msg_id, Message.ent_1, Message.ent_2, Message.tar_1, Message.tar_2, Message.stop, Message.chnl_id, Message.msg_date).\
                        having(func.count(Message.msg_id) > 1)

                    result_condition_1 = await session.execute(condition_1_dups_stmt)
                    condition_1_dups = result_condition_1.scalars().all()

                    if condition_1_dups:
                        for row in condition_1_dups:
                            delete_stmt_condition_1 = delete(Message).where(and_(Message.msg_id == row.msg_id, 
                                                        Message.ent_1 == row.ent_1, 
                                                        Message.ent_2 == row.ent_2, 
                                                        Message.tar_1 == row.tar_1, 
                                                        Message.tar_2 == row.tar_2, 
                                                        Message.stop == row.stop, 
                                                        Message.chnl_id == row.chnl_id, 
                                                        Message.msg_date == row.msg_date, 
                                                        Message.id != row.id))
                            await session.execute(delete_stmt_condition_1)

                    # Condition 2: Delete rows with duplicate ent_1, ent_2, tar_1, tar_2, stop, chnl_id, but different msg_id and time_stamp, based on id
                    condition_2_query = """DELETE FROM telegram_messages 
                                          WHERE id NOT IN (
                                             SELECT MAX(id)
                                             FROM telegram_messages
                                             WHERE msg_date > :check_time
                                             GROUP BY ent_1, ent_2, tar_1, tar_2, stop, chnl_id);"""
                                         
                    await session.execute(text(condition_2_query).params(check_time=check_time))
                    await session.commit()

        except Exception as e:
            check_duplicate_logger.error(f"Error while checking for duplicates: {str(e)}")
        finally:
            await asyncio.sleep(600)
# Call the necessary functions to start the script
async def run():
    await database.create_engine()
    await database.create_tables()
    await main()

# Start point of the script
if __name__ == "__main__":
    asyncio.run(run())