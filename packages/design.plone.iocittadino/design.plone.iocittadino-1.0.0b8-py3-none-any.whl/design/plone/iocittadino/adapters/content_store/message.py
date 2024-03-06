# -*- coding: utf-8 -*-
import binascii
from datetime import datetime
from urllib.request import urlopen

from Acquisition import aq_inner
from plone import api
from plone.memoize import view
from zExceptions import NotFound
from zExceptions import Unauthorized
from zope.component import adapter
from zope.component import getAllUtilitiesRegisteredFor
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implementer

from design.plone.iocittadino import _
from design.plone.iocittadino.adapters.content_store import DesignBaseContentStore
from design.plone.iocittadino.adapters.content_store.types import CONTENT_TYPE_MESSAGE
from design.plone.iocittadino.interfaces.store import IMessageContentStore
from design.plone.iocittadino.interfaces.store import IPraticaContentStore
from design.plone.iocittadino.interfaces.store import IMessageStoreFieldsExtender

# 256 mb. Converted to bytes for optimization
MESSAGE_ATTACHMENTS_FILESIZE_MAX = 256 * 1024 * 1024


# 256 mb. Converted to bytes for optimization
MESSAGE_ATTACHMENTS_FILESIZE_MAX = 256 * 1024 * 1024


@implementer(IMessageContentStore)
@adapter(Interface, Interface)
class MessageContentStore(DesignBaseContentStore):
    manage_permission = "design.plone.iocittadino: Manage Message"
    content_type = CONTENT_TYPE_MESSAGE
    allowed_states = ["pending", "sent"]
    initial_state = "pending"
    user_allowed_states = ["seen", "sent"]
    user_allowed_transitions = ["seen"]

    @property
    def fields(self):
        base_fields = {
            "date": {
                "required": False,
                "indexable": True,
            },
            "title": {
                "required": False,
                "indexable": True,
            },
            "pratica_id": {
                "required": False,
                "indexable": True,
            },
            "message": {"required": True, "indexable": False},
            "notify_on_email": {"required": False, "indexable": False},
            "object_uid": {
                "required": False,
                "indexable": True,
            },
            "email": {
                "required": False,
                "indexable": True,
            },
            "attachments": {"required": False, "indexable": False},
            **super().fields,
        }

        for utility in getAllUtilitiesRegisteredFor(IMessageStoreFieldsExtender):
            base_fields.update(utility.fields)

        return base_fields

    @property
    @view.memoize
    def states(self):
        return {
            "pending": {
                "title": translate(
                    _("pending", default="Pending"), context=self.request
                ),
                "available_states": ["sent"],
            },
            "sent": {
                "title": translate(_("sent", default="Sent"), context=self.request),
                "available_states": ["seen"],
            },
            "seen": {
                "title": translate(_("seen", default="Seen"), context=self.request),
                "available_states": [],
            },
        }

    def add(self, data):
        """
        Create a message instance

        # TODO: avere definito le add con come parametro un dizionario
        #       e non con dei nomi di parametro rende meno documentabile
        # e robusta l'implementazione

        # TODO: questa documentazione è da rivedere
        @param pratica_id: the id of pratica
        @param userid: the id of user
        @return creation status (ok / no ok)
        """

        self._validate_add(**data)

        # set state
        if not data.get("state", ""):
            data["state"] = self.get_initial_state()

        if data.get("pratica_id"):
            # set the passed pratica user to record
            pratica_store = queryMultiAdapter(
                (api.portal.get(), self.request), IPraticaContentStore
            )
            pratica = pratica_store.get(data["pratica_id"])
            # modello_pratica = api.content.get(
            #     UID=pratica.attrs.get("form_id", None)
            # )
            # TODO: sarebbe stato megli avere i recipienti in un campo a parte, anzichè
            # calcolarli
            userid = pratica.attrs["userid"]
            data["email"] = pratica.attrs["email"]
            data["userid"] = userid

        elif data.get("object_uid"):
            # XXX: nelle prenotazioni la prenotazione crerata non risulta al momento
            # tra i contenuti del sito accessibili dall'utente, quindi non è possibile
            # recuperarla con i permessi dell'utente.
            # TODO: valutare come gestire meglio questa casistica
            with api.env.adopt_roles(["Manager"]):
                obj = api.content.get(UID=data["object_uid"])
            # TODO: sarebbe stato megli avere i recipients in un campo a parte, anzichè
            # calcolarli

            # questo è sbagliato perchè la prenotazione potrebbe essere stata creata
            # da un operatore
            # userid = obj.Creator()

            # TODO: il fatto che lo userid e il ficalcode si sovrappongono e vengano usati
            # con stessa semenatica ma nomi di attributo differenti è un problema
            # TODO: i codicifiscali che arrivano da iocittadino/spid sono tutti
            # nella forma internazionale "tinit-..." e tutti in minuscolo
            # valutare se è il caso di fare un controllo e una conversione
            if hasattr(aq_inner(obj), "fiscalcode"):
                user = api.user.get(userid=obj.fiscalcode.lower())
                if user:
                    data["email"] = user.getProperty("email")
                    data["userid"] = user.getId()

            # if not data.get("title", None):
            #     data["title"] = obj.Title()

        # anche se in validazione è richiesto pratica_id o object_uid, consideriamo
        # l'evenienza futura di gestire messaggi non legati a pratica o oggetto ?
        # else:
        #     user = api.user.get_current()
        #     userid = user.getId()
        #     data["email"] = user.getProperty("email")
        #     data["userid"] = userid

        # set creation date
        data["date"] = datetime.utcnow()

        # set notification flag
        data["notify_on_email"] = data.get("notify_on_email", True)

        # manage attachments
        # data["attachments"] = self._prepare_attachments(
        #     data.get("attachments", [])
        # )

        return super().add(**data)

    def update(self, item_id, data):
        raise Unauthorized(
            translate(
                _(
                    "not_allowed_action",
                    default='The action "${action}" is not allowed for this storage',
                    mapping={"action": "update"},
                ),
                context=self.request,
            )
        )

    def delete(self, item_id):
        if not api.user.has_permission(self.manage_permission, obj=api.portal.get()):
            raise Unauthorized(
                translate(
                    _(
                        "unauthorided_delete",
                        default="You can't delete this record.",
                    ),
                    context=self.request,
                )
            )
        return super().delete(item_id)

    def update_state(self, state, *args, **kwargs):
        # if (
        #     not api.user.has_permission(
        #         self.manage_permission, obj=Modello pratica here
        #     )
        #     and state not in self.user_allowed_transitions
        # ):
        #     raise Unauthorized(
        #         translate(
        #             _(
        #                 "unauthorided_update",
        #                 default="You can't update this record.",
        #             ),
        #             context=self.request,
        #         )
        #     )

        return super().update_state(state=state, *args, **kwargs)

    # validators
    def _validate_add(self, **kwargs):
        """Basicaly validates if we have enough data to create the message with sufficient correlations"""
        super()._validate_add(**kwargs)
        self._validate_attachments(kwargs.get("attachments", []))

        pratica_id = kwargs.get("pratica_id", "")
        if pratica_id:
            pratica_storage = queryMultiAdapter(
                (api.portal.get(), self.request), IPraticaContentStore
            )
            try:
                pratica = pratica_storage.get(item_id=pratica_id)
                uid = pratica.attrs.get("form_id", "")
                context = uid and api.content.get(UID=uid)

                if not context:
                    context = api.portal.get()

                if not api.user.has_permission(self.manage_permission, obj=context):
                    raise Unauthorized(
                        translate(
                            _(
                                "message_add_uanuthorized",
                                default="The message can be only created by operator",
                            ),
                            context=self.request,
                        )
                    )
            except NotFound:
                raise ValueError(
                    translate(
                        _(
                            "wrong_pratica_id",
                            default='Wrong pratica_id "${pratica_id}". Item not found.',
                            mapping={"pratica_id": pratica_id},
                        ),
                        context=self.request,
                    )
                )
            return

        object_uid = kwargs.get("object_uid", "")
        if object_uid:
            # XXX: nelle prenotazioni la prenotazione crerata non risulta al momento
            # tra i contenuti del sito accessibili dall'utente, quindi non è possibile
            # recuperarla con i permessi dell'utente.
            # TODO: valutare come gestire meglio questa casistica
            with api.env.adopt_roles(["Manager"]):
                obj = api.content.get(UID=object_uid)
            # alternativa
            # try:
            #     obj = api.content.get(UID=object_uid)
            # except Unauthorized:
            #     return
            if not obj:
                raise ValueError(
                    translate(
                        _(
                            "object_uid",
                            default='Wrong object_uid "${object_uid}". Item not found.',
                            mapping={"object_uid": object_uid},
                        ),
                        context=self.request,
                    )
                )
            return

        raise ValueError(
            translate(
                _(
                    "not_relations_provided",
                    default="Must be provided `pratica_id` or `object_uid` parameter",
                ),
                context=self.request,
            )
        )

    def _validate_attachments(self, attachments: dict) -> None:
        for attachment in attachments:
            # data is a url with base64 encoded string
            # data:application/pdf;base64,JV....
            if not attachment["data"].startswith("data:"):
                raise ValueError(
                    translate(
                        _(
                            "bad_message_attachment_encoding",
                            default="Bad message attachment encoding: ${filename}",
                            mapping={"filename": attachment["name"]},
                        ),
                        context=self.request,
                    )
                )
            try:
                filesize = len(urlopen(attachment["data"]).getvalue())
            except binascii.Error:
                raise ValueError(
                    translate(
                        _(
                            "bad_message_attachment_encoding",
                            default="Bad message attachment encoding: ${filename}",
                            mapping={"filename": attachment["name"]},
                        ),
                        context=self.request,
                    )
                )

            if filesize > MESSAGE_ATTACHMENTS_FILESIZE_MAX:
                raise ValueError(
                    translate(
                        _(
                            "bad_message_attachment_filesize",
                            default="File size exceeds limits: ${filename}",
                            mapping={"filename": attachment["name"]},
                        ),
                        context=self.request,
                    )
                )

    def _user_can_access(self, record):
        userid = self.get_current_userid()

        pratica_id = record.attrs.get("pratica_id", "")
        if pratica_id:
            if record.attrs.get("userid", "") == userid:
                return True
            pratica = queryMultiAdapter(
                (api.portal.get(), self.request), IPraticaContentStore
            ).get(pratica_id)

            return pratica and True

        object_uid = record.attrs.get("object_uid", "")
        if object_uid:
            if record.attrs.get("userid", "") == userid:
                return True
            obj = api.portal.get().restrictedTraverse(
                "/".join(api.content.get(UID=object_uid).getPhysicalPath())
            )
            return obj and True

    # def _prepare_attachments(self, attachments=[]):
    #     # This should be a clean method but we want to save the memory
    #     used_indexes = []

    #     def generate_fileindex():
    #         # ʕ·͡ᴥ·ʔ
    #         # May seem to be useless but when you also will see two equal uuids
    #         # you will write these controls like me
    #         import uuid

    #         index = uuid.uuid4().hex
    #         while index in used_indexes:
    #             index = uuid.uuid4().hex
    #         used_indexes.append(index)

    #         return index

    #     # NOTE: We dont have the update method for this storage
    #     # so do not care about it
    #     # TODO: In the future leave only the uuid or filepath in attachment
    #     # and move file to the blobstorage
    #     for attachment in attachments:
    #         attachment["fileindex"] = generate_fileindex()

    #     return attachments
