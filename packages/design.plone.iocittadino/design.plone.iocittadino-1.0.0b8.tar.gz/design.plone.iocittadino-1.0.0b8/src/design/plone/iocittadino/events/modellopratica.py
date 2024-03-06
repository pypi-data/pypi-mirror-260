# -*- coding: utf-8 -*-
from pkg_resources import resource_string

from design.plone.iocittadino import logger


def modified(obj, event):
    """
    @param obj: Content item (ModelloPratica)

    @param event: Event that triggers the method
    """
    # XXX: rendere più generico
    if (
        "IModelloPratica.model" in event.descriptions[0].attributes
        and obj.model != "custom"
    ):
        # reset to a different model
        obj.pratica_model = resource_string(
            "design.plone.iocittadino", f"models/{obj.model}"
        )
    elif "IModelloPratica.pratica_model" in event.descriptions[0].attributes:
        obj.model = "custom"
    else:
        # TODO: ci sono altre casistiche ?
        logger.warning(f"{obj} {event.descriptions}")


# TODO: il default al momento è (anche) su volto


def created(obj, event):
    """
    @param obj: Content item (ModelloPratica)
    @param event: Event that triggers the method
    """
    if not obj.model and not obj.pratica_model:
        # set default empty model
        obj.model = "empty.json"
        obj.pratica_model = resource_string(
            "design.plone.iocittadino", f"models/{obj.model}"
        )
    elif obj.model and not obj.pratica_model:
        obj.pratica_model = resource_string(
            "design.plone.iocittadino", f"models/{obj.model}"
        )
