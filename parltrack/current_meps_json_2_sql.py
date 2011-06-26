#!/usr/bin/python
# -*- coding:Utf-8 -*-

import os
import sys
import json

sys.path += [os.path.abspath(os.path.split(__file__)[0])[:-len("parltrack")] + "apps/"]

from meps.models import MEP

current_meps = "meps.json"

def clean_existant_data(mep):
    print "   remove links with delegations"
    mep.delegationrole_set.all().delete()

def create_mep(mep_json):
    pass

def manage_mep(mep, mep_json):
    pass

if __name__ == "__main__":
    print "load json"
    #meps = json.load(open(current_meps, "r"))
    #new = 0
    #to_update = 0
    #for mep_json in meps["meps"]:
    mep_json = json.load(open("one_mep.json", "r"))
    in_db_mep = MEP.objects.filter(ep_id=mep_json["UserID"])
    if in_db_mep:
        mep = in_db_mep[0]
        clean_existant_data(mep)
    else:
        mep = create_mep(mep_json)
    manage_mep(mep, mep_json)
    #print "%i new meps, %i meps to update" % (new, to_update)

# TODO
# need to check all the existant building and to remove the empty one
# same for delegations and committees
# need to set all current mep to current = False before the importation
# also check in reps for emails and stuff like that to remove
# meps urls

# vim:set shiftwidth=4 tabstop=4 expandtab: