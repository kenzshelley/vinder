from sets import Set
def string_intersection(string1, string2):
	string1 = Set(string1.split(' '))
	string2 = Set(string2.split(' '))
	return string1 & string2