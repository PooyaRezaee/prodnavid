# from mutagen.mp3 import MP3
# audio = MP3("http://127.0.0.1:8000/media/beat/audio/2022/12/09/3.mp3")
# print(audio.info.length)
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import Beat
import mutagen
import random

@receiver(pre_save,sender=Beat)
def pre_save_beat(sender,  **kwargs):
    instance = kwargs['instance']

    if not instance.code:
        while True:
            rand_code = random.randint(10000,99999)
            if Beat.objects.filter(code=rand_code).exists():
                continue
            else:
                break
        instance.code = rand_code
    try:
        audio_info = mutagen.File(instance.main_beat).info
        instance.time_audio = int(audio_info.length)
    except:
        audio_info = mutagen.File(instance.audio_beat).info
        instance.time_audio = int(audio_info.length)

# @receiver(post_save,sender=Beat)
# def post_save_beat(sender,  **kwargs):
#     instance = kwargs['instance']
#     if kwargs['created']:
#         while True:
#             rand_code = random.randint(10000,99999)
#             if Beat.objects.filter(code=rand_code).exists():
#                 continue
#             else:
#                 break
#         instance.code = rand_code
#         instance.save()