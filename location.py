# the Location class holds all data for each location the player can go to
# if you're wondering how i know about classes and objects and stuff it's because i took a java class in highschool and am just generally interested in coding
class Location: # learned Python class syntax from the docs
    # class constructor
    def __init__(self):
        self.name = ""
        self.desc = ""
        self.items = []
        self.can_go_array = []


# builder for the location class to deal with all the paragraphs of shit we have
# after implementing this i realized i was overthinking it and i don't actually need a builder, but i'm gonna leave it in because it already works
class LocationBuilder:
    def __init__(self):
        self.location = Location()


    def set_name(self, name):
        self.location.name = name


    def set_desc(self, desc):
        self.location.desc = desc


    def set_items(self, items):
        self.location.items = items


    def set_can_go(self, can_go_array):
        self.location.can_go_array = can_go_array


    def build(self):
        return self.location
