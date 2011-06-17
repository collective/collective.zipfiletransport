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

import os
import zope.formlib
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

try: # >= 4.1 
    from five.formlib.formbase import EditForm
except ImportError: # < 4.1 
    from Products.Five.formlib.formbase import EditForm

_FORMLIB_DIR = os.path.dirname(zope.formlib.__file__)
_PAGEFORM_PATH = os.path.join(_FORMLIB_DIR, 'pageform.pt')

class BaseForm(EditForm):
    """ Base form to avoid """
    template = ViewPageTemplateFile(_PAGEFORM_PATH)
