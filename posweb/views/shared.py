from posweb.resources import (ApiRouter, Root)
def RequestIsAPI(context, request):
    if (context.__parent__ == ApiRouter):
        return True

    return False
def RequestIsPage(context, request):
    print context.__parent__
    if (context.__parent__ == Root):
        return True
    return False