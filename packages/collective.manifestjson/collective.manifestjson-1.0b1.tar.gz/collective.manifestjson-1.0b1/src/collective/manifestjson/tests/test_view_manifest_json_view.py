# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

from collective.manifestjson.testing import (
    COLLECTIVE_MANIFESTJSON_FUNCTIONAL_TESTING,
    COLLECTIVE_MANIFESTJSON_INTEGRATION_TESTING,
)
from collective.manifestjson.views.manifest_json_view import IManifestJsonView


class ViewsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_MANIFESTJSON_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_manifest_json_is_registered(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST), name="manifest.json"
        )
        self.assertTrue(IManifestJsonView.providedBy(view))


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_MANIFESTJSON_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
