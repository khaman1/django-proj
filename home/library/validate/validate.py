import re

class Validate:
    def isString(self, string):
        return True if re.match('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', string) else False
    
    def isEmail(self, string):
        return True if re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', string) else False
    
    def isPhoneNumber(self, string):
        return True if re.match('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', string) else False