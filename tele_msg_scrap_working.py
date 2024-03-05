import re
from telethon import TelegramClient, events
from  unidecode import unidecode
from config import api_hash, api_id

# Compile regular expressions for pattern matching
COIN_RE = re .compile(r"[#$]?([A-Z]+)/?USDT?", re.IGNORECASE)
IGNORED_MSG_RE = re.compile(r"#SEARCH_IN_TELEGRAM_DIGILEAKBOT/USDT", re.IGNORECASE)
INSTRUCTION_RE =  re.compile(r"Buy|Long|Short|Sell|Leverage|STOP|LOSS", re.IGNORECASE)
LEVERAGE_INSTRUCTION_RE = re.compile(r"x|Leverage|cross|isolated", re.IGNORECASE)
LEVERAGE_TYPE_RE = re.compile(r"Cross|Isolated", re.IGNORECASE)
LEVERAGE_VALUE_RE = re.compile(r"\d+(X|x)_\d+(X|x)|\d+ -\d+X|\d+x", re.IGNORECASE)
POSITION_TYPE_RE = re.compile(r"Long|Short", re.IGNORECASE)

# Define a dictionary to replace certain keywords with their corresponding values
REPLACE_KEYS = {"entry targets": "entry",
                "entry target": "entry",
                "buy": "entry",
                "Entry Range": "entry",
                "Entry Price": "entry",
                "entry zone": "entry",
                "LONG/BUY": "entry",
                "long/entry": "entry",
                "entries": "entry",
                "enter": "entry",
                "tp": "tar",
                "Take Profit": "tar",
                "Take-Profit": "tar",
                "take profit target": "tar",
                "Sell": "tar",
                "take-profit targets": "tar",
                "targets": "tar",
                "target": "tar",
                "tps": "tar",
                "Target Profit": "tar",
                "tarargets": "tar",
                "sl": "stop",
                "sp": "stop",
                "stop loss": "stop", 
                "stop target": "stop",
                "stoploss": "stop",
                "stop tar": "stop",
                "stop-loss": "stop",
                "Short Term": "",
                "mi day trading shan": "",
                "mi swing trading shan": "",
                "Primary": "",
                "profit": "",
                "to": "",
                "mid term": ""}

# Define a list of channel IDs to monitor for relevant messages
CHANNELS_IDS = [1002130335326]


def check_statement(statement):
    """
    Check if the given statement contains any relevant instructions.

    Args:
        statement (str): The raw text of the message.

    Returns:
        bool: True if the statement contains relevant instructions, False otherwise.
    """

    # Check if the message is ignored
    if IGNORED_MSG_RE.findall(statement):
        return False

    # Check if the message contains any relevant instructions
    match = INSTRUCTION_RE.findall(statement)
    if match:
        match_1 = LEVERAGE_INSTRUCTION_RE.findall(statement)
        if match_1:
            return True

    return False


def handle_string_replacement(statement):
    """
    Preprocess the given statement by replacing certain keywords with their corresponding values.

    Args:
        statement (str): The raw text of the message.

    Returns:
        str: The preprocessed statement.
    """

    # Convert to lowercase, remove trailing whitespace, and replace certain characters
    statement = unidecode(statement).lower().replace('\n', ' ').replace(':', ' ').replace("-", " ").replace("_", " ").replace(",", " ").replace("=", " ").replace("$", " ")
    # Remove multiple spaces
    statement = re.sub(' +', ' ', statement)
    # Replace keywords with their corresponding values
    for key, val in REPLACE_KEYS.items():
        statement = re.sub(key.lower(), val, statement, flags=re.IGNORECASE)

    return statement


def preprocess_statement(statement):
    """
    Extract relevant data from the given statement.

    Args:
        statement (str): The preprocessed statement.

    Returns:
        str: The preprocessed  statement without relevant data.
        dict: A dictionary containing the extracted data.
    """

    # Initialize a dictionary to store extracted data
    data = {}

    # Extract the coin
    coin = COIN_RE.search(statement)
    coin = coin.group(1) if coin else ""

    # Extract the number of take profit targets
    tar_count = len(re.findall(r"tar", statement))
    if tar_count != 1:
        # Remove all single-digit numbers in sequence
        statement = re.sub(r'(( \d)+ )', ' ', statement)
        # Split the statement into two parts based on the first occurrence of "tar"
        parts = statement.split('tar', 1)
        # Remove "tar" from the second part
        parts[1] = parts[1].replace('tar', '')
        # Join the two parts back together
        statement = 'tar'.join(parts)

    # Remove all single-digit numbers in sequence
    statement = re.sub(r'(( \d)+ )', ' ', statement)
    # Replace "tar1" with "tar", "tars" with "tar", and "sp" with "stop"
    statement = statement.replace(' tar1 ', ' tar ').replace(' tars ', ' tar ')
    statement = statement.replace(' sp ', ' stop ')
    # Remove any parentheses within the statement
    statement = re.sub(r'\(.*?\)', '', statement)
    # Remove any numbers followed by a closing parenthesis
    statement = re.sub(r'\d+\)', ' ', statement)
     # Remove "tar)" from the statement
    statement = re.sub(r"tar\)", ' tar ', statement)
    # Remove extra spaces
    statement = re.sub(' +', ' ', statement)
    # Extract the leverage type and value
    lev_type_match = LEVERAGE_TYPE_RE.search(statement)
    lev_type = lev_type_match.group() if lev_type_match else None
    lev_value_match = LEVERAGE_VALUE_RE.search(statement)
    lev_value = lev_value_match.group() if lev_value_match else re.findall(r"x(\d+)", statement)



    # Update the dictionary with the extracted data
    data['coin'] = [coin]
    data['lev_type'] = [lev_type]
    data['lev_value'] = [lev_value]
    

    return statement.strip(), data


def extract_numbers(statement):
    """
    Extract the entry, take profit, and stop loss values from the given statement.

    Args:
        statement (str): The preprocessed statement.

    Returns:
        dict: A dictionary containing the extracted values.
    """
    data = {}
    # Define a dictionary to store the extracted values
    keywords = ['entry', 'tar', 'stop']
    results = {'entry': [], 'stop': [], 'tar': []}

    # Split the statement into words
    words = statement.split()

    # Initialize the current keyword to None
    current_keyword = None

    for word in words:
        # Check if the current word is a keyword
        if word in keywords:
            current_keyword = word
        # Check if the current word is a number and the current keyword is not None
        elif current_keyword and word.replace('.', '', 1).isdigit():
            results[current_keyword].append(float(word))
        # If the current word is not a keyword or a number, reset the current keyword
        else:
            current_keyword = None
    # Deduce position type based on provided logic
    position_type = None
    if 'tar' in results and 'entry' in results:
        # parse targets to float
        targets = results['tar']
        entry = results['entry']
        if len(targets) == 1 and entry:
            entry = entry[0]
            position_type = 'LONG' if targets[0] > entry else 'SHORT'
        elif len(targets) > 1:
            position_type = 'LONG' if targets[0] < targets[1] else 'SHORT'    

    data['position_type'] = [position_type]

    return results, data


# Create a Telegram client instance
client = TelegramClient('anon', api_id, api_hash)

# Define an event handler to listen for new messages in the specified channels
@client.on(events.NewMessage(chats=CHANNELS_IDS))
async def my_event_handler(event):
    try:
        # Check if the message contains relevant instructions
        statement_status = check_statement(event.raw_text)
        if statement_status:
            # Preprocess the message
            statement = handle_string_replacement(event.raw_text)
            statement, data = preprocess_statement(statement)
            # Extract the entry, take profit, and stop loss values
            numbers,pos_type = extract_numbers(statement)
            # Combine the extracted data
            data.update(numbers)
            data.update(pos_type)
            # Print the combined data
            print("Combined Data: ", data)
    except Exception as e:
        print("Error occurred: ", e)

with client:
    client.start()
    client.run_until_disconnected()