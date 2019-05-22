# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName


def uninstall(context):
    portal_properties = getToolByName(context, 'portal_properties')
    portal_properties.manage_delObjects(['zipfile_properties'])
