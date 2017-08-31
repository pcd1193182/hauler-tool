# -*- encoding: utf-8 -*-
from esipy import App
from esipy import EsiClient
from esipy.exceptions import APIException
from collections import OrderedDict
import json
from item import Item
from itemCount import ItemCount

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
            fit_list[resp.data.name] += [(fit.name, json.dumps(fit)
                                              .replace(u'<', u'\\u003c')
                                              .replace(u'>', u'\\u003e')
                                              .replace(u'&', u'\\u0026')
                                              .replace(u"'", u'\\u0027'))]
        else:
            fit_list[resp.data.name] = [(fit.name, json.dumps(fit)
                                              .replace(u'<', u'\\u003c')
                                              .replace(u'>', u'\\u003e')
                                              .replace(u'&', u'\\u0026')
                                              .replace(u"'", u'\\u0027'))]
            
    
    return OrderedDict(sorted(fit_list.items(), key=lambda t: t[0]))
        
def add_to_cargo(fit, icList):
    for ic in icList:
        newitem = {'flag': 5}
        newitem['type_id'] = ic.icItem.itemID
        newitem['quantity'] = ic.icCount
        fit['items'].append(newitem)
    return fit

def rename_fit(fit, url):
    fit['name'] = fit['name'] + ' | ' + url.rsplit('/')[-1]
    return fit
