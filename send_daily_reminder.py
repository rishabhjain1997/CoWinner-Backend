#!/usr/bin/env python
from notification import create_user_list, send_notifications

user_list = create_user_list('users/')
message_notification = 'Hi,\n\nYour 24-hour session with our service is about to expire. Please send us *ok* to keep receiving alerts for the next 24 hours.\n\n_If you like our service, please spread the word. Tag us on FB/IG @cowinner.app_\n\nThank you. Stay safe!' 
notification_responses = send_notifications(user_list, message_notification)

