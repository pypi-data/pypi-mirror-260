# -*- coding: utf-8 -*-
from zope.interface import Attribute
from zope.interface.interfaces import IObjectEvent


class IStoreRecordTransitionEvent(IObjectEvent):
    """An event that's fired upon a workflow transition."""

    obj = Attribute("The context object")

    old_state = Attribute(
        "The state definition of the workflow state " "before the transition"
    )
    new_state = Attribute(
        "The state definition of the workflow state " "before after transition"
    )


class IStoreRecordCreatedEvent(IObjectEvent):
    """An event that's fired on message creation."""

    obj = Attribute("The context object")


class IStoreRecordUpdatedEvent(IObjectEvent):
    """An event that's fired on message creation."""

    obj = Attribute("The context object")


class IStoreRecordDeletedEvent(IObjectEvent):
    """An event that's fired on message creation."""

    obj = Attribute("The context object")


class IPraticaAssignedEvent(IObjectEvent):
    """An event that's fired when a pratica has been assigned to someone"""


class IPraticaCreatedEvent(IObjectEvent):
    """An event that's fired when a pratica is created"""
