import json, requests, math, sys, bisect
from item import Item
from itemCount import ItemCount
useBuy = True

def optimal_sort(x):
    return x[1].icItem
def smallest_sort(x):
    return x[1].icItem.itemVol * -1
def value_sort(x):
    return x[1].icItem.itemVal
def value2_sort(x):
    return x[1].val()

def parse_evepraisal(url):
    rawdict=requests.get(url=url).json()
    mydict={}
    for thing in rawdict['items']:
        id = thing['typeID']
        it = Item()
        it.itemName = thing['name'].encode('utf-8')
        it.itemVol = thing['typeVolume']
        if it.itemVol == 0:
            it.itemVol = 0.000001
        it.itemVal = thing['prices']['buy' if useBuy else 'sell' ]['max']
        it.itemID = id
        if id in mydict:
            mydict[id].icCount += thing['quantity']
        else:
            mydict[id] = ItemCount(it, thing['quantity'])
    return mydict

def find_item_list(itemdict, cargo):
    outlist = []
    
    usedCargo = 0.0
    cargoVal = 0.0
    totalVal = 0.0
    for k, v in sorted(itemdict.iteritems(), key=optimal_sort, reverse=True):
        it = v.icItem
        count = v.icCount
        totalVal += it.itemVal * count
        if usedCargo + it.itemVol * count < cargo:
            cargoVal += it.itemVal * count
            usedCargo += it.itemVol * count
            outlist.append(ItemCount(it, count))
        elif it.itemVol <= cargo - usedCargo:
            remaining = cargo - usedCargo
            canfit = math.floor(remaining/it.itemVol)
            cargoVal += it.itemVal * canfit
            usedCargo += it.itemVol * canfit
            outlist.append(ItemCount(it, canfit))
        else:
            continue
    return outlist

def find_short_item_list(itemdict, cargo, maxitems=12):
    items = []
    usedCargo = 0.0
    for k, v in sorted(itemdict.iteritems(), key=optimal_sort, reverse=True):
        it = v.icItem
        usableCount = v.icCount
        if usedCargo + v.size() > cargo:
            if usedCargo + it.itemVol > cargo:
                continue
            usableCount = math.floor((cargo - usedCargo)/it.itemVol)
        if len(items) < maxitems:
            ic2 = ItemCount(it, usableCount)
            usedCargo += ic2.size()
            bisect.insort(items, ic2)
            continue

        #
        # If the current thing has higher value than the lowest value in the list,
        # then we'll replace the current lowest. Recalculate the number we can fit
        # with the lowest removed.
        #
        candidate = items[0]
        proposedCargo = usedCargo - candidate.size()
        if proposedCargo + v.size() < cargo:
            usableCount = v.icCount
        else:
            usableCount = math.floor((cargo - proposedCargo)/it.itemVol)
        newic = ItemCount(v.icItem, usableCount)
        usedCargo += newic.size()
        bisect.insort(items, newic)
        removed = items.pop(0)
        usedCargo -= removed.size()
    return items
