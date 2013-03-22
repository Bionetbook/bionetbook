

# COMMON UNIT LISTS
CONCENTRATION_UNITS = (("ng/ul","nanogram / microliter"),("ug/ul","microgram / microliter"),("mg/ul","miligram / microliter"),("mg/ml","miligram / mililiter"),
	("mg/l","miligram / liter"), ("g/ml","gram / mililiter"), ("g/l","gram / liter"), ('nM', 'nanoMolar'), ('uM', 'microMolar'), ('mM', 'miliMolar'), ('M', 'Molar'), 
	('U/ul', 'Units / microliter'), ('X', 'Fold'), )
MASS_UNITS = (('ng', 'nanogram'),('ug', 'microgram'),('mg', 'miligram'),('g', 'gram'),('kg', 'kilogram'), ('U', 'Units'), )
VOLUME_UNITS = (("l","liter"),("ml","Mililiter"), ("ul","microliter"), )
AMMOUNT_UNITS = (('nm', 'nanomole'),('um', 'micromole'),('mm', 'milimole'),('m', 'mole'), )
TIME_UNITS = (("hrs","Hours"),("min","Minutes"),("sec","Seconds"),)
SPEED_UNITS = (("rpm","Revolutions Per Minutes"),("rcf","Relative Centrifugal Force"),)
TEMPERATURE_UNITS = (("c","Celsius"),("k","Kelvin"),("f","Ferinheit"),)
VESSELS = (('epi','1.8 ml tube'), ('pcr','200 ul tube'), ('15 ml','Falcon 15 ml'), ('50 ml', 'Falcon 50 ml'),)


def check_protocol_edit_authorization(protocol, user):

    if user.is_superuser or user.is_staff or protocol.owner.pk in [ org.pk for org in user.organization_set.all() ]:
        return True
    return False

		 
        
        
        
       