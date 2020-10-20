from TwitterAPI import TwitterAPI
import json

api = TwitterAPI(<consumer key>, 
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)

user_id = <user id of the recipient>
message_text = <the DM text>

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
print('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)