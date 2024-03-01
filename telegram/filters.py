# telegram/filters. py

KEYWORD = 'LONG' 

def filter_messages(messages):
  """
  Filters a list of messages, returning only those 
   that contain the specified keyword.
  """

  filtered = []

  for msg in messages:
    try:
      if KEYWORD in msg.text:
        filtered.append(msg)
    except:
      continue

  return filtered
