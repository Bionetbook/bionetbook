textverbs="""add
adjust
agitate
aliquot
apply
attach
call for protocol
centrifuge
check
chill
close
collect
combine
connect
cool
cover
cut
decant
digest
discard
drain
dry
electrophorese
elute
equilibrate
excise
extract
filter
grind
grow
harvest
heat
incubate
insert
invert
keep
let sit/stand
load
measure
melt
microcentrifuge
mix
open
pass
pcr
photograph
pipette out
place
pour
pour off
precipitate
prepare
purify
recover
remove
repeat
resuspend
rinse
seal
shake
spin
split
spool
stop
store
swirl
switch off
thaw
thermal cycle
transfer
visualize
vortex
wash
weigh
withdraw"""
    
form_template = """from verbs.baseforms import forms


class {verb_classtitle}(forms.VerbForm):

    name = "{verb_name}"
    slug = "{verb_slug}"

    duration_in_seconds = forms.IntegerField()
"""
def main():
    for verb in textverbs.splitlines():
        verb_classtitle = verb.title().replace(" ", "").replace("/","") + "Form"
        form = form_template.format(
            verb_classtitle = verb_classtitle,
            verb_name = verb,
            verb_slug = verb.replace(" ", "-").replace("/", "-")
        )
        verb_filename = verb.replace(" ", "_").replace("/","_")
        f = open(verb_filename + ".py", "w")
        f.write(form)
        f.close()
        print "from {verb_filename} import {verb_classtitle}".format(
            verb_filename=verb_filename,
            verb_classtitle=verb_classtitle
        )
    
if __name__ == "__main__":
    main()