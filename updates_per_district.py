import sys
from notification import create_user_list, send_notifications
from WeekData import WeekData

# We pass dist_id as command line argument
dist_id = int(sys.argv[1])
update_messages = WeekData(dist_id).messages
if len(update_messages):
    messages = "\n\n".join(update_messages)
    user_list = create_user_list(f'regions/{dist_id}/users')
    notification_responses = send_notifications(user_list, messages)
