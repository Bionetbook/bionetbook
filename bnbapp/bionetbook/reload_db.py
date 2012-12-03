from django.contrib.auth.models import User
from protocols.models import Protocol	
user = User.objects.get(pk=1)
user.save()
def init_prot(ind, fname, user, Protocol):
	
	ind = Protocol()

	ind.data = ind.read_data(fname)
	ind.name = ind.data['Name']
	ind.owner = user
	ind.description = ind.data['Remarks']
	ind.save()
	return ind



	ind.protocol_input = ind.data['Input']
	ind.protocol_output = ind.data['Output']
	