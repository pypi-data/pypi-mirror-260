# Easy Console Table Package

A package to easily create a console table that can render this :
```
-------------------------
|   Hello   |   World   |
-------------------------
|     Hello |         1 |
| _________ | _________ |
|     World |         2 |
| _________ | _________ |
|           |         3 |
| _________ | _________ |
```

## How to use it ?

### Introduction code
Code to make the introduction table :
```py
from easy_console_table import Table


t = Table()
t.add_column("Hello", ["Hello", "World"])
t.add_column("World", [1, 2, 3])
print(t)
```

### Functionnalities

All methods refer to ``Table`` class.

#### Create a table
You need to create an object of ``Table`` that uses ``**kwargs`` parameters so you can configure table appearance.

Here's all you can configure : ``alignment=str, title_separator=str, column_separator=str, line_separator=str``.

Base settings are : ``"alignment": "right", "title_separator": "-", "column_separator": "|", "line_separator": "_"``

Even after creating the table you can configure it by using the method ``config`` which takes the same arguments.

#### Add and Delete a column
Add : method ``add_column`` that takes as parameters a column's name and a list of values.

Delete : methods ``Delete_column`` that takes as parameter a column's name in the table. If a column is delete, it gets removed in the filter.

#### Set and Get a column
Set : method ``set_column`` that takes as parameters a column's name and a list of values.

Get : method ``get_column`` that takes as parameter a column's name and return a list of values.

#### Get table
You can get the whole table implemented using dict of list by using method ``get_table``.

#### Perfect table
A perfect table is like a perfect graph. It's a table where all the columns have the same lenght.

Use the method ``get_is_perfect`` that returns a boolean to know if the table is perfect (True) or not (False).

#### Filter system
An attribute of ``Table`` is a ``filter``. It is a list that contains all the column's names that you don't want to show.

##### Filter methods
Add : method ``add_filter`` makes you add a column's name into the filter. It takes as parameter a column's name that must be in the table.

Remove : method ``remove_filter`` makes you remove an element of the filter, remove it by the column's name.

Clear : method ``clear_filter`` clear the whole filter.

#### Sort table
You can sort the whole table by following a column sorting. You can use it with the method ``sort_table_from_column`` that takes a column's name as parameter. Table have to be perfect to sort.

#### Export to CSV
You can export the table to a CSV file by using ``export_as_csv`` method that takes as parameter the file path or name. Columns filtered will not be exported.

### Mixed example
Code :
```py
from easy_console_table import Table


t = Table(alignment="center", title_separator="#", line_separator="-", column_separator="I")
t.add_column("Hello", ["World", "!", "Hello"])
t.add_column("Sort", [2, 3, 1])
t.add_column("trash", ["Dont", "Work", "As", "It", "Should"])

print(t)
print()

t.add_filter("trash")
print(t)
print()

t.delete_column("trash")
t.sort_table_from_column("Sort")
t.config(alignment="right", title_separator="-", line_separator="_", column_separator="|")
t.add_filter("Sort")
print(t)
```

It returns :
```
#####################################
I   Hello   I   Sort    I   trash   I
#####################################
I   World   I     2     I   Dont    I
I --------- I --------- I --------- I
I     !     I     3     I   Work    I
I --------- I --------- I --------- I
I   Hello   I     1     I    As     I
I --------- I --------- I --------- I
I           I           I    It     I
I --------- I --------- I --------- I
I           I           I  Should   I
I --------- I --------- I --------- I

#########################
I   Hello   I   Sort    I
#########################
I   World   I     2     I
I --------- I --------- I
I     !     I     3     I
I --------- I --------- I
I   Hello   I     1     I
I --------- I --------- I
I           I           I
I --------- I --------- I
I           I           I
I --------- I --------- I

-------------
|   Hello   |
-------------
|     Hello |
| _________ |
|     World |
| _________ |
|         ! |
| _________ |
```

## [Github link](https://github.com/flastar-fr/easy_console_table)