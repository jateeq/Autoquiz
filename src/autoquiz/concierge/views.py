# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import TargetDocumentForm

def index(request):
	return render(request, 'concierge/index.html', None)

def getTargetDoc(request):
	if request.method == "POST":
		form = TargetDocumentForm(request.POST)
		#return render(request, 'concierge/thanks.html', None)
		return showResults(request)
	else:
		form = TargetDocumentForm

	context = {'form':form}
	return render(request, 'concierge/getTargetDoc.html', context)

def showResults(request):
	results = [1, 2, 3]
	context = {'results':results}
	return render(request, 'concierge/showResults.html', context)

