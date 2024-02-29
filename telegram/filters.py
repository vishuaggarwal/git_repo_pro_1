# telegram/filters.py

KEYWORD = 'python' 

def filter_messages(messages):
  """
  Filters a list of messages, returning only those 
  that contain the specified keyword.
  """

  filtered = []

  for msg in messages:
    if KEYWORD in msg.text:
      filtered.append(msg)

  return filtered