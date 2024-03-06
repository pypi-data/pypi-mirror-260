# -*- coding: utf-8 -*-
from plone import api


class CurrentUserMixIn:
    def get_current_userid(self):
        if api.user.is_anonymous():
            return ""
        current = api.user.get_current()
        return current.getId()

    def get_current_user_email(self):
        if api.user.is_anonymous():
            return ""
        current = api.user.get_current()
        return current.getProperty("email")
