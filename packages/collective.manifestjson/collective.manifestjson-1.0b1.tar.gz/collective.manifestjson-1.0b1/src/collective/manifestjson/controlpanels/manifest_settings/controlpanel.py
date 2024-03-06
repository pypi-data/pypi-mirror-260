# -*- coding: utf-8 -*-

from collective.manifestjson import _
from collective.manifestjson.interfaces import ICollectiveManifestjsonLayer
from plone import schema
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.z3cform.widget import SingleCheckBoxBoolFieldWidget
from plone.autoform import directives
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope.component import adapter
from zope.interface import Interface


class IManifestSettings(Interface):
    directives.widget(manifest_enables=SingleCheckBoxBoolFieldWidget)
    manifest_enabled = schema.Bool(
        title=_(
            "manifest.json enabled",
        ),
        description=_(
            "You can enable or disable the manifest.json view",
        ),
        required=False,
        default=True,
    )
    manifestcontent = schema.JSONField(
        title=_("manifest.json content"),
        description=_("Enter a JSON-formatted manifest configuration."),
        # schema=json.dumps(
        #     {
        #         "title": "Image srcset definition",
        #         "type": "object",
        #         "additionalProperties": {"$ref": "#/$defs/srcset"},
        #         "$defs": {
        #             "srcset": {
        #                 "type": "object",
        #                 "properties": {
        #                     "title": {
        #                         "type": "string",
        #                     },
        #                     "preview": {
        #                         "type": "string",
        #                     },
        #                     "hideInEditor": {
        #                         "type": "boolean",
        #                     },
        #                     "sourceset": {
        #                         "type": "array",
        #                         "items": {
        #                             "type": "object",
        #                             "properties": {
        #                                 "scale": {
        #                                     "type": "string",
        #                                 },
        #                                 "media": {
        #                                     "type": "string",
        #                                 },
        #                                 "additionalScales": {
        #                                     "type": "array",
        #                                 },
        #                             },
        #                             "additionalProperties": False,
        #                             "required": ["scale"],
        #                         },
        #                     },
        #                 },
        #                 "additionalProperties": False,
        #                 "required": ["title", "sourceset"],
        #             },
        #         },
        #     }
        # ),
        default={
            "name": "My Plone Site",
            "theme_color": "#0095d7",
            "background_color": "#fafafa",
            "display": "fullscreen",
            "Scope": "/",
            "start_url": "/",
            "icons": [
                {
                    "src": "images/icons/icon-72x72.png",
                    "sizes": "72x72",
                    "type": "image/png",
                },
                {
                    "src": "images/icons/icon-96x96.png",
                    "sizes": "96x96",
                    "type": "image/png",
                },
                {
                    "src": "images/icons/icon-128x128.png",
                    "sizes": "128x128",
                    "type": "image/png",
                },
                {
                    "src": "images/icons/icon-144x144.png",
                    "sizes": "144x144",
                    "type": "image/png",
                },
                {
                    "src": "images/icons/icon-152x152.png",
                    "sizes": "152x152",
                    "type": "image/png",
                },
                {
                    "src": "images/icons/icon-192x192.png",
                    "sizes": "192x192",
                    "type": "image/png",
                },
                {
                    "src": "images/icons/icon-384x384.png",
                    "sizes": "384x384",
                    "type": "image/png",
                },
                {
                    "src": "images/icons/icon-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                },
            ],
            "splash_pages": None,
        },
        required=True,
    )


class ManifestSettings(RegistryEditForm):
    schema = IManifestSettings
    schema_prefix = "collective.manifestjson.manifest_settings"
    label = _("Manifest Settings")


ManifestSettingsView = layout.wrap_form(ManifestSettings, ControlPanelFormWrapper)


@adapter(Interface, ICollectiveManifestjsonLayer)
class ManifestSettingsConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IManifestSettings
    configlet_id = "manifest_settings-controlpanel"
    configlet_category_id = "Products"
    title = _("Manifest Settings")
    group = ""
    schema_prefix = "collective.manifestjson.manifest_settings"
