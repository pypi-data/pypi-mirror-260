# -*- coding: utf-8 -*-
from base64 import b64decode
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from plone import api
from plone.namedfile.utils import stream_data
from plone.registry.interfaces import IRegistry
from plone.stringinterp.adapters import BaseSubstitution
from plone.stringinterp.interfaces import IContextWrapper
from plone.stringinterp.interfaces import IStringInterpolator
from zope.component import adapter
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface.interface import Interface

from design.plone.iocittadino import _
from design.plone.iocittadino import logger
from design.plone.iocittadino.adapters.content_store.types import CONTENT_TYPE_PRATICA
from design.plone.iocittadino.browser.mail import PRATICA_ASSIGNED_EMAIL
from design.plone.iocittadino.browser.mail import PRATICA_SAVED_EMAIL
from design.plone.iocittadino.interfaces.store import IMessageContentStore
from design.plone.iocittadino.interfaces.store import IPraticaContentStore


@adapter(Interface)
class PraticaNewStateSubstitution(BaseSubstitution):
    def safe_call(self):
        msgid = f"wf_label_{self.wrapper.pratica_new_state}"
        return translate(
            _(msgid),
            context=getRequest(),
            domain="design.plone.iocittadino",
        )


@adapter(Interface)
class PraticaOldStateSubstitution(BaseSubstitution):
    def safe_call(self):
        msgid = f"wf_label_{self.wrapper.pratica_old_state}"
        return translate(
            _(msgid),
            context=getRequest(),
            domain="design.plone.iocittadino",
        )


@adapter(Interface)
class PraticaIdSubstitution(BaseSubstitution):
    def safe_call(self):
        return self.wrapper.pratica_id


def transition_notify(pratica, event):
    """IStoreRecordTransitionEvent"""
    if pratica.type != CONTENT_TYPE_PRATICA:
        return None

    request = getRequest()

    # ensure that we have the pratica item
    if not queryMultiAdapter((api.portal.get(), request), IPraticaContentStore).get(
        pratica.intid
    ):
        return

    message_store = queryMultiAdapter((api.portal.get(), request), IMessageContentStore)

    message_text = compose_transition_message(pratica, event)
    pratica_model = api.content.get(UID=pratica.attrs.get("form_id"))

    if not message_text:
        logger.error(message="Could not compose the message")
        return

    message = {
        "title": pratica_model.Title(),
        "pratica_id": pratica.intid,
        "message": message_text,
        "state": "sent",
    }
    # TODO: modificare add da un metodo che accetta un dict a uno che accetta
    #       singoli parametri, ed eventualmente un kwargs

    with api.env.adopt_roles(["Manager"]):
        message_store.add(message)


def compose_transition_message(pratica, event):
    modello_pratica = api.content.get(UID=pratica.attrs.get("form_id"))

    if modello_pratica:
        message = getattr(modello_pratica, "pratica_transition_message", "")

        if not message:
            logger.error("There is no message")
            return message

    interpolator_context = IContextWrapper(api.portal.get())(
        pratica_new_state=event.new_state,
        pratica_old_state=event.old_state,
        pratica_id=pratica.intid,
    )

    interpolator = IStringInterpolator(interpolator_context)

    return interpolator(message)


def pratica_assigned_notify(pratica, event):
    """
    The notification email will be sent to the assigned user
    """
    if pratica.type != CONTENT_TYPE_PRATICA:
        return None

    assigned_to = pratica.attrs.get("assigned_to", "")
    if not assigned_to:
        return
    user = api.user.get(userid=assigned_to)
    if not user:
        logger.warning(
            f'[Pratica "{pratica.intid}" assigned to "{assigned_to}"] Unable to sent notification: user not found.'
        )
        return
    email = user.getProperty("email", "")
    if not email:
        logger.warning(
            f'[Pratica "{pratica.intid}" assigned to "{assigned_to}"] Unable to sent notification: user without email.'
        )
        return

    request = getRequest()
    mail_view = api.content.get_view(
        request=request,
        context=api.portal.get(),
        name="mail_view",
    )
    message = mail_view(pratica=pratica, mail_type=PRATICA_ASSIGNED_EMAIL)
    msg = prepare_message(
        message=message,
        subject=f"Pratica assegnata: {pratica.intid}",
    )

    msg.replace_header("To", email)
    send_mail(msg=msg)


def pratica_created_notify_by_message(pratica, event):
    if pratica.type != CONTENT_TYPE_PRATICA:
        return None

    # do not notify if it pratica has a 'draft' state
    if pratica.attrs.get("state", "") == "draft":
        return None

    request = getRequest()

    # ensure that we have the pratica item
    if not queryMultiAdapter((api.portal.get(), request), IPraticaContentStore).get(
        pratica.intid
    ):
        return

    message_store = queryMultiAdapter((api.portal.get(), request), IMessageContentStore)
    pratica_model = api.content.get(UID=pratica.attrs.get("form_id"))
    pratica_user = api.user.get(userid=pratica.attrs.get("userid"))

    # Pratica modle url with no api in the url
    # TODO: remove when /api url will not be used more
    pratica_model_url = pratica_model.absolute_url().replace("/api", "")

    # TODO: spostare su pagetemplate
    message_text = (
        f"Gentile {pratica_user and pratica_user.getProperty('fullname') or ''}<br>"
        f"la sua richiesta per {pratica_model.title} è stata inviata con successo.<br>"
        f"<br><p><a href=\"{pratica_model_url + '/@@download/' + str(pratica.intid)}\">Scarica il pdf</a></p>"
    )

    message = {
        "title": pratica_model.Title(),
        "message": message_text,
        "state": "sent",
        "notify_on_email": False,
        "pratica_id": pratica.intid,
    }
    # TODO: modificare add da un metodo che accetta un dict a uno che accetta
    #       singoli parametri, ed eventualmente un kwargs

    with api.env.adopt_roles(["Manager"]):
        message_store.add(message)


def pratica_created_notify_by_email(pratica, event):
    if pratica.type != CONTENT_TYPE_PRATICA:
        return None

    # do not notify if it pratica has a 'draft' state
    if pratica.attrs.get("state", "") == "draft":
        return None

    # send emails
    error_msg = "Could not send notification email due to: {message}"
    pratica_model = api.content.get(UID=pratica.attrs.get("form_id"))
    pratica_email = pratica.attrs.get("email", "")
    mfrom = api.portal.get_registry_record("plone.email_from_address")
    recipients = [i for i in pratica_model.pratica_notification_emails or []]
    request = getRequest()
    mfrom = api.portal.get_registry_record("plone.email_from_address")
    message_text = 'Nuova pratica nella sua <a href="{area_personale_url}">area personale</a> è stata creata'.format(
        area_personale_url=api.portal.get().absolute_url().replace("/api", "")
        + "/area-personale-cittadino"
    )

    pratica_email and recipients.append(pratica_email)

    if not recipients:
        logger.error(
            error_msg.format(message="Could not find recipients for the email message")
        )
        return None

    if not mfrom:
        logger.error(error_msg.format(message="Email from address is not configured"))
        return None

    mail_view = api.content.get_view(
        request=request,
        context=api.portal.get(),
        name="mail_view",
    )
    messag_text = mail_view(message_text=message_text, mail_type=PRATICA_SAVED_EMAIL)

    # compose the message part
    msg = MIMEMultipart()
    msg.attach(MIMEText(messag_text, "html"))
    msg["Subject"] = f"Pratica inviata: {pratica.intid}"
    msg["From"] = mfrom
    msg["To"] = ""

    pratica_report = pratica.attrs.get("pratica_report", None)

    if pratica_report:
        pratica_attachment_filename = pratica_model.getId() + ".pdf"
        # handle new pratica report save techinque
        if type(pratica_report) is dict and pratica_report.get("blob"):
            pratica_report_attachment = MIMEApplication(
                stream_data(pratica_report.get("blob")),
                Name=pratica_attachment_filename,
            )
        else:
            pratica_report_attachment = MIMEApplication(
                b64decode(pratica.attrs.get("pratica_report", "")),
                Name=pratica_attachment_filename,
            )

        pratica_report_attachment["Content-Disposition"] = (
            'attachment; filename="%s"' % pratica_attachment_filename
        )

        msg.attach(pratica_report_attachment)

    for recipient in recipients:
        # send a copy also to the fields with bcc flag
        msg.replace_header("To", recipient)
        send_mail(msg=msg)


def pratica_created_notify_editor(pratica, event):
    if pratica.type != CONTENT_TYPE_PRATICA:
        return None

    # do not notify if pratica ha a 'draft' state
    if pratica.attrs.get("state", "") == "draft":
        return None

    request = getRequest()
    error_msg = "Could not send notification email due to: {message}"
    mfrom = api.portal.get_registry_record("plone.email_from_address")

    if not mfrom:
        logger.error(error_msg.format(message="Email from address is not configured"))
        return None

    modello_pratica = api.content.get(UID=pratica.attrs.get("form_id"))

    if not modello_pratica:
        logger.error(
            error_msg.format(message="Could not find related ModelloPratica obj.")
        )

    if not modello_pratica.pratica_notification_emails:
        logger.error(
            error_msg.format(message="Could not find recipients for the email message")
        )
        return None

    mail_view = api.content.get_view(
        request=request,
        context=api.portal.get(),
        name="mail_view",
    )
    # compose the message part
    message_text = f"""
        <p>E' stata inserita la nuova pratica numero {pratica.intid} </p>
        <p>Accedi all'<a href="{api.portal.get().portal_url().replace('/api', '') + "/area-personale-operatore"}">area operatore</a></p>
        """
    message = mail_view(message_text=message_text, mail_type=PRATICA_SAVED_EMAIL)

    msg = prepare_message(
        message=message,
        subject="Nuova pratica creata",
    )

    for recipient in modello_pratica.pratica_notification_emails:
        # send a copy also to the fields with bcc flag
        msg.replace_header("To", recipient)
        send_mail(msg=msg)


def prepare_message(message, subject):
    mfrom = api.portal.get_registry_record("plone.email_from_address")
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = subject
    msg["From"] = mfrom

    # ????
    msg["To"] = ""

    # ????
    msg.replace_header("Content-Type", 'text/html; charset="utf-8"')

    return msg


def send_mail(msg):
    host = api.portal.get_tool(name="MailHost")
    registry = getUtility(IRegistry)
    encoding = registry.get("plone.email_charset", "utf-8")
    # we set immediate=True because we need to catch exceptions.
    # by default (False) exceptions are handled by MailHost and we can't catch them.
    # XXX: don't use immediate=True in production, it's not transaction safe
    host.send(msg, charset=encoding)  # , immediate=True)
