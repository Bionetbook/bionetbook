# Loading new protocols in to a database:
from organization.models import Organization
from django.contrib.auth.models import User
from protocols.models import Protocol	
org = Organization.objects.get(name='bionetbook')
user = User.objects.get(pk=1)
user.save()
def init_prot(ind, fname, user, Protocol):
	
	ind = Protocol()

	ind.data = ind.read_data(fname)
	ind.name = ind.data['Name']
	ind.owner = user
	ind.description = ind.data['Remarks']
	ind.duration_in_seconds = ind.get_duration()
	ind.save()
	return ind

def update_param(Protocol,i): 
	a = Protocol.objects.get(pk=i); 
	a.duration_in_seconds = a.get_duration('padding'); 
	a.save()





	ind.protocol_input = ind.data['Input']
	ind.protocol_output = ind.data['Output']
	


