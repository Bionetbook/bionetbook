from django.core.exceptions import ObjectDoesNotExist

# COMMON UNIT LISTS
CONCENTRATION_UNITS = (("","None"),("ng/ul","nanogram / microliter"),("ug/ul","microgram / microliter"),("mg/ul","miligram / microliter"),("ug/ml",'microgram/mililiter'),("mg/ml","miligram / mililiter"),
    ("mg/l","miligram / liter"), ("g/ml","gram / mililiter"), ("g/l","gram / liter"), ('nM', 'nanoMolar'), ('uM', 'microMolar'), ('mM', 'miliMolar'), ('M', 'Molar'), 
    ('U/ul', 'Units / microliter'), ('U/ml', 'Units / mililiter'), ('X', 'Fold'), ('v/v%','volume percent'),('molar ratio','molar ratio'), ("ul/ml","microliter / mililiter"),)
MASS_UNITS = (("","None"),('ng', 'nanogram'),('ug', 'microgram'),('mg', 'miligram'),('g', 'gram'),('kg', 'kilogram'), ('U', 'Units'), )
VOLUME_UNITS = (("","None"),("L","liter"),("ml","Mililiter"), ("ul","microliter"), ('%v', 'percent volume'), ('%m', 'percent mass'),('fold','volumes of/ fold'))
AMMOUNT_UNITS = (("","None"),('nm', 'nanomole'),('um', 'micromole'),('mm', 'milimole'),('m', 'mole'), )
TIME_UNITS = (("","None"),("yrs","Years"),("mths","Months"),("d","Days"),("hrs","Hours"),("min","Minutes"),("sec","Seconds"),)
SPEED_UNITS = (("","None"),("rpm","Revolutions Per Minutes"),("rcf","Relative Centrifugal Force"),)
TEMPERATURE_UNITS = (("C","Celsius"),("K","Kelvin"),("F","Ferinheit"),)
VESSELS = (("","None"),('epi','1.8 ml tube'), ('pcr','200 ul tube'), ('15 ml','Falcon 15 ml'), ('50 ml', 'Falcon 50 ml'),)




def check_owner_edit_authorization(protocol, user):
    '''
    Checks the Authorization for a user to see if they can edit a given protocol based on the 
    protocol's owner, if the user is a member of that organization and the role the user has.
    '''

    if user.is_superuser or user.is_staff:      # IF THEY ARE SYSTEM ADMIN THE CAN SEE THE PROTOCOL
        return True

    try:
        membership = user.membership_set.get(org=protocol.owner)
        if membership.role in ['a','w']:                                # ADMIN OR WRITE PERMISSIONS
            return True
    except ObjectDoesNotExist:
        pass
    
    return False


def check_owner_view_authorization(protocol, user):
    '''
    Checks the Authorization for a user to see if they can view a given protocol based on the 
    protocol's owner and if the user is a member of that organization.
    '''

    if user.is_superuser or user.is_staff:      # IF THEY ARE SYSTEM ADMIN THE CAN SEE THE PROTOCOL
        return True

    try:
        membership = user.membership_set.get(org=protocol.owner)
        return True
    except ObjectDoesNotExist:
        pass
    
    return False




# def check_owner_edit_authorization(item, user):
#     '''
#     Checks the Authorization for a user to see if they can edit a given item based on the 
#     item's owner, if the user is a member of that organization and the role the user has.
#     '''

#     if user.is_superuser or user.is_staff:      # IF THEY ARE SYSTEM ADMIN THE CAN SEE THE PROTOCOL
#         return True

#     try:
#         membership = user.membership_set.get(pk=item.owner.pk)
#         if membership.role in ['a','w']:                                # ADMIN OR WRITE PERMISSIONS
#             return True
#     except ObjectDoesNotExist:
#        pass
    
#     return False


# def check_owner_view_authorization(protocol, user):
#     '''
#     Checks the Authorization for a user to see if they can view a given item based on the 
#     item's owner and if the user is a member of that organization.
#     '''

#     if user.is_superuser or user.is_staff:      # IF THEY ARE SYSTEM ADMIN THE CAN SEE THE PROTOCOL
#         return True

#     try:
#         membership = user.membership_set.get(pk=protocol.owner.pk)
#         return True
#     except ObjectDoesNotExist:
#        pass
    
#     return False


