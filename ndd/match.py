
class match:
    def __init__(self, matches=set([]), method=None):
        self.matches = set(matches)
        self.has_match = len(matches) > 0
        self.method = method
    
    def to_dict(self):
        return {
            "matches" : self.matches,
            "has_match" : self.has_match,
            "method" : self.method
        }