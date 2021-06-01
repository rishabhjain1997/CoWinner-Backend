#!/usr/bin/env python
# coding: utf-8

# In[1]:
import sys

from new_slot_finder import calculate_session_updates, get_current_data, create_session_message
from notification import create_user_list, send_notifications

# We pass dist_id as command line argument
dist_id = int(sys.argv[1])
data = get_current_data(dist_id)
session_updates = calculate_session_updates(dist_id, data)
messages = []
for session, center in session_updates:
    messages.append(create_session_message(center, session, data))
messages = "\n\n".join(messages)
user_list = create_user_list(f'regions/{dist_id}/users')
notification_responses = send_notifications(user_list, messages)
