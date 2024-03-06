# -*- coding: utf-8 -*-
import souper.plone
from design.plone.policy.testing import DesignPlonePolicyLayer
from design.plone.policy.testing import DesignPlonePolicyRestApiLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import applyProfile
from plone.testing import z2

import design.plone.iocittadino


class DesignPloneIocittadinoLayer(DesignPlonePolicyLayer):
    def setUpZope(self, app, configurationContext):
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=souper.plone)
        self.loadZCML(package=design.plone.iocittadino)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
        applyProfile(portal, "design.plone.iocittadino:default")


DESIGN_PLONE_IOCITTADINO_FIXTURE = DesignPloneIocittadinoLayer()


DESIGN_PLONE_IOCITTADINO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DESIGN_PLONE_IOCITTADINO_FIXTURE,),
    name="DesignPloneIocittadinoLayer:IntegrationTesting",
)


DESIGN_PLONE_IOCITTADINO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_IOCITTADINO_FIXTURE,),
    name="DesignPloneIocittadinoLayer:FunctionalTesting",
)


class DesignPloneIocittadinoApiLayer(DesignPlonePolicyRestApiLayer):
    def setUpZope(self, app, configurationContext):
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=souper.plone)
        self.loadZCML(package=design.plone.iocittadino)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
        applyProfile(portal, "design.plone.iocittadino:default")


DESIGN_PLONE_IOCITTADINO_API_FIXTURE = DesignPloneIocittadinoApiLayer()
DESIGN_PLONE_IOCITTADINO_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DESIGN_PLONE_IOCITTADINO_API_FIXTURE,),
    name="DesignPloneIocittadinoApiLayer:Integration",
)

DESIGN_PLONE_IOCITTADINO_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_IOCITTADINO_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="DesignPloneIocittadinoApiLayer:Functional",
)
