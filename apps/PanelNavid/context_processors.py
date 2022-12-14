from .models import SiteSettings,Message

def settings(request):
    return {'settings': SiteSettings.load()}

def new_messages(request):
    return {'new_messages': Message.objects.filter(seen=False).order_by('-created')[:5]}