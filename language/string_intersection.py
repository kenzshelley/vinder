from sets import Set
person1 = "interesting fishsim stuff yeah I don't know I think best American state"
person2 = 'critical functioning good animals know lions tigers bears 23 good animals know lions tigers bears 23'
person1 = Set(person1.split(' '))
person2 = Set(person2.split(' '))
intersection = person1 & person2
print intersection