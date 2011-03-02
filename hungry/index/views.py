from django.shortcuts import render_to_response
from django.template import RequestContext


# Homepage
def index(request):
    
    return render_to_response('index.html',
                              {},
                              context_instance=RequestContext(request))
