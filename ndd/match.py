
class match:
    def __init__(self, matches=set([]), method=None):
        self.matches = set(matches)
        self.has_match = len(matches) > 0
        self.method = method
