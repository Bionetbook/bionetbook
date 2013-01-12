from django.conf import settings # import the settings file

def registration_enabled(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'REGISTRATION_ENABLED': settings.REGISTRATION_ENABLED}
