# -*- coding: utf-8 -*-
from typing import List

from plone import api
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import Interface
from zope.interface import implementer

from design.plone.iocittadino.data_store import StoreRecord
from design.plone.iocittadino.interfaces import IModelloPratica
from design.plone.iocittadino.interfaces import IPraticaPdfGenerator
from design.plone.iocittadino.interfaces import ISurveyFormField

from . import PdfGenerator

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

import json
import logging

logger = logging.getLogger(__name__)


@implementer(IPraticaPdfGenerator)
@adapter(IModelloPratica, Interface)
class PraticaPdfGenerator(PdfGenerator):
    def get_html(self, record: StoreRecord) -> str:
        res = api.content.get_view(
            context=self.context, request=self.request, name="pratica_pdf"
        )(
            fields_block=self.render_survey_fields(record),
            portal=api.portal.get(),
            pratica_model=self.context,
        )
        return res

    @property
    def logob64(self) -> str:
        """Implement after logo saved to portal registry"""
        return ""

    @property
    def stylesheets(self) -> List[str]:
        return [
            files("design.plone.iocittadino.survey_pdf.static")
            .joinpath("pratica.css")
            .read_text()
        ]

    def render_survey_fields(self, record: StoreRecord) -> str:
        rendered_fields = ""
        survey_data = record.attrs.get("data", None)

        try:
            survey_form = json.loads(self.context.pratica_model)
        except json.decoder.JSONDecodeError:
            logger.error(
                f"Could not decode the survey form of {self.context.absolute_url()}"
            )
            return ""

        if type(survey_data) is not dict:
            logger.error("Bad survey data type (!dict)")
            return ""

        if not survey_form:
            logger.error("Could not render the pratica pdf due to missing survey form")
            return ""

        if not survey_data:
            logger.error(
                "Could not render the pratica pdf due to missing survey form data"
            )
            return ""

        # TODO: rewrite using the cycles
        def render_elements(elements):
            rendered_fields = ""

            for element in elements:
                inner_elements = element.get("elements", [])

                if inner_elements:
                    rendered_fields += render_elements(inner_elements)

                field_adapter = queryMultiAdapter(
                    (self.context, self.request),
                    ISurveyFormField,
                    name="survey_" + element.get("type", ""),
                )

                if field_adapter:
                    value = survey_data.get(
                        element.get("valueName", element.get("name", "")), ""
                    )
                    if not value:
                        continue
                    rendered_fields += field_adapter(
                        field=element,
                        value=value,
                    )
                else:
                    logger.warn(
                        f"Survey field adapter was not found for: {element.get('type', '')}"
                    )

            return rendered_fields

        for page in survey_form.get("pages", []):
            rendered_fields += render_elements(page.get("elements", []))

        return rendered_fields
