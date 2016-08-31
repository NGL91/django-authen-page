from __future__ import unicode_literals

import sys
from django.apps import AppConfig
from django.db.models.signals import post_migrate




def setup_dummy_social_apps(sender, **kwargs):
	"""
	`allauth` needs tokens for OAuth based providers. So let's
	setup some dummy tokens
	"""
	
	from allauth.utils import get_current_site
	from allauth.socialaccount.models import SocialApp
	from django.contrib.sites.models import Site
	from allauth.socialaccount.providers import registry
	from allauth.socialaccount.providers.oauth.provider import OAuthProvider
	from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

	print '\n...setup_dummy_social_apps'
	
	request = kwargs.get('request')

	site = get_current_site(request)
	for provider in registry.get_list():
	    if (isinstance(provider, OAuth2Provider)
	        or isinstance(provider, OAuthProvider)):
	        try:
	            SocialApp.objects.get(provider=provider.id, sites=site)
	        except SocialApp.DoesNotExist:

	            site = Site.objects.get(id=1)
	            app = SocialApp.objects.create(provider=provider.id,
	                                           secret='e07472957e95a6452c89afa5781cd1fc',
	                                           client_id='525151244328288',
	                                           name='%s app' % provider.id)
	            app.sites.add(site)

	            localhost = 'localhost:8000'
	            site.name= localhost
	            site.domain = localhost
	            site.save()

class DjangoAuthenPageConfig(AppConfig):
	name = 'django_authen_page'

	def ready(self):
		if 'migrate' in sys.argv:
			post_migrate.connect(setup_dummy_social_apps, sender=self)


