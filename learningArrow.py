import arrow

# Getting current time
currentDate = arrow.now()
print(currentDate)

# Search date in a string
print(arrow.get('June was born in May 1980', 'MMMM YYYY'))

# Creating a datetime
dateObj = arrow.get(1998, 11, 25)
print(dateObj)

# PROPERTIES
print('datetime:', currentDate.datetime)
print('naive: ', currentDate.naive)
print('tzinfo: ', currentDate.tzinfo)
print('ambiguous: ', currentDate.ambiguous)
print('float_timestamp: ', currentDate.float_timestamp)
print('int_timestamp: ', currentDate.int_timestamp)
print('imaginary: ', currentDate.imaginary)
print('Year:', currentDate.year, 'Month:', currentDate.month, 'Day:', currentDate.day)
print("Hour:", currentDate.hour)
print("Minute:", currentDate.minute)
print("Seconds:", currentDate.second)
print("Date:", currentDate.date())
print("Time:", currentDate.time())