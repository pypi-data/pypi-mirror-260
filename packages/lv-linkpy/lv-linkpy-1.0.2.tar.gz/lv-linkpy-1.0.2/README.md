lv-linkpy
===================================
a python interface to remote LabVIEW controls.
<br>
Python version above 3.6 is required.

![](banner.jpg)


This package depends on Pykit for LabVIEW, a LabVIEW addon.
For more information, please see
[Pykit for LabVIEW documentation](https://www.zdiao.xyz/pykit-doc/).

## Installation

* `pip install lv-linkpy`


## Register the control on LabVIEW

## Usage

### Create a session

```python
from lvlinkpy import Session
s = Session(1919)
```

### Check control references 

```python
s.print_control_info()
```
This code will print all control references outline which are registered on LabVIEW. 

### Get control value

User can get the value from the name of the control.
Suppose there is a control called "Boolean" in the LabVIEW.
```python
print(s.get_value("Boolean"))
```

If the control name is incorrectly given, it will raise an error.
```python
s.get_value("fdzggZWSdgs")
```


### Set control value

User can set the value by the name of the control.
Suppose there is a control called "Boolean" in the LabVIEW, 
this code will set the control value to "True".
```python
s.set_value(valueName="Boolean", value=True)
```

This package will perform type check before send to LabVIEW.
So, If user send a string to a bool control, it will raise an error.

However, `ignore_check=True` can avoid type check on python. 
It may lead an error on LabVIEW.
```python
s.set_value(valueName="Boolean", value="string")
s.set_value(valueName="Boolean", value="string", ignore_check=True)
```

`mechaction=True` argument can activate mechanical actions of the control.
(for example firing an event case)

```python
s.set_value(valueName="Boolean", value=True, mechaction=True)
```

Notice that, a button-like latch action is not supported. 
If you want to activate an event case of a button, 
you can add a hidden boolean to the target event case structure on LabVIEW.