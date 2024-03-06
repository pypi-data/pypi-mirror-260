# -*- coding: utf-8 -*-
import markdown
from Acquisition import aq_inner
from plone import api
from plone.stringinterp.interfaces import IStringInterpolator
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest

from design.plone.iocittadino import logger
from design.plone.iocittadino.interfaces.store import IMessageContentStore

# @implementer(IExecutable)
# @adapter(IPrenotazioniFolder, IMailFromFieldAction, Interface)
# class MessageActionExecutor(MailActionExecutor):
#     def __call__(self):


def MailActionExecutor_call(self):
    """Send message to the user with the booking information

    TODO: at the moment is a monkey patch of the collective.contentrules.mailfromfield's
          MailActionExecutor. Need to be refactored in a better way, peraphs using a
          new conent rule.
    """
    obj = self.event.object
    # TODO: dove è definito il sender del messaggio? ora viene "calcolato"
    # in base al pratica_id o object_uid passato, ma sarebbe stato
    # più semplice e lineare se fosse stato nella add
    if hasattr(aq_inner(obj), "fiscalcode"):
        # TODO: i codicifiscali che arrivano da iocittadino/spid sono tutti
        # nella forma internazionale "tinit-..." e tutti in minuscolo
        # valutare se è il caso di fare un controllo e una conversione
        user = api.user.get(userid=obj.fiscalcode.lower())
        if user:
            interpolator = IStringInterpolator(obj)
            subject = self.element.subject
            message = self.element.message
            subject = self.expand_markers(subject)
            message = self.expand_markers(message)
            subject = interpolator(subject).strip()
            message = interpolator(message).strip()
            if getattr(self.element, "is_markdown", False):
                message = markdown.markdown(message)
            message_store = getMultiAdapter(
                (api.portal.get(), getRequest()), IMessageContentStore
            )
            # TODO: modificare add da un metodo che accetta un dict a uno che accetta
            #       singoli parametri, ed eventualmente un kwargs
            message_store.add(
                {
                    "object_uid": obj.UID(),
                    "title": subject,  # "Prenotazione appuntamento: " + obj.booking_type,
                    "message": message,
                    "state": "sent",
                    "notify_on_email": False,  # ???
                }
            )
        else:
            logger.warning(
                "skip message creation: user not found for %s",
                obj.absolute_url(),
            )
    # Original: send email
    self._old___call__()
    # return super().__call__()
