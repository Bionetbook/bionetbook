# Protocol Scheduling 
# version 0.1
# Author: Oren Schaedel
# Date 10/03/2012

# Writing a single .ics file with a summary, and start date and end date
# install google api client library - succesful
# install oauth 2.0 through google api - fail



import sys
from icalendar import Event, Calendar, vDatetime
from datetime import datetime, timedelta as td
import pytz
# import vobject
from protocolutils import Protocol

filename = sys.argv[1]
start_date = sys.argv[2]
in_args = sys.argv
target_protocol = Protocol('YAML files' + '/' + filename)

# Format Start date:
start_date = vDatetime.from_ical(start_date)

# format time delta:
if 'padding' in sys.argv:
	protocol_duration = target_protocol.get_duration('padding')
else:
	protocol_duration = target_protocol.get_duration()
if protocol_duration >= 86400: # longer than a day
	total_time = divmod(protocol_duration,86400)
	delta = td(total_time[0], total_time[1])
else:
	delta = td(0, protocol_duration)	

# Set calendar
cal = Calendar()
cal.add('prodid', '-//Apple Inc.//Mac OS X 10.8.2//EN')
cal.add('version', '2.0')
cal.add('X-WR-CALNAME', 'Work')
cal.add('X-APPLE-CALENDAR-COLOR', '#44A703')
cal.add('X-WR-TIMEZONE', 'America/Fortaleza')
cal.add('method', 'publish')

# Set event:
event = Event()
event.add('summary', target_protocol.Name)
event.add('dtstart', start_date) # Change to 'US/Pacific-New'
event.add('dtend', start_date + delta)
event.add('priority', 5)
cal.add_component(event)
fname_out= filename[:filename.index('.')] + '.ics'
f = open(fname_out, 'wb')
f.write(cal.to_ical())
f.close()

#set decorator calendars:

pad = Calendar()
cal.add('prodid', '-//Apple Inc.//Mac OS X 10.8.2//EN')
cal.add('version', '2.0')
cal.add('X-WR-CALNAME', 'Work')
cal.add('X-APPLE-CALENDAR-COLOR', '#89c75f')
cal.add('X-WR-TIMEZONE', 'America/Fortaleza')
cal.add('method', 'publish')

padding = Event()
event.add('summary', 'heating the sample')
event.add('dtstart', start_date + delta) # Change to 'US/Pacific-New'
event.add('dtend', start_date + delta + td(0,3600*4))
event.add('priority', 5)
padding.add_component(event)
fname_out= filename[:filename.index('.')] + '_pad1.ics'
f = open(fname_out, 'wb')
f.write(cal.to_ical())
f.close()



# cal2 = Calendar.from_ical(open('work1.ics','rb').read())

# to do:
# Create a protocol type event - a multiple event object
# Draw out the function over several hours including spacing
# Include active and passive times
# Find events on calendar
# Identify conflicts
# Identify down times
