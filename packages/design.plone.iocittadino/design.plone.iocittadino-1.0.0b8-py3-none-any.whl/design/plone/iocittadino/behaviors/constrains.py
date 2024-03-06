# -*- coding: utf-8 -*-
from plone.app.dexterity.behaviors.constrains import (
    ConstrainTypesBehavior as BaseBehavior,
)

# FIX
# For: ('utility', <InterfaceClass plone.behavior.interfaces.IBehavior>, 'plone.constraintypes')
# File "/Users/lucabel/workspace/buildout_cache/eggs/plone.app.dexterity-2.6.11-py3.9.egg/plone/app/dexterity/behaviors/configure.zcml", line 128.2-135.8
#     <plone:behavior
#         name="plone.constraintypes"
#         title="Folder Addable Constrains"
#         description="Restrict the content types that can be added to folderish content"
#         provides="Products.CMFPlone.interfaces.constrains.ISelectableConstrainTypes"
#         factory=".constrains.ConstrainTypesBehavior"
#         for="plone.dexterity.interfaces.IDexterityContainer"
#         />
# File "/Users/lucabel/workspace/plonecli_3.0/design.plone.iocittadino/src/design/plone/iocittadino/behaviors/configure.zcml", line 10.4-17.10
#       <plone:behavior
#           name="plone.constraintypes"
#           title="Folder Addable Constrains"
#           description="Restrict the content types that can be added to folderish content"
#           provides="Products.CMFPlone.interfaces.constrains.ISelectableConstrainTypes"
#           factory=".constrains.ConstrainTypesBehavior"
#           for="design.plone.contenttypes.interfaces.servizio.IServizio"
#           />


class ConstrainTypesBehavior(BaseBehavior):
    """
    Allow to add just one ModelloPratica under Servizio
    """

    def getDefaultAddableTypes(self, context=None):
        if context is None:
            context = self.context
        return self.getAddableTypesFor(self.context, context)
