from firebase_admin import messaging


class SuccessMessage:
    def __init__(self, message_id=None):
        self.message_id = message_id


class FailedMessage:
    def __init__(self, message_id=None, exception=None):
        self.message_id = message_id
        self.exception = exception


class FireBaseActions:

    @staticmethod
    def send_message(user_tokens, data):
        try:
            if not user_tokens:
                return None
            message = messaging.MulticastMessage(
                tokens=user_tokens,
                data=data
            )
            fcm_response = {}
            response = messaging.send_multicast(message)
            if response:
                fcm_response["success_count"] = response.success_count
                fcm_response["failure_count"] = response.failure_count
            return fcm_response
        except Exception as e:
            print(e.__str__())
            return None
