

# COMMON UNIT LISTS
CONCENTRATION_UNITS = (("l","Liter"),("ml","Microliter"),)
VOLUME_UNITS = (("l","Liter"),("ml","Microliter"),)
TIME_UNITS = (("m","Minutes"),("s","Seconds"),)
SPEED_UNITS = (("rpm","Revolutions Per Minutes"),("rps","Revolutions Per Seconds"),)
TEMPERATURE_UNITS = (("c","Celsius"),("k","Kelvin"),("f","Ferinheit"),)


def check_protocol_edit_authorization(protocol, user):

    if user.is_superuser or user.is_staff or protocol.owner.pk in [ org.pk for org in user.organization_set.all() ]:
        return True
    return False
