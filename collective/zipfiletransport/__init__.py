##################################################################################
#    Copyright (c) 2004-2009 Utah State University, All rights reserved. 
#    Portions copyright 2009 Massachusetts Institute of Technology, All rights reserved.
#                                                                                 
#    This program is free software; you can redistribute it and/or modify         
#    it under the terms of the GNU General Public License as published by         
#    the Free Software Foundation, version 2.                                      
#                                                                                 
#    This program is distributed in the hope that it will be useful,              
#    but WITHOUT ANY WARRANTY; without even the implied warranty of               
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                
#    GNU General Public License for more details.                                 
#                                                                                 
#    You should have received a copy of the GNU General Public License            
#    along with this program; if not, write to the Free Software                  
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA    
#                                                                                 
##################################################################################

__author__  = '''Brent Lambert, David Ray, Jon Thomas'''
__version__   = '$ Revision 0.0 $'[11:-2]


# There are three ways to inject custom code here:
#
#   - To set global configuration variables, create a file AppConfig.py.
#       This will be imported in config.py, which in turn is imported in
#       each generated class and in this file.
#   - To perform custom initialisation after types have been registered,
#       use the protected code section at the bottom of initialize().
#   - To register a customisation policy, create a file CustomizationPolicy.py
#       with a method register(context) to register the policy.

import logging

logger = logging.getLogger('ZipFileTransport')

try:
    import CustomizationPolicy
except ImportError:
    CustomizationPolicy = None

from AccessControl import allow_module
from Globals import package_home
from Products.Archetypes import listTypes
from Products.Archetypes.atapi import *
from Products.Archetypes.utils import capitalize
from Products.CMFCore import DirectoryView
from Products.CMFCore import permissions
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.utils import ToolInit
from zope.i18nmessageid import MessageFactory
import utilities

ZipFileTransportMessageFactory = MessageFactory('ZipFileTransport')
allow_module('collective.zipfiletransport.ZipFileTransportMessageFactory')

import os, os.path

from collective.zipfiletransport.config import *

DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/ZipFileTransport',
                                    product_globals)


def initialize(context):
    # Initialize portal content
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    # Apply customization-policy, if theres any
    if CustomizationPolicy and hasattr(CustomizationPolicy, 'register'):
        CustomizationPolicy.register(context)
        print 'Customization policy for ZipFileTransport installed'


