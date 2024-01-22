from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('User Profile is created successfully')
    else:
        try:
            #update profile
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print('User Profile is updated successfully')
        except:
            #create profile if not exist
            UserProfile.objects.create(user=instance)
            print('User Profile is created successfully')

@receiver(pre_save, sender=User)
def pre_save_profile(sender, instance, **kwarg):
    print(instance.username, 'this is user being saved')

# post_save.connect(post_save_create_profile_receiver, sender=User)