# -*- coding: utf-8 -*-

import json

from plone import api
from Products.Five.browser import BrowserView
from zope.interface import Interface, implementer


class IManifestJsonView(Interface):
    """Marker Interface for IManifestJsonView"""


@implementer(IManifestJsonView)
class ManifestJsonView(BrowserView):
    def __call__(self):
        manifest_content = api.portal.get_registry_record(
            name="collective.manifestjson.manifest_settings.manifestcontent"
        )
        self.request.RESPONSE.setHeader("Content-Type", "application/json")
        template = json.dumps(manifest_content)
        return template
