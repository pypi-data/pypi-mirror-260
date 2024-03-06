# -*- coding: utf-8 -*-
from zope.interface import implementer
from zope.interface.interfaces import ObjectEvent

from design.plone.iocittadino.events.content_store.events.interfaces import (
    IPraticaAssignedEvent,
)
from design.plone.iocittadino.events.content_store.events.interfaces import (
    IPraticaCreatedEvent,
)
from design.plone.iocittadino.events.content_store.events.interfaces import (
    IStoreRecordCreatedEvent,
)
from design.plone.iocittadino.events.content_store.events.interfaces import (
    IStoreRecordDeletedEvent,
)
from design.plone.iocittadino.events.content_store.events.interfaces import (
    IStoreRecordTransitionEvent,
)
from design.plone.iocittadino.events.content_store.events.interfaces import (
    IStoreRecordUpdatedEvent,
)


@implementer(IStoreRecordTransitionEvent)
class StoreRecordTransitionEvent(ObjectEvent):
    def __init__(self, obj, old_state, new_state):
        super().__init__(obj)
        self.old_state = old_state
        self.new_state = new_state


@implementer(IStoreRecordCreatedEvent)
class StoreRecordCreatedEvent(ObjectEvent):
    def __init__(self, obj):
        super().__init__(obj)


@implementer(IStoreRecordUpdatedEvent)
class StoreRecordUpdatedEvent(ObjectEvent):
    def __init__(self, old_obj, obj):
        self.old_obj = old_obj
        super().__init__(obj)


@implementer(IStoreRecordDeletedEvent)
class StoreRecordDeletedEvent(ObjectEvent):
    def __init__(self, obj):
        super().__init__(obj)


# Pratica events
@implementer(IPraticaAssignedEvent)
class PraticaAssignedEvent(ObjectEvent):
    def __init__(self, obj):
        super().__init__(obj)


@implementer(IPraticaCreatedEvent)
class PraticaCreatedEvent(ObjectEvent):
    def __init__(self, obj):
        super().__init__(obj)
