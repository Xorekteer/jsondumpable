# JSONDUMPABLE  -- A superclass for easy object serialization

## What it does
With this library you can easily save/reload all instances of a class.

## Use
1. Import `jsondumpable.py` in your own python file.
2. Create your class and use JSONDumpable as a parent.
3. Remeber to use `super.init()` (or some equivalent) in your subclass.

Now you have the following available in your class `cls`. Set each of these to the appropriate values.
* `cls.dumpfile` - name of the JSON file
* `cls.var_str_list` - list with the names of the variables that you wish to save
    * eg.: if you have `self.name` and `self.age` in your class that you wish to save, set `var_str_list = ["name", "age"]` 
* `cls.quickload_var_str_list` - set like `cls.var_str_list`, but this one will handle loading.
* If you have variables that require special parsing (eg. a Datetime), convert first, pass the converted into `cls.var_str_list`, and parse back after loading.

Finally you can dump using `cls.dump_to_json_file()`.
For loading, use something like this (with `cls` being your class):
```
with open(cls.dump_file, 'r') as dump:
        objs = json.load(dump)
        for obj in objs:
            new_obj = cls()
            cls.quickload_vars(new_obj, obj)
            # other (special) loading methods here
print(cls.current_jobs)             # should contain all loaded instances of the class
```

This last example is also at the end of the source `jsondumpable.py`. Enjoy.

## Tech info
* Uses `exec()` to convert from string to source-code for the variable names.
* Linting might suggest some errors as `var_str_list` and `quickload_var_str_list` are by default None in the base class. Ignore this: the base class is not intended to be used w/o subclassing/further config.