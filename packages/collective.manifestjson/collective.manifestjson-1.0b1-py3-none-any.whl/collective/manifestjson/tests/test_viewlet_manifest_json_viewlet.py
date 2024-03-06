# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from Products.Five.browser import BrowserView
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

from collective.manifestjson.interfaces import ICollectiveManifestjsonLayer
from collective.manifestjson.testing import (
    COLLECTIVE_MANIFESTJSON_FUNCTIONAL_TESTING,
    COLLECTIVE_MANIFESTJSON_INTEGRATION_TESTING,
)


class ViewletIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_MANIFESTJSON_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.app = self.layer["app"]
        self.request = self.app.REQUEST
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Document", "other-document")
        api.content.create(self.portal, "News Item", "newsitem")

    def test_manifest_json_viewlet_is_registered(self):
        view = BrowserView(self.portal["other-document"], self.request)
        manager_name = "plone.htmlhead.links"
        alsoProvides(self.request, ICollectiveManifestjsonLayer)
        manager = queryMultiAdapter(
            (self.portal["other-document"], self.request, view),
            IViewletManager,
            manager_name,
            default=None,
        )
        self.assertIsNotNone(manager)
        manager.update()
        my_viewlet = [
            v for v in manager.viewlets if v.__name__ == "manifest-json-viewlet"
        ]  # NOQA: E501
        self.assertEqual(len(my_viewlet), 1)

    # XXX would be nice to have this test working:
    # def test_manifest_json_viewlet_is_not_available_on_newsitem(self):
    #     view = BrowserView(self.portal['newsitem'], self.request)
    #     manager_name = 'plone.abovecontenttitle'
    #     alsoProvides(self.request, ICollectiveManifestjsonLayer)
    #     manager = queryMultiAdapter(
    #         (self.portal['newsitem'], self.request, view),
    #         IViewletManager,
    #         manager_name,
    #         default=None
    #     )
    #     self.assertIsNotNone(manager)
    #     manager.update()
    #     my_viewlet = [v for v in manager.viewlets if v.__name__ == 'manifest-json-viewlet']  # NOQA: E501
    #     self.assertEqual(len(my_viewlet), 0)


class ViewletFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_MANIFESTJSON_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
