import logging
from django.conf import settings
import africastalking

logger = logging.getLogger(__name__)


class SMSService:
    def __init__(self) -> None:
        africastalking.initialize(username=settings.AFRICASTALKING_USERNAME,
                                  api_key=settings.AFRICASTALKING_API_KEY)
        self.sms = africastalking.SMS

    def send_sms(self, phone_number, message):
        try:
            if not phone_number:
                raise ValueError('Phone number is required')
            if not message:
                raise ValueError('Message is required')
            if not phone_number.startswith('+'):
                phone_number = f'+254{phone_number.lstrip('0')}'

            response = self.sms.send(message, [phone_number])

            if response['SMSMessageData']['Recipients']:
                recipient = response['SMSMessageData']['Recipients'][0]
                if recipient['status'] == 'Success':
                    logger.info(f'SMS sent to {phone_number} successfully')
                    return True
                else:
                    logger.error(f'Error sending SMS to {phone_number}: '
                                 f'{recipient["status"]}')
                    return False
            else:
                logger.error(f'Error sending SMS to {phone_number}: '
                             f'{response}')
                return False
        except Exception as e:
            logger.error(f'Error sending SMS: {e}')
            raise e
