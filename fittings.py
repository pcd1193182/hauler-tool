# -*- encoding: utf-8 -*-
from esipy import App
from esipy import EsiClient
from esipy.exceptions import APIException
from collections import OrderedDict

def process_resp(esiapp, esiclient, resp):
    assert (resp.status == 200)
    fit_list = {}
    for fit in resp.data:
        
        op = esiapp.op['get_universe_types_type_id'](
            type_id=fit.ship_type_id
        )
        resp = esiclient.request(op)
        if resp.status != 200:
            raise APIException('', resp.status, resp.data)
        if resp.data.name in fit_list:
            fit_list[resp.data.name] += fit
        else:
            fit_list = [fit]
    
    return OrderedDict(sorted(ship_list.items(), key=lambda t: t[0]))
        
