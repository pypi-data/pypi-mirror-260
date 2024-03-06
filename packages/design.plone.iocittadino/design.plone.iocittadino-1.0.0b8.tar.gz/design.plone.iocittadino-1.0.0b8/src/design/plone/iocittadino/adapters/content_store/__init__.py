# -*- coding: utf-8 -*-
from typing import List

from plone import api
from zExceptions import Unauthorized
from zope.component import queryMultiAdapter
from zope.event import notify
from zope.i18n import translate

from design.plone.iocittadino import _
from design.plone.iocittadino import logger
from design.plone.iocittadino.adapters.content_store.mixins.current_user import (
    CurrentUserMixIn,
)
from design.plone.iocittadino.data_store import StoreRecord
from design.plone.iocittadino.events.content_store.events.events import (
    StoreRecordCreatedEvent,
)
from design.plone.iocittadino.events.content_store.events.events import (
    StoreRecordDeletedEvent,
)
from design.plone.iocittadino.events.content_store.events.events import (
    StoreRecordTransitionEvent,
)
from design.plone.iocittadino.events.content_store.events.events import (
    StoreRecordUpdatedEvent,
)
from design.plone.iocittadino.interfaces.store import IDesingBaseDataStore


class DesignBaseContentStore(CurrentUserMixIn):
    """Base implemetation for a storage"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def has_unrestricted_search_permission(self):
        return api.user.has_permission(self.manage_permission, obj=api.portal.get())

    # store methods
    @property
    def store(self):
        store = queryMultiAdapter(
            (api.portal.get(), self.request),
            IDesingBaseDataStore,
            name=self.content_type,
        )
        return store

    @property
    def indexes(self) -> List[str]:
        return self.store.indexes

    @property
    def keyword_indexes(self):
        return self.store.keyword_indexes

    @property
    def text_indexes(self):
        return self.store.text_indexes

    @property
    def length(self):
        return self.store.length

    # content storage management methods
    @property
    def content_type(self) -> str:
        raise NotImplementedError("The method was not implemented")

    @property
    def allowed_delete_states(self) -> List:
        raise NotImplementedError("The method was not implemented")

    @property
    def manage_permission(self) -> str:
        raise NotImplementedError("The method was not implemented")

    @property
    def states(self) -> dict:
        raise NotImplementedError("The method was not implemented")

    @property
    def allowed_states(self) -> List:
        raise NotImplementedError("The method was not implemented")

    @property
    def _user_can_access(self, record: StoreRecord) -> bool:
        """Check if the current user can access the record.

        :param record: a storage record
        :return: True if the user can access the record, False otherwise
        """
        raise NotImplementedError("The method was not implemented")

    @property
    def fields(self) -> dict:
        return {
            "userid": {
                "required": False,
            },
            "state": {"required": False},
        }

    @property
    def initial_state(self) -> str:
        raise NotImplementedError("The method was not implemented")

    @property
    def required_fields(self) -> List:
        return [
            field for field, data in self.fields.items() if data.get("required", False)
        ]

    # CRUD methods
    def add(self, **kwargs) -> StoreRecord:
        self._validate_add(**kwargs)

        new_record = {}

        for key, val in kwargs.items():
            if key not in self.fields.keys():
                logger.warning("[ADD] SKIP unkwnown field: %s", key)
            else:
                new_record[key] = val

        # set userid
        if not kwargs.get("userid"):
            new_record["userid"] = self.get_current_userid()

        result = self.store.add(new_record)

        if result:
            notify(StoreRecordCreatedEvent(result))
        else:
            raise Exception(
                translate(
                    _(
                        "error_add_label",
                        default="Error creating a new record.",
                    ),
                    context=self.request,
                )
            )

        return result

    def get(self, item_id: int) -> StoreRecord:
        record = self.store.get(item_id)

        if not self._user_can_access(record):
            raise Unauthorized(
                translate(
                    _(
                        "unauthorized_get",
                        default="You can't get this record.",
                    ),
                    context=self.request,
                )
            )

        return record

    def update(self, item_id, data) -> StoreRecord:
        self._validate_update(**data)
        old = self.get(item_id)
        keys = self.fields.keys()
        new = {}
        for k, v in data.items():
            if k not in keys:
                logger.warning("[UPDATE] SKIP field: %s", k)
            else:
                new[k] = v
        new = self.store.update(item_id, new)
        notify(StoreRecordUpdatedEvent(old, new))
        return new

    def delete(self, item_id) -> None:
        record = self.get(item_id)
        if record:
            self.store.delete(item_id)
            notify(StoreRecordDeletedEvent(record))

    def search(
        self,
        query: dict = None,
        sort_index: str = "date",
        reverse: bool = True,
    ) -> List[StoreRecord]:
        query = query or {}

        if not self.has_unrestricted_search_permission():
            query["userid"] = self.get_current_userid()

        return self.store.search(
            query=query,
            sort_index=sort_index,
            reverse=reverse,
        )

    def clear(self) -> None:
        self.store.clear()

    def get_initial_state(self) -> str:
        return self.initial_state

    def update_state(self, item_id, state) -> None:
        """Reruns None in case of success"""

        record = self.get(item_id=item_id)

        self._validate_transition(state=state, record=record)

        old_state = record.attrs["state"]

        self.store.update(record.intid, {"state": state})

        notify(StoreRecordTransitionEvent(record, old_state, state))

        return record

    def get_records_by_userid(self, userid):
        """Return all records for the given userid"""
        return self.search({"userid": userid})

    # validators
    def _validate_transition(self, state: str, record: StoreRecord):
        if not state:
            raise ValueError(
                translate(
                    _(
                        "missing_required_field",
                        default='Missing "${field}" field.',
                        mapping={"field": "state"},
                    ),
                    context=self.request,
                )
            )
        if state not in self.states.keys():
            raise ValueError(
                translate(
                    _(
                        "wrong_state_label",
                        default="Unknown state: ${state}.",
                        mapping={"state": state},
                    ),
                    context=self.request,
                )
            )
        record_state = record.attrs.get("state", "")
        state_data = self.states.get(record_state, {})

        if state not in state_data["available_states"]:
            raise ValueError(
                translate(
                    _(
                        "wrong_transition_label",
                        default="Unable to change state from ${old} to ${new}.",
                        mapping={"old": record_state, "new": state},
                    ),
                    context=self.request,
                )
            )

    def _validate_add(self, **kwargs) -> None:
        """Validate data

        :param kwargs: the fields to add
        :raises Unauthorized: if the user is not logged in
        :raises ValueError: if a required field is missing
        :raises ValueError: if the state is not allowed
        """
        if not self.get_current_userid():
            raise Unauthorized(
                translate(
                    _("unauthorized_add", default="You can't add records."),
                    context=self.request,
                )
            )
        state = kwargs.get("state")

        for required in self.required_fields:
            if not kwargs.get(required):
                raise ValueError(
                    translate(
                        _(
                            "missing_required_field",
                            default='Missing "${field}" field.',
                            mapping={"field": required},
                        ),
                        context=self.request,
                    )
                )
        if state and state not in self.allowed_states:
            raise ValueError(
                translate(
                    _(
                        "wrong_state",
                        default='Unable to create a record with "${state}" initial state.',
                        mapping={"state": state},
                    ),
                    context=self.request,
                )
            )

    def _validate_update(self, **kwargs):
        """Validate the update operation.

        :param kwargs: the fields to update
        :raises Unauthorized: if the user is not logged in
        :raises ValueError: if the state is not allowed
        """

        if not self.get_current_userid():
            raise Unauthorized(
                translate(
                    _("unauthorized_add", default="You can't add records."),
                    context=self.request,
                )
            )
        state = kwargs.get("state", "")

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
