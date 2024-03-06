# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getGlobalSiteManager
from zope.interface import Interface

from design.plone.iocittadino.interfaces import IDesignPloneIocittadinoLayer
from design.plone.iocittadino.interfaces import IModelloPratica
from design.plone.iocittadino.interfaces import ISurveyFormField

# try:
#    from importlib.resources import files
# except ImportError:
#    from importlib_resources import files


class SurveyFieldView(BrowserView):
    index = None

    def __call__(self, *args, **kwargs):
        return self.index(*args, **kwargs)


class SurveyFieldAdapter:
    _field_type = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def lang(self):
        """We use Italian as default but the code might be customized"""
        return "it"

    @property
    def field_type(self):
        return self._field_type

    @property
    def view(self):
        return api.content.get_view(
            name=self.field_type, context=self.context, request=self.request
        )

    def __call__(self, field, value, *args, **kwargs):
        return self.view(field=field, value=value, lang=self.lang)


gsm = getGlobalSiteManager()

# DO NOT TOUCH THE CODE BELOW ITS A DARK MAGIC
# ... WE DON'T LIKE DARK MAGIC !
# NO MAGIC NO HAPPINESS (╥﹏╥)
# for view_path in files(
#     "design.plone.iocittadino.survey_pdf.fields.templates"
# ).iterdir():
#     field_name = view_path.name.split(".")[-2]
for field_name in (
    "survey_checkbox",
    "survey_html",
    "survey_text",
    "survey_radiogroup",
):
    gsm.registerAdapter(
        factory=type(
            "SurveyFieldView_" + field_name,
            (SurveyFieldView,),
            dict(index=ViewPageTemplateFile(f"templates/{field_name}.pt")),
        ),
        required=(IModelloPratica, IDesignPloneIocittadinoLayer),
        name=field_name,
        provided=Interface,
    )
    gsm.registerAdapter(
        factory=type(
            "SurveyFieldAdapter_" + field_name,
            (SurveyFieldAdapter,),
            dict(field_type=field_name),
        ),
        required=(IModelloPratica, IDesignPloneIocittadinoLayer),
        name=field_name,
        provided=ISurveyFormField,
    )
