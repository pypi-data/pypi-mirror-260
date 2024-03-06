# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

try:
    from importlib.resources import files

    HAS_IMPORTLIB = True
except ImportError:
    from pathlib import Path

    from pkg_resources import resource_filename as files

    HAS_IMPORTLIB = False


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "design.plone.iocittadino:uninstall",
            "design.plone.iocittadino:demo_contents",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["design.plone.iocittadino.upgrades"]


def post_install(context):
    """Post install script"""
    # create a new plone group
    create_group()


def create_group():
    api.group.create(
        groupname="operatori_pratiche",
        title="Operatori pratiche",
        description="Utenti che gestiscono le pratiche",
        roles=["Gestore Pratiche", "Reader"],
    )


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def demo_contents(context):
    """Post install script"""
    if HAS_IMPORTLIB:
        json_file = files("design.plone.iocittadino.demo").joinpath(
            "demo_contents.json"
        )
    else:
        # Python < 3.9
        path = files("design.plone.iocittadino", "demo/demo_contents.json")
        json_file = Path(path)
    if json_file.exists():
        portal = api.portal.get()
        request = portal.REQUEST
        view = api.content.get_view("import_content", portal, request)
        request.form["form.submitted"] = True
        request.form["commit"] = 500
        view(jsonfile=json_file.read_text(), return_json=True)
