from django.http import HttpResponse
from django.template import RequestContext, loader

def home(request, network, channel):
	template = loader.get_template('index.html')
	context = RequestContext(request, {'network': network, 'channel': channel})
	return HttpResponse(template.render(context))

