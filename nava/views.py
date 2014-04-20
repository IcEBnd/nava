from django.http import HttpResponse
from django.template import RequestContext, loader

def home(request, channel):
	print(channel)

	template = loader.get_template('index.html')
	context = RequestContext(request, {'channel': channel})
	return HttpResponse(template.render(context))
	#return http.HttpResponse('Hello World! This is changed')

