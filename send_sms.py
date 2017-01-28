import urllib
import urllib2


def send_sms(message, numbers="918589957768"):
	username = "steva_fernandes@yahoo.com"
	hash_code = '10e9151d6a1f5dd0acf4340ddd518e62d7cb7fa1'
	sender = 'TXTLCL'
	numbers = numbers
	message = message
	post_param_dict = {
		'username': username,
		'hash': hash_code,
		'message': message,
		'sender': sender,
		'numbers': numbers
	}
	send_sms_url = "http://api.textlocal.in/send/?"
	post_data = urllib.urlencode(post_param_dict)
	request = urllib2.Request(send_sms_url, post_data)
	try:
		response = urllib2.urlopen(request)
		if response.geturl() == send_sms_url:
			print "SMS Sent. Message: {message}".format(message=message)
	except urllib2.URLError as urlerror:
		print "Send failed. Reason: {reason}".format(reason=urlerror.reason)
		
