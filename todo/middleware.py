#coding: utf-8
from django.http import HttpResponseRedirect

class CheckUserSiteMiddleware(object):

    def process_request(self, request):
        if (request.path.startswith('/admin/') and
                not request.user.is_authenticated()):

            return HttpResponseRedirect('/')
