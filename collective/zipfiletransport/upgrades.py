from Products.CMFCore.utils import getToolByName


def upgrade_100_to_101(context):
    zipfile_properties = getToolByName(context, 'portal_properties').zipfile_properties
    zipfile_properties.manage_addProperty(id='allow_zip64', value=False, type="boolean")

