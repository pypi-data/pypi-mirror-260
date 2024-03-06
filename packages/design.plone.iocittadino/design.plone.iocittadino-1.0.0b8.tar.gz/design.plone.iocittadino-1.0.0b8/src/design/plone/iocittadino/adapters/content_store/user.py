# -*- coding: utf-8 -*-
import json
from datetime import datetime

from plone import api
from zExceptions import Unauthorized
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implementer

from design.plone.iocittadino import _
from design.plone.iocittadino.adapters.content_store.types import CONTENT_TYPE_USER
from design.plone.iocittadino.interfaces import IUserStore
from design.plone.iocittadino.interfaces.store import IDesingBaseDataStore


@implementer(IUserStore)
@adapter(Interface, Interface, Interface)
class UserStore(object):
    # TODO: usare il registry
    # we can have saved the field timestamp to manage the
    # privacy requirements
    # the name convetion should have the following format: "<key>.timestamp" = "2023-08-21T10:34:51.252947"
    user_properties = [
        "id",
        "fullname",
        "fullname",
        "nome",
        "cognome",
        "fiscalNumber",
        "mobile",
        "gender",
        "dateOfBirth",
        "placeOfBirth",
        "address",
        "digitalAddress",
        "email",
    ]

    def __init__(self, context, user, request):
        self.context = context
        self.user = user
        self.request = request

    def _check_user(self):
        current = api.user.get_current()
        if current.getId() != self.user.getId() and not api.user.has_permission(
            "Manage Portal"
        ):
            raise Unauthorized(
                translate(
                    _(
                        "set_user_error",
                        "You can't update user properties for a different user.",
                    )
                )
            )

    def _get_user_record(self):
        records = [
            *self.store.search(query={"userid": self.user.getId()}, sort_index="userid")
        ]
        if len(records) == 0:
            return None
        if len(records) == 1:
            return records[0]
        raise Exception(
            translate(
                _(
                    "multiple_user_error",
                    'Multiple Records found in storage for userid "{userid}".',
                    mapping={"userid": self.user.getId()},
                )
            )
        )

    def get(self):
        self._check_user()
        data = {key: self.user.getProperty(key, "") for key in self.user_properties}
        record = self._get_user_record()

        if record:
            for key, value in record.attrs.items():
                # remove the service data from response
                if ".timestamp" not in key:
                    data[key] = value

        return data

    # TODO: THESE METHODS SHOULD BE REFACTORED
    @property
    def store(self):
        store = queryMultiAdapter(
            (api.portal.get(), self.request),
            IDesingBaseDataStore,
            name=CONTENT_TYPE_USER,
        )
        return store

    def set(self, data):
        """Create a 'user' record

        :param data: the fields to add
        :returns: the created record
        :rtype: Record
        :raises Exception: if the record cannot be created

        """

        self._check_user()

        # Use named fields to store the user data
        onceonly_fields = set()
        model_form = api.content.get(UID=data.get("form_id", ""))

        if model_form:
            try:
                pratica_model = json.loads(model_form.pratica_model)
            except json.decoder.JSONDecodeError:
                pratica_model = {}

            for page in pratica_model.get("pages", []):
                for element in page.get("elements", []):
                    valueName = element.get("valueName", None)
                    if valueName and valueName not in self.user_properties:
                        onceonly_fields.add(valueName)

                    for element in element.get("elements", []):
                        valueName = element.get("valueName", None)
                        if valueName and valueName not in self.user_properties:
                            onceonly_fields.add(valueName)

        if not onceonly_fields:
            return

        # get the record
        record = self._get_user_record()
        if not record:
            new_record = {}
            new_record["userid"] = self.user.getId()
            record_id = self.store.add(new_record).intid
            record = self.store.get(record_id)

        update_data = {}

        for key, val in data.get("data", {}).items():
            if key in onceonly_fields:
                update_data[key] = val
                update_data[key + ".timestamp"] = datetime.now().isoformat()

        self.store.update(record.intid, update_data)
