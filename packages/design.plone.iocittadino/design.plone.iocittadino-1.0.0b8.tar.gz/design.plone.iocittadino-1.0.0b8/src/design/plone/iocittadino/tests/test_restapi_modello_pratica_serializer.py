# -*- coding: utf-8 -*-
from design.plone.iocittadino.tests.restapi_mixin import Mixin


class TestRestapiModelloPratica(Mixin):
    def test_anonymous_cant_get_modello_pratica_even_if_it_is_published(self):
        resp = self.api_session_anon.get(self.modello_pratica.absolute_url())
        self.assertEqual(resp.status_code, 401)

    def test_auth_can_get_modello_pratica(self):
        resp = self.api_session_auth.get(self.modello_pratica.absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_gestore_can_get_modello_pratica(self):
        resp = self.api_session_gestore.get(self.modello_pratica.absolute_url())
        self.assertEqual(resp.status_code, 200)
