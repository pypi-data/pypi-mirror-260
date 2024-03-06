# -*- coding: utf-8 -*-
import re

from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.row import DictRow
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from Products.CMFPlone.PloneTool import EMAIL_RE
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema

from design.plone.iocittadino import _
from design.plone.iocittadino.exceptions import InvalidEmailError


def isEmail(value):
    if re.match(EMAIL_RE, value):
        return True
    raise InvalidEmailError


class INextStepsValueSchema(model.Schema):
    days_number = schema.TextLine(
        title=_("next_steps_value_numero_title", default="Testo"),
        description=_(
            "next_steps_value_numero_help",
            default="Descrizione",
        ),
        required=True,
    )
    title = schema.TextLine(
        title=_("next_step_value_title_title", default="Titolo"),
        description=_(
            "next_steps_value_title_help",
            default="Titolo del prossimo passo",
        ),
        required=True,
    )


class IModelloPratica(model.Schema):
    """Marker interface and Dexterity Python Schema for ModelloPratica"""

    # al salvataggio se presente un json differente dal modello, il modello scelto diventa
    # automaticamente "custom"
    model = schema.Choice(
        title=_("select_model_label", default="Modello"),
        vocabulary="design.plone.iocittadino.ModelsVocabulary",
        required=False,
    )

    # al salvataggio se "model" è diverso da "custom" e non c'è un valore per il json
    # il valore viene inizializzato con quello del modello
    # automaticamente "custom"
    # JSON
    # TODO: rename field
    pratica_model = schema.Text(
        title=_("pratica_model_label", default="Pratica Model"), required=False
    )
    servizi_collegati = RelationList(
        title=_("servizi_collegati_label", default="Servizi collegati"),
        description=_(
            "servizi_collegati_help",
            default="Seleziona la lista dei servizi collegati a questo.",
        ),
        default=[],
        value_type=RelationChoice(
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
    )
    next_steps = schema.List(
        title=_("next_steps_title", default="Prossimi passi"),
        default=[],
        value_type=DictRow(schema=INextStepsValueSchema),
        required=False,
    )

    pratica_transition_message = schema.SourceText(
        title=_(
            "pratica_transition_message_title",
            default="Messaggio al cambio di stato della pratica",
        ),
        description=_(
            "pratica_transition_message_description",
            default="""Testo del messaggio inviato al cambio di stato della pratica
                Le variabili che possono essere usate nel messaggio:
                ${pratica_new_state} - stato nuovo della pratica
                ${pratica_old_state} - stato precedente della pratica
                ${pratica_id} - id della pratica""",
        ),
        required=True,
        default="Lo stato della sua pratica n. ${pratica_id} è stato cambiato in ${pratica_new_state}",
    )

    pratica_notification_emails = schema.List(
        title=_("pratica_notification_emails_title", "Email notifica"),
        description=_(
            "pratica_notification_emails_desription",
            "Indirizzi di notifica al salvataggio della pratica",
        ),
        value_type=schema.TextLine(constraint=isEmail),
        required=False,
    )

    form.widget(
        "servizi_collegati",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Servizio"],
        },
    )
    form.widget(
        "next_steps",
        DataGridFieldFactory,
        frontendOptions={"widget": "data_grid"},
    )
