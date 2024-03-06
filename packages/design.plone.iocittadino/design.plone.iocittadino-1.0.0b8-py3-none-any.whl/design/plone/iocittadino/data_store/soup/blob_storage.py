# -*- coding: utf-8 -*-
import uuid

from persistent.mapping import PersistentMapping
from plone import api
from plone.namedfile import NamedBlobFile
from zExceptions import InternalError
from zExceptions import Unauthorized


class BlobStorage(PersistentMapping):
    """Temporary store for blobs"""

    def __setitem__(self, name, value, *args, **kwargs):
        if not type(value.get("blob")) is NamedBlobFile:
            raise InternalError(
                f"Only the {str(NamedBlobFile)} instances are allowed as a `blob`."
            )

        try:
            uuid.UUID(name)

        except ValueError:
            raise InternalError("Badly formed key, expected a valid UUID string.")

        return super().__setitem__(name, value, *args, **kwargs)

    def add(self, file):
        identifier = uuid.uuid4().hex
        self[identifier] = {
            "blob": file,
            "userid": api.user.get_current().getId(),
        }
        return identifier

    def get(self, key, *args, **kwargs):
        item = super().get(key=key, default=None)

        if not item:
            return None or kwargs.get("default")

        if not self.user_can_access(item):
            raise Unauthorized(f"Unauthorized attempt to access the {str(item)} file.")

        return item["blob"]

    def user_can_access(self, item):
        if api.user.is_anonymous():
            return False

        userid = api.user.get_current().getId()

        # owner
        if userid == item.get("userid", "unknown"):
            return True

        return api.user.has_permission("design.plone.iocittadino.ManageBlobs")
