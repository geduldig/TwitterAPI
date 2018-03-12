from TwitterAPI import TwitterAPI
import json

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)

user_id = 334398732
message_text = 'DM message 01'

event = {
	"event": {
		"type": "message_create",
		"message_create": {
			"target": {
				"recipient_id": user_id
			},
			"message_data": {
				"text": message_text
			}
		}
	}
}


r = api.request('direct_messages/events/new', json.dumps(event))

print(r.status_code)