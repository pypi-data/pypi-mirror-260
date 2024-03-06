# -*- coding: utf-8 -*-

from plone import api
from plone.app.layout.viewlets import ViewletBase


class ManifestJsonViewlet(ViewletBase):
    def update(self):
        self.portal_url = api.portal.get().absolute_url()
        self.enabled = api.portal.get_registry_record(
            name="collective.manifestjson.manifest_settings.manifest_enabled",
            default=True,
        )

    def index(self):
        return super(ManifestJsonViewlet, self).render()
