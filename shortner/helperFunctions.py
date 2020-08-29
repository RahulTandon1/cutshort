
# Create your views here.
import random
import string

# this is not oringal code
# copied this from https://pynative.com/python-generate-random-string/


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# determines whether or not the reqbody passed to the function
# is valid according to app's needs


def isValidReqBody(reqBody):
    # check request body has requisite fields
    requiredFields = ['toCheck', 'shortLink']
    fieldsToTest = reqBody.keys()
    for field in requiredFields:
        if field not in fieldsToTest:
            return False
    return True


def handleGet(request):
    print('Handle Get called \n')

    def isAvailable(shortLink):

        # if the shortlink is already taken/used
        if len(Link.objects.filter(shortLink=shortLink)) == 0:
            return True

        else:
            return False

    # check for json existence.
    # If JSON present it's most probably a to check for shortLink availability
    if (request.body):
        reqBody = loads(request.body)
        if isValidReqBody(reqBody):
            if isAvailable(reqBody['shortLink']):
                # shortlink is available
                return HttpResponse(dumps({"shortLinkPresent": True}))
            else:
                # shortlink is not available
                HttpResponse(dumps({
                    "shortLinkPresent": False
                }))
        else:
            # if fields don't match up
            return HttpResponse(json.loads(
                {'message':
                 "You're a cool innovative guy! BTW json ields don't match"}
            ))

    else:
        # If no JSON, it's most probably a request to the home page,
        # so return home page
        # NOTE/FOR LATER: Maybe do a redirect here?
        return render(request, 'shortner/index.html')


def handlePost(request):
    print('Handle Post called \n')

    # checks if the post body passed is a valid one.
    # this is not necessarily required
    # but in case there's somebody who tries bypassing
    # the body used in the fetch on frontend then
    # it's worth checking on the backend.
    def isValidPostBody(reqBody):
        print(reqBody.keys())
        for i in ['toCreate', 'shortLink', 'longLink']:
            if i not in reqBody.keys():
                return False
        return True

    # check whether or not a link is valid on the basis of it being prefixed by https or http
    # I could think up and make something which smartly checks whether or not a site exists
    # and then creates a link or returns an error accordingly
    # but I lazy

    def isValidLongLink(longLink):
        if not(longLink.startswith('https://')) and not(shortLink.startswith('https://')):
            return False
        else:
            return True

    # checks whether the desired shortlink, if provided by the user, is taken or not
    # this isn't necessarily required but in case somebody's playing around with the code
    # I wouldn't want the backend to malfunction or anything

    def isValidShortLink(shortLink):
        if len(Link.objects.filter(shortLink=shortLink)) != 0:
            return False
        else:
            return True

    # generatres a random shortLink based on a randomString generator
    # that I got from the internet.
    # Look at the definition of get_random_string above for more info.
    def getShortRandomLink(length):
        temp = get_random_string(length)
        if temp in Links.objects.filter(shortLink=temp):
            getShortRandomLink(length)
        return temp

    print('POST request aai')

    def createShortLink(shortLink, longLink):
        tempLink = Link(shortLink, longLink)
        tempLink.save()
        tempLinkURL = f"https://cutshort.in/{tempLink.shortLink}"
        return tempLinkURL

    def kaamKaar(shortLink, longLink):
        # if long link is valid continue
        if isValidLongLink(longLink):
            # if shortLink present check it
            if len(shortLink) != 0:
                # check if valid
                if not isValidShortLink(shortLink):
                    # if shortLink taken then inform user the same
                    context = {'errorPresent': True,
                               'errorMessage': "Shortlink already taken"}
                    return render(request, 'shortner/index.html', context)

            # if shortLink not present generate a shortLink randomly
            else:
                shortLink = getShortRandomLink(6)

            # createShortLink and re render page
            context = {'linkPresent': True,
                       'link': createShortLink(shortLink, longLink)}
            return render(request, 'shortner/index.html', context)

        else:
            # if not valid link return error to user
            context = {'errorPresent': True,
                       'errorMessage': 'The URL does not seems right. Please include the https:// or http:// in the url as well'}
            return render(request, 'shortner/index.html', context)

    # parsing the POST request body and storing in variables
    reqBody = loads(request.body)
    longLink = reqBody.get('longLink')
    shortLink = reqBody.get('shortLink')

    if not isValidPostBody(reqBody) and not isValidReqBody(reqBody):
        context = {'errorPresent': True,
                   'errorMessage': 'POST request body does not have the right fields and/or values.'
                   }

    if isValidReqBody(reqBody):
        return handleGet(request)

    return dumps({'confirmedLink': kaamKaar(shortLink, longLink)})


def index(request):
    if request.method == 'GET':
        print('is GET req')
        return render(request, 'shortner/index.html')
    elif request.method == 'POST':
        print('is POST req')
        return handlePost(request)


'''homepage
    Get:
   

    Post
    // validate url presence
    // Create
    // send confirmatory json and display that on page

/shortLink
    // Check db and redirect accordingly
    // If not found 404.
    '''
