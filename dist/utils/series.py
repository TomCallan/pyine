class Series:
    def __init__(self, l=[]):
        self.arr = l

    def __repr__(self): # return
        return f"{self.arr[-1]}"

    def __str__(self): # print        
        return f"{self.arr[-1]}"

    def __getitem__(self, item):
        item += 1
        if item <= len(self.arr):
            return self.arr[-item]
        else:
            raise IndexError(f"There are only {len(self.arr)} elements in the series")
