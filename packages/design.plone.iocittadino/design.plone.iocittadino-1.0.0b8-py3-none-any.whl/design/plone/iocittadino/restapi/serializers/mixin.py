# -*- coding: utf-8 -*-
from plone import api
from plone.registry.interfaces import IRegistry
from plone.volto.interfaces import IVoltoSettings
from zope.component import getUtility
from zope.globalrequest import getRequest


class PortalUrlMixIn:
    def get_portal_url(self):
        portal_state = api.content.get_view(
            name="plone_portal_state",
            context=api.portal.get(),
            request=getRequest(),
        )

        portal_url = portal_state.navigation_root_url()
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IVoltoSettings, prefix="volto", check=False)
        settings_frontend_domain = getattr(settings, "frontend_domain", None)

        if (
            settings_frontend_domain
            and settings_frontend_domain != "http://localhost:3000"
        ):
            portal_url = settings_frontend_domain

        if portal_url.endswith("/"):
            portal_url = portal_url[:-1]

        return portal_url
