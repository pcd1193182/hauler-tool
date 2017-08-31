from functools import total_ordering
from item import Item
@total_ordering
class ItemCount:
    icItem = Item()
    icCount = 0

    def __init__(self, it, count):
        icItem = it
        icCount = count
        
    def __eq__(self, other):
        return self.icItem == other.icItem and self.icCount == other.icCount
    def __lt__(self, other):
        return self.val() < other.val() or ((self.val() == other.val()) and self.icItem.itemID == other.icItem.itemID)

    def val(self):
        return self.icItem.itemVal * self.icCount
    def size(self):
        return self.icItem.itemVol * self.icCount
    def __str__(self):
        return str(self.icCount) + " of " + str(self.icItem)
