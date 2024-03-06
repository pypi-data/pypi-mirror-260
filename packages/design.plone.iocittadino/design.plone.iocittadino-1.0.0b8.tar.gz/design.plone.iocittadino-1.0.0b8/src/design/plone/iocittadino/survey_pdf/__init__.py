# -*- coding: utf-8 -*-
from pathlib import Path
from string import Template
from typing import BinaryIO
from typing import List

from plone import api
from weasyprint import CSS
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration

from design.plone.iocittadino.data_store import StoreRecord

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

import base64


class PdfGenerator:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_html(self, record: StoreRecord) -> str:
        raise NotImplementedError("The method was not implemented")

    @property
    def stylesheets(self) -> List[str]:
        """May not be implemented"""
        return []

    @property
    def main_css(self) -> str:
        return (
            files("design.plone.iocittadino.survey_pdf.static")
            .joinpath("main.css")
            .read_text()
        )

    @property
    def fonts_css(self) -> str:
        css = (
            files("design.plone.iocittadino.survey_pdf.static")
            .joinpath("fonts.css")
            .read_text()
        )
        frontend_url = api.portal.get_registry_record(name="volto.frontend_domain")

        return Template(css).substitute(frontend_url=frontend_url)

    @property
    def font_config(self) -> FontConfiguration:
        return FontConfiguration()

    def write_pdf(self, record: StoreRecord, path: Path = None) -> BinaryIO:
        """Return binary object if not passed the path"""
        return HTML(
            string=self.get_html(record),
        ).write_pdf(
            path,
            stylesheets=[
                CSS(string=i)
                for i in [self.main_css, self.fonts_css, *self.stylesheets]
            ],
            font_config=self.font_config,
        )

    def get_pdf_as_b64(self, record: StoreRecord):
        return base64.b64encode(self.write_pdf(record))
