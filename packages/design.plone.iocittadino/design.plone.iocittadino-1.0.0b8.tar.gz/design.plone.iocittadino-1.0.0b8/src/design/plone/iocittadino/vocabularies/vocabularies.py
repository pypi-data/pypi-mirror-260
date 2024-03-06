# -*- coding: utf-8 -*-
import json

from pkg_resources import resource_listdir
from pkg_resources import resource_string
from plone.memoize import forever
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from design.plone.iocittadino import _


@implementer(IVocabularyFactory)
class ModelsVocabulary(object):
    @forever.memoize
    def get_terms(self):
        terms = []
        for model in resource_listdir("design.plone.iocittadino", "models"):
            data = json.loads(
                resource_string("design.plone.iocittadino", f"models/{model}")
            )
            terms.append({"title": data["title"], "id": model})
        terms.append({"title": _("Custom"), "id": "custom"})
        # SORT ?
        return terms

    def __call__(self, context):
        return SimpleVocabulary(
            [
                SimpleTerm(value=term["id"], token=term["id"], title=term["title"])
                for term in self.get_terms()
            ]
        )


ModelsVocabularyFactory = ModelsVocabulary()
