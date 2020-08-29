# from django.contrib import messages
from json import loads, dumps
from .models import Link
import random
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseServerError, Http404, HttpResponseBadRequest


def index(request):
    return render(request, 'shortner/index.html')


def check(request, shortlink):
    if linkExists(shortlink):
        return HttpResponse(dumps({'link': shortlink, 'available': False}))
    else:
        return HttpResponse(dumps({'link': shortlink, 'available': True}))
    return HttpResponseServerError()


def create(request):
    # assump1: post body exists
    # assump1: post body has 'longlink' defined

    if request.method != 'POST':
        return redirect('/')

    reqBody = loads(request.body)
    longlink = reqBody['longlink']
    shortlink = ''  # temporary empty value

    try:
        shortlink = reqBody['shortlink']

        if shortlink=='':
            # ik it's wrong...sorry.
            raise KeyError('Empty shortlink')
        if linkExists(shortlink):
            res = HttpResponseBadRequest()
            res.reason_phrase = 'Shortlink already taken'
            res.status_code = 400
            return res
    except KeyError:
        shortlink = getShortRandomLink(5)

    obj = Link(shortlink=shortlink, longlink=longlink)
    obj.save()
    return HttpResponse(dumps(obj.getDict()))


def rediretor(request, shortlink):
    shortlinkObj = get_object_or_404(Link, pk=shortlink)
    return redirect(shortlinkObj.longlink)


def linkExists(shortlink):
    try:
        Link.objects.get(pk=shortlink)
        return True
    except Link.DoesNotExist:
        return False

# helper functinos


def getShortRandomLink(length):
    temp = get_random_string(length)
    if linkExists(temp):
        getShortRandomLink(length)
    return temp


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
