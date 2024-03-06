# -*- coding: utf-8 -*-
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from plone import api
from plone.namedfile.utils import get_contenttype
from plone.namedfile.utils import stream_data
from zope.globalrequest import getRequest

from design.plone.iocittadino import _
from design.plone.iocittadino import logger
from design.plone.iocittadino.adapters.content_store.types import CONTENT_TYPE_MESSAGE
from design.plone.iocittadino.browser.mail import MESSAGE_CREATED_EMAIL


def notify_about_message_creation(message, event):
    if message.type != CONTENT_TYPE_MESSAGE:
        return

    # notify only if the `message.notify_on_email field` is True
    if not message.attrs.get("notify_on_email", False):
        return

    request = getRequest()
    error_msg = "Could not send notification email due to: {message}"
    mfrom = api.portal.get_registry_record("plone.email_from_address")
    if not mfrom:
        logger.error(error_msg.format(message="Email from address is not configured"))
        return None

    recipient = message.attrs.get("email", "")

    if not recipient:
        logger.error(error_msg.format(message="User email address is not configured"))
        return None

    host = api.portal.get_tool("MailHost")

    view = api.content.get_view(
        request=request,
        context=api.portal.get(),
        name="mail_view",
    )
    content = view(
        message_text=message.attrs.get("message", ""),
        mail_type=MESSAGE_CREATED_EMAIL,
    )

    msg = MIMEMultipart()
    msg.attach(MIMEText(content, "html"))
    msg["Subject"] = _("Nuovo messaggio")
    msg["From"] = mfrom
    msg["To"] = recipient

    for attachment in message.attrs.get("attachments", []):
        mail_attachment_filename = attachment.get("name", "")
        mail_attachment = MIMEApplication(
            stream_data(attachment.get("blob", None)),
            Name=mail_attachment_filename,
        )

        mail_attachment["Content-Type"] = get_contenttype(attachment.get("blob", None))
        mail_attachment["Content-Disposition"] = (
            'attachment; filename="%s"' % mail_attachment_filename
        )

        msg.attach(mail_attachment)

    try:
        host.send(msg, charset="utf-8")
    except Exception as e:
        logger.error(error_msg.format(email_message=str(e)))
