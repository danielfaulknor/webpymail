# -*- coding: utf-8 -*-

# WebPyMail - IMAP python/django web mail client
# Copyright (C) 2008 Helder Guerreiro

## This file is part of WebPyMail.
##
## WebPyMail is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## WebPyMail is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with WebPyMail.  If not, see <http://www.gnu.org/licenses/>.

#
# Helder Guerreiro <helder@paxjulia.com>
#
# $Id: folder_views.py 434 2008-12-05 16:55:47Z helder $
#

"""Display folders and associated actions
"""

# Imports:
# Python
import base64

# Django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Local
from webpymail.mailapp.models import FoldersToExpand
from utils import serverLogin

##
# Views
##

@login_required
def show_folders_view(request):
    '''Show the account folders.
    '''
    # Login to the server:
    M = serverLogin( request )

    # Special folders
    # TODO: will get this from the user config
    M.set_special_folders('INBOX', 'INBOX.Drafts', 'INBOX.Templates')

    # Expandable folders
    expand_folders = request.user.folderstoexpand_set.all()
    if expand_folders:
        M.set_expand_list(*[ f.folder_name for f in expand_folders ])

    # Read the subscribed folder list:
    M.refresh_folders(subscribed=True)

    return render_to_response('folder_list.html',{'server': M  })

@login_required
def set_folder_expand(request, folder):
    folder_name =  base64.urlsafe_b64decode(str(folder))
    user = request.user

    folder_in_list = FoldersToExpand.objects.filter(user__exact=user,
          folder_name__exact = folder_name).count()

    if not folder_in_list:
        f = FoldersToExpand( user = user, folder_name = folder_name)
        f.save()

    return HttpResponseRedirect(reverse('folder_list'))

@login_required
def set_folder_collapse(request, folder):
    folder_name =  base64.urlsafe_b64decode(str(folder))
    user = request.user
    FoldersToExpand.objects.filter(user__exact=user,
          folder_name__exact = folder_name).delete()

    return HttpResponseRedirect(reverse('folder_list'))