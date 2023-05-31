from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
  
def homeview(request):
  return render(request,"apnamd_ai/index.html")