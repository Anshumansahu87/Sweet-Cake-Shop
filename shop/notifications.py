from django.conf import settings
from .models import Notification

try:
    from twilio.rest import Client
except ImportError:
    Client = None


def send_customer_notification(
    *,
    user,
    phone,
    message,
    order=None,
    channel="SMS"
):
    """
    Sends a real SMS/WhatsApp message when Twilio credentials
    are configured.

    Order confirmation SMS:
    Sweet Cake Shop: Your order has been successfully placed.
    Thank you for ordering!
    """

    # -----------------------------------------
    # ORDER SUCCESS MESSAGE
    # -----------------------------------------
    if (
        channel == "SMS"
        and message
        and "confirmed" in message.lower()
    ):
        message = (
            "Sweet Cake Shop: Your order has been successfully "
            "placed. Thank you for ordering!"
        )

    status = "DEMO"
    provider_id = ""

    # -----------------------------------------
    # TWILIO SETTINGS
    # -----------------------------------------
    sid = getattr(settings, "TWILIO_ACCOUNT_SID", "")
    token = getattr(settings, "TWILIO_AUTH_TOKEN", "")
    from_number = getattr(settings, "TWILIO_FROM_NUMBER", "")
    whatsapp_from = getattr(settings, "TWILIO_WHATSAPP_FROM", "")

    # -----------------------------------------
    # SEND REAL SMS / WHATSAPP
    # -----------------------------------------
    if Client and sid and token:
        try:
            client = Client(sid, token)

            if channel == "WHATSAPP":

                if not whatsapp_from:
                    raise ValueError(
                        "TWILIO_WHATSAPP_FROM is not configured."
                    )

                to = (
                    phone
                    if phone.startswith("whatsapp:")
                    else f"whatsapp:{phone}"
                )

                from_ = (
                    whatsapp_from
                    if whatsapp_from.startswith("whatsapp:")
                    else f"whatsapp:{whatsapp_from}"
                )

            else:

                if not from_number:
                    raise ValueError(
                        "TWILIO_FROM_NUMBER is not configured."
                    )

                # Twilio SMS numbers must use E.164 format.
                to = phone.strip()
                if not to.startswith("+"):
                    digits = "".join(ch for ch in to if ch.isdigit())
                    if len(digits) == 10:
                        to = "+91" + digits
                    else:
                        to = "+" + digits

                # Twilio ka SMS-capable number
                from_ = from_number

            # REAL SMS SEND
            msg = client.messages.create(
                body=message,
                from_=from_,
                to=to
            )

            provider_id = msg.sid
            status = "SENT"

        except Exception as exc:

            status = "FAILED"
            provider_id = str(exc)[:120]

    # -----------------------------------------
    # SAVE NOTIFICATION IN DATABASE
    # -----------------------------------------
    return Notification.objects.create(
        user=user,
        order=order,
        channel=channel,
        phone=phone,
        message=message,
        status=status,
        provider_id=provider_id,
    )