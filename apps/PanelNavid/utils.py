from django.conf import settings

def save_background(file):
    if settings.DEBUG:
        root = 'static'
    else:
        root = str(settings.STATIC_ROOT)
        
    with open(root + '\\media\\background.jpg',mode='wb') as Backgroud:
        Backgroud.write(file.read())