from functools import total_ordering

@total_ordering
class Item:
    itemName = ''
    itemVol = 0.0
    itemVal = 0.0
    itemID = 0

    def __str__(self):
        return "{} {} {:,.2f} {:,.2f}".format(self.itemID, self.itemName, self.itemVol, self.itemVal)
    def __eq__(self, other):
        return self.itemID == other.itemID and (self.itemVal / self.itemVol) == (other.itemVal / other.itemVol)
    def __lt__(self, other):
        myipv = 2**30 if self.itemVol == 0 else self.itemVal / self.itemVol
        if self.itemVol == 0:
            print self
        theiripv = 2**30 if self.itemVol == 0 else self.itemVal / self.itemVol
        if other.itemVol == 0:
            print other
        return myipv < theiripv or (myipv == theiripv and self.itemID == other.itemID)

