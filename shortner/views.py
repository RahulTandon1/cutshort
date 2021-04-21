# from django.contrib import messages
from json import loads, dumps
from .models import Link
from django.db.models import Sum
from django.db import OperationalError
from tenacity import (retry, stop_after_attempt, wait_fixed,
                      retry_if_exception_type)

import random
import string
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponse, HttpResponseServerError, Http404,
                         HttpResponseBadRequest)


# For Google Web Crawler to work and website to show up on Google
def robots_txt(request):

    lines = [
        "User-Agent: *",
        "Disallow: /admin/"
        # "Disallow: /*"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# Returning home page
def index(request):
    stats = get_stats()
    return render(request, 'shortner/index.html', context=stats)

# returns stats for rendering in index.html


def return_last_value(retry_state):
    print(f'\n\n attempt number {retry_state.attempt_number} \n \
        function for which retry was called: {retry_state.fn} \n\n')


@retry(retry=retry_if_exception_type(OperationalError),
       stop=stop_after_attempt(2),
       wait=wait_fixed(0.5),
       retry_error_callback=return_last_value)
def get_stats():

    # generating date information
    d1 = datetime.datetime(2020, 8, 30)
    d2 = datetime.datetime.now()
    time_difference = d2-d1
    months = round(time_difference.days / 30)

    stats = {
        'total_links': Link.objects.all().count(),
        'total_clicks':
            Link.objects.aggregate(total_clicks=Sum('clicks'))['total_clicks'],
        'active_months': months
    }

    return stats


def check(request, shortlink):
    if linkExists(shortlink):
        return HttpResponse(dumps({'link': shortlink, 'available': False}))
    else:
        return HttpResponse(dumps({'link': shortlink, 'available': True}))
    # not strictly required but might be useful for debugging
    print('nothing got returned')


def create(request):
    # assump1: post body exists
    # assump2: post body has 'longlink' defined

    if request.method != 'POST':
        return redirect('/')

    reqBody = loads(request.body)
    longlink = reqBody['longlink']
    shortlink = ''  # temporary empty value

    try:
        shortlink = reqBody['shortlink']

        if shortlink == '':
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


@retry(retry=retry_if_exception_type(OperationalError),
       stop=stop_after_attempt(2),
       wait=wait_fixed(0.5),
       retry_error_callback=return_last_value)
def rediretor(request, shortlink):
    shortlinkObj = get_object_or_404(Link, pk=shortlink)

    # uncomment below lines when adding feature
    shortlinkObj.clicks += 1
    shortlinkObj.save()

    return redirect(shortlinkObj.longlink)


def custom_404(request, exception):
    return render(request, 'shortner/404.html', status=404)


def linkExists(shortlink):
    try:
        Link.objects.get(pk=shortlink)
        return True
    except Link.DoesNotExist:
        return False

# ------- helper functions ---------


def getShortRandomLink(length):
    temp = get_random_string(length)
    if linkExists(temp):
        # recursion!
        getShortRandomLink(length)
    return temp


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


# function to tell user how many clicks their link have gotten
# usable as api/clicky/<shortlink>
def clicks(request, shortlink):
    # print(f"shortlink of cliks is {shortlink}\n")
    if linkExists(shortlink):
        link = Link.objects.get(pk=shortlink)
        return HttpResponse(link.clicks)

    else:
        return HttpResponse('0')
