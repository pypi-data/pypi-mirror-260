# BitEnumListField for Django Models
> [!WARNING]  
> This library is still work in progress. While it does work for case it was creaded for, it might not work in different contexts, please use at your own risk   

This field is used to store a list of enum values as a binary representation on a database.

### Example
First add the BitEnumListField to your model and choose the Enum it should use.
```python
class Weekdays(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

    
class Event(models.Model):
    name = TextField()
    days = BitEnumListField(Weekdays)
```
It require the Enum values to be integers.
At this point you can create new records just by setting the field to a list of enum values:
```python
my_event = Event(
    name="Event",
    days=[Weekdays.Tuesday, Weekdays.Friday]
)

my_event.save()
```
This will set the `days` field on the database to 18. That's because Weekdays.Tuesday correspond to the bitwise mask `0100000` which,
converted to decimal, gives us a `2` (digits are reversed when converting from binary to decimal, with hti swe don't have to worry about the length of the enumerator changing over time).
Now for Weekdays.Friday we have the mask `0000100` that converts to `16`. Now `0100000 | 0000100` equals `0100100` which converts to `18`   
At this point we can create, read, update and delete objects that use the BitEnumListField

## Querying the database

Using the standard match in a django query will only return us the elements that match exactly that list of enum values.   
If you want to create more complex queries this library introduces 3 lookups you can use.
### All Lookup
This lookup will return all elements that have all the specified enum values (and eventually more)
```python
Event.objects.filter(days__all=[Weekdays.Tuesday, Weekdays.Friday])
```
The example above will return all the events that have both tuesday and friday set as days.
### Any Lookup
This lookup will return all elements that have at least one of the specified enum values (and eventually more)
```python
Event.objects.filter(days__all=[Weekdays.Tuesday, Weekdays.Friday])
```
The example above will return all the events that have either tuesday or friday set as days. So for example it will return a day that has tuesday + wednesday.
### None Lookup
This lookup will return all elements that don't have any of the specified values.
```python
Event.objects.filter(days__nome=[Weekdays.Tuesday, Weekdays.Friday])
```
The example above will return all the events that have not tuesday nor friday set as days.

