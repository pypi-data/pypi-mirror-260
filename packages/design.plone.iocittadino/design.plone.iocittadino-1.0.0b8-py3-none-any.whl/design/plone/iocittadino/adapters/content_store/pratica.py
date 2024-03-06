# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime
from logging import getLogger

from plone import api
from plone.memoize import view
from zope.component import adapter
from zope.component import getAllUtilitiesRegisteredFor
from zope.component import queryMultiAdapter
from zope.event import notify
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implementer

from design.plone.iocittadino import _
from design.plone.iocittadino.adapters.content_store import DesignBaseContentStore
from design.plone.iocittadino.adapters.content_store.types import CONTENT_TYPE_PRATICA
from design.plone.iocittadino.events.content_store.events.events import (
    PraticaAssignedEvent,
)
from design.plone.iocittadino.events.content_store.events.events import (
    PraticaCreatedEvent,
)
from design.plone.iocittadino.events.content_store.events.events import (
    StoreRecordCreatedEvent,
)
from design.plone.iocittadino.interfaces import IPraticaContentStore
from design.plone.iocittadino.interfaces import IPraticaPdfGenerator
from design.plone.iocittadino.interfaces import IPraticaStoreFieldsExtender

# from design.plone.iocittadino.interfaces import IBlobStorage


logger = getLogger(__name__)


@implementer(IPraticaContentStore)
@adapter(Interface, Interface)
class PraticaContentStore(DesignBaseContentStore):
    """ """

    content_type = CONTENT_TYPE_PRATICA
    manage_permission = "design.plone.iocittadino: Manage Pratica"
    initial_state = "ongoing"
    allowed_states = ["draft", "ongoing"]
    allowed_delete_states = ["draft"]

    # Pratica Workflow management
    @property
    @view.memoize
    def states(self):
        return {
            "draft": {
                "title": translate(
                    _("wf_label_draft", default="Draft"), context=self.request
                ),
                "available_states": ["ongoing", "canceled"],
            },
            "ongoing": {
                "title": translate(
                    _("wf_label_ongoing", default="Ongoing process"),
                    context=self.request,
                ),
                "available_states": [
                    "suspended",
                    "completed",
                    "canceled",
                    "draft",
                ],
            },
            "suspended": {
                "title": translate(
                    _("wf_label_suspended", default="Suspended process"),
                    context=self.request,
                ),
                "available_states": [
                    "ongoing",
                    "completed",
                    "canceled",
                    "draft",
                ],
            },
            "completed": {
                "title": translate(
                    _("wf_label_completed", default="Completed process"),
                    context=self.request,
                ),
                "available_states": [],
            },
            "canceled": {
                "title": translate(
                    _("wf_label_canceled", default="Canceled"),
                    context=self.request,
                ),
                "available_states": ["draft"],
            },
        }

    # END OF Pratica Workflow management

    @property
    def fields(self):
        base_fields = {
            **(super().fields),
            "form_id": {"required": True},
            "data": {
                "required": False,  # requirement depends on state, so is checked manually
            },
            "email": {"required": False},
            "state": {"required": False},
            "numero_protocollo": {"required": False},
            # "creation_date"
            "date": {
                "required": False,  # it's added manually, so it's not required
            },
            "modification_date": {
                "required": False,  # it's added manually, so it's not required
            },
            "ongoing_date": {
                "required": False,  # it's added manually, so it's not required
            },
            "servizio": {
                "required": False,  # it's added manually, so it's not required
            },
            "ufficio": {
                "required": False,  # it's added manually, so it's not required
            },
            "assigned_to": {
                "required": False,
            },
            "next_steps": {"required": False},
            "pratica_report": {"required": False},
        }

        for utility in getAllUtilitiesRegisteredFor(IPraticaStoreFieldsExtender):
            base_fields.update(utility.fields)

        return base_fields

    # END OF SCHEMA MANAGEMENT

    # UTILS METHODS
    @view.memoize
    def get_modello_pratica(self, uid):
        return api.content.get(UID=uid)

    def _validate_add(self, **kwargs):
        """Validate the add operation.

        :param kwargs: the fields to add
        :raises ValueError: if the data is not valid
        :raises ValueError: if the email is not valid
        :raises ValueError: if the form_id is not valid
        :raises ValueError: if the assigned_to is not valid
        :raises ValueError: if the next_steps is not valid
        :raises ValueError: if the pratica_report is not valid
        """
        super()._validate_add(**kwargs)

        userid = self.get_current_userid()
        state = kwargs.get("state")
        data = kwargs.get("data")

        if state != "draft" and not data:
            raise ValueError(
                translate(
                    _("missing_field_error", default="Missing form data."),
                    context=self.request,
                )
            )

        form_id = kwargs.get("form_id")
        item = form_id and api.content.get(UID=form_id)
        if not item:
            raise ValueError(
                translate(
                    _(
                        "wrong_form_id",
                        default='Wrong form_id "${form_id}". Item not found.',
                        mapping={"form_id": form_id},
                    ),
                    context=self.request,
                )
            )

        # check for duplicated entries
        pratiche = self.search(
            query={
                "form_id": form_id,
                "state": self.allowed_states,
                "userid": userid,
            }
        )
        if pratiche:
            raise ValueError(
                translate(
                    _(
                        "duplicate_pratica",
                        default="Unable to submit a new Record. There is already a Record in progress for this Service.",
                    ),
                    context=self.request,
                )
            )

    def _validate_update(self, **kwargs):
        """Validate the update operation.

        :param kwargs: the fields to update
        :raises Unauthorized: if the user is not logged in
        :raises ValueError: if the state is not allowed
        :raises ValueError: if the data is not valid
        :raises ValueError: if the assigned_to is not valid
        """

        super()._validate_update(**kwargs)

        state = kwargs.get("state", "")

        # TODO: Move the state change logic completely to transitions
        if state and state not in self.allowed_states:
            raise ValueError(
                translate(
                    _(
                        "wrong_state_update",
                        default='Unable to change record state in "${state}".',
                        mapping={"state": state},
                    ),
                    context=self.request,
                )
            )

        fields = ["data", "assigned_to"]
        has_required_field = False

        for required in fields:
            if kwargs.get(required, None):
                has_required_field = True

        if not has_required_field:
            raise ValueError(
                translate(
                    _(
                        "missing_required_field_update",
                        default="Missing required field: data or assigned_to.",
                    ),
                    context=self.request,
                )
            )

    def _set_ongoing_date_now(self, item_id):
        self.store.update(item_id, {"ongoing_date": datetime.utcnow()})

    def _user_can_access(self, record):
        """Check if the current user can access the record.

        :param record: a store record
        :return: True if the user can access the record, False otherwise

        The user can access the record if:
        - the record is assigned to him
        - has the permission to manage the `pratica` related to the record (operatore)
        """
        userid = self.get_current_userid()
        if record.attrs.get("userid", "") == userid:
            return True
        uid = record.attrs.get("form_id", "")
        context = uid and api.content.get(UID=uid)
        if not context:
            context = api.portal.get()
        return api.user.has_permission(self.manage_permission, obj=context)

    def get_next_steps(self, modello_uid):
        modello = self.get_modello_pratica(uid=modello_uid)
        next_steps = []

        if modello and modello.next_steps:
            for item in modello.next_steps:
                days_number = item.get("days_number", "")
                title = item.get("title", "")
                next_steps.append({"days_number": days_number, "title": title})

        return next_steps

    # END OF UTILS METHODS

    def add(self, data):
        """Create a 'pratica' record

        After the record is created, the event 'PraticaCreatedEvent' is fired, and
        the event 'PraticaAssignedEvent' is fired if 'assigned_to' has a value.

        :param data: the fields to add
        :returns: the created record
        :rtype: Record
        :raises Exception: if the record cannot be created

        # TODO ? :raises Unauthorized: if the user is not logged in
        """

        # TODO: non c'è alcun controllo di permessi sulla form_id,
        #       non dovrebbe essere in self.context la form ?
        # NOTE: we should have an Unauthorized if call get_modello_pratica method
        #       without a proper permission
        self._validate_add(**data)

        form_id = data["form_id"]

        if not data.get("state", ""):
            data["state"] = self.get_initial_state()

        if data.get("state") == "ongoing":
            data["ongoing_date"] = datetime.utcnow()

        data["userid"] = self.get_current_userid()
        data["email"] = self.get_current_user_email()

        # salva servizio e uffici (TODO: è corretto inserire nel record servizio e uffici,
        # se servono, perchè potrebbero non essere più presenti nel tempo, ma salvare come informazione
        # gli UID non aiuta a storicizzare il dato)
        modello_pratica = self.get_modello_pratica(uid=form_id)
        servizio = modello_pratica.aq_parent
        data["servizio"] = servizio.UID()
        data["ufficio"] = [
            x.to_object.UID() for x in servizio.ufficio_responsabile if x.to_object
        ]

        # set creation date and next steps
        data["date"] = data["modification_date"] = datetime.utcnow()
        data["next_steps"] = self.get_next_steps(form_id)

        # XXX: questo va spiegato: la funzione oltre a tornare i fileid temporanei
        # scrive nel dizionario data i riferimenti ai blob per il successivo salvataggio
        # nel record (quello che viene fatto con super().add nella riga successiva)
        blob_ids = self.move_blobs_to_pratica(modello_pratica, data)
        record = super().add(**data)

        self.delete_saved_blobs_from_temp_storage(blob_ids)

        if data["state"] == "ongoing":
            self.update_pratica_with_report(record)

        if record.attrs.get("assigned_to", ""):
            notify(PraticaAssignedEvent(record))

        notify(PraticaCreatedEvent(record))

        return record

    def update(self, item_id, data):
        self._validate_update(**data)

        record = self.get(item_id)

        form_state = data.get("state")
        record_state = record.attrs.get("state")
        assigned_to_request = data.get("assigned_to")
        assigned_to_pratica = record.attrs.get("assigned_to")

        if data.get("data") and record_state != "draft":
            raise ValueError(
                translate(
                    _(
                        "unable_to_edit_pratica",
                        default="Unable to edit a Pratica not in draft state.",
                    ),
                    context=self.request,
                )
            )
        if assigned_to_request and record_state not in self.allowed_states:
            raise ValueError(
                translate(
                    _(
                        "unable_to_assign_pratica",
                        default="Unable to assign a Pratica to an user when is in a final state.",
                    ),
                    context=self.request,
                )
            )

        data["modification_date"] = datetime.utcnow()

        # XXX: questo va spiegato: la funzione oltre a tornare i fileid temporanei
        # scrive nel dizionario data i riferimenti ai blob per il successivo salvataggio
        # nel record (quello che viene fatto con super().update nella riga successiva)
        blob_ids = self.move_blobs_to_pratica(
            model_form=self.get_modello_pratica(record.attrs.get("form_id", "")),
            data=data,
            record=record,
        )
        result = super().update(item_id, data)

        self.delete_saved_blobs_from_temp_storage(blob_ids)

        if form_state == "ongoing":
            self.update_pratica_with_report(record)

        updated_record = self.store.get(item_id)

        # if error is not None:
        #     # c'è stato un errore
        #     return error

        if form_state == self.initial_state:
            # notify the user because this is the confirm of the record
            notify(StoreRecordCreatedEvent(updated_record))

        if assigned_to_request and assigned_to_pratica != assigned_to_request:
            notify(PraticaAssignedEvent(updated_record))

        return result

    def update_state(self, item_id, state):
        # TODO: Don't know if the code below could be named atomic
        if state == "ongoing":
            self._set_ongoing_date_now(item_id)
            self.update_pratica_with_report(self.get(item_id))

        record = super().update_state(item_id=item_id, state=state)
        # We need to keep the ongoing date
        return record

    def delete(self, item_id):
        if not item_id:
            raise ValueError(
                translate(
                    _("missing_item_id", default="Missing record ID."),
                    context=self.request,
                )
            )
        record = self.get(item_id=item_id)

        if record.attrs.get("state", "") not in self.allowed_delete_states:
            raise ValueError(
                translate(
                    _(
                        "unable_to_delete_error",
                        default="You can't delete a record in this state: ${state}",
                        mapping={"state": record.attrs.get("state", "")},
                    ),
                    context=self.request,
                )
            )

        self.store.delete(record.intid)

    def update_pratica_with_report(self, pratica):
        # TODO: move logic to events
        # NOTE: placed here and not in the event so as we cant use normaly this storage
        #       update method so as it controls the required fields(he doesnt have to do this)
        modello_pratica = api.content.get(UID=pratica.attrs.get("form_id"))
        pdf_generator = queryMultiAdapter(
            (modello_pratica, self.request), IPraticaPdfGenerator
        )
        if not pdf_generator:
            return

        self.store.update(
            item_id=pratica.intid,
            validated_data={
                "pratica_report": {
                    "name": f"{self.get_modello_pratica(pratica.attrs.get('form_id')).getId()}.pdf",
                    "data": "data:application/pdf;base64,"
                    + pdf_generator.get_pdf_as_b64(pratica).decode(),
                }
            },
        )

    def move_blobs_to_pratica(self, model_form, data, record=None):
        """Method moves blobs from temporary storage to pratica record

        Returns:
            list: List of the file id's which have been moved to pratica form data
        """
        # TODO: rewrite the try/except block, this was used to bypass the bad written tests
        try:
            pratica_model = json.loads(model_form.pratica_model)
        except json.decoder.JSONDecodeError:
            pratica_model = {}

        file_fields = set()
        files_managed = []

        for page in pratica_model.get("pages", []):
            for element in page.get("elements", []):
                if element["type"] == "file":
                    file_fields.add(element.get("valueName", element.get("name")))
                for element in element.get("elements", []):
                    if element["type"] == "file":
                        file_fields.add(element.get("valueName", element.get("name")))

        form_data = data.get("data", {})
        for field in file_fields:
            if field in form_data:
                value = form_data[field]
                # XXX: get previous value, because 'update' method doesn't update data,
                #      but overwrite it
                if record:
                    record_data = record.attrs.get("data", {}).get(field)
                    if record_data:
                        form_data[field] = record_data.get("blob")

                if value is None:
                    # del form_data[field]
                    continue
                # TODO: value è una lista o un valore secco ?
                #       - If the field was updated/inserted it will be
                #         managed by surveyjs(new file) an we will recieve a list with one value.
                #         if the field was not updated, we will have serialized
                #         storage blob dict structure
                if isinstance(value, list):
                    if len(value) > 1:
                        raise NotImplementedError("Multiple files not supported yet")
                    value = value[0]
                # Get file id from link, expected to be broken if can't find the id
                # TODO: mettere l'id in un field evitando la regexp
                #       - Additional field will requeire the surveyjs core code customizations
                try:
                    file_id = re.search(r"@@download/([a-zA-Z0-9]+)", value["content"])[
                        1
                    ]
                except:  # noqa
                    logger.exception("Unable to find file id in link %s", value)
                    # del form_data[field]
                    continue
                # Bind the plone.namedfile.NamedBlobFile instance to pratica data
                # form_data[key] = self.blob_storage.get(file_id)
                blob = self.store.get_tempfile(file_id)
                if blob:
                    form_data[field] = {
                        "name": blob.filename,
                        "type": blob.contentType,
                        "blob": blob,
                        "size": blob.getSize(),
                    }
                    files_managed.append(file_id)
                else:
                    # il file non è nella temp storage, probabilmente è già stato caricato
                    # del form_data[field]
                    pass
        return files_managed

    def delete_saved_blobs_from_temp_storage(self, id_list):
        """Delete blobs from temporary storage"""
        for id in id_list:
            # del self.blob_storage[id]
            self.store.del_tempfile(id)
