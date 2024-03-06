# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView

MESSAGE_CREATED_EMAIL = "MESSAGE_CREATED_EMAIL"
PRATICA_SAVED_EMAIL = "PRATICA_SAVED_EMAIL"
PRATICA_ASSIGNED_EMAIL = "PRATICA_ASSIGNED_EMAIL"


class MailView(BrowserView):
    def __call__(self, *args, **kwargs):
        """
        Args:
            mail_type (str): Portal email type, possible values: `PRATICA_CREATED_EMAIL`,
                `PRATICA_SAVED_EMAIL`, `PRATICA_ASSIGNED_EMAIL`
        """
        return super().__call__(*args, **kwargs)

    def get_portal(self):
        return api.portal.get()

    def get_pratica_title(self, pratica):
        pratica_model = api.content.get(UID=pratica.attrs.get("form_id"))

        return getattr(pratica_model, "pratica_model", "")
