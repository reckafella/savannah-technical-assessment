from celery import shared_task
from app.models.orders.models import Order
from app.tasks.sms_service import SMSService
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_order_notification(order_id):
    try:
        order = Order.objects.get(id=order_id)
        sms_service = SMSService()
        message = (f'Hello {order.customer.name}! Your order for '
                   f'{order.item} for has been received successfully.'
                   f'Order ID: {order.id}')

        result = sms_service.send_sms(phone_number=order.customer.phone_number,
                                      message=message)
        logger.info(f'SMS Notification sent for order {order.id}: {result}')
        return result
    except Order.DoesNotExist:
        logger.error(f'Order with id {order_id} does not exist')
        return False
    except Exception as e:
        logger.error(f'Failed to send SMS for order {order_id}: {str(e)}')
        return False
