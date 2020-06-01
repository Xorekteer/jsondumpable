import json

class JSONDumpable():
    """
    Superclass for JSON Dumpable objects.
    Keeps a list of all instances and some useful 
    functions for serialization.

    Interface:
    cls.var_str_list {list of strings}  
        -- Set of variables to be dumped
            -- SUBCLASS VARIABLE: Set in subclass before running
            -- no default, error if not set
    cls.quickload_var_str_list
        -- Set of variables to be loaded w/o special methods
            -- SUBCLASS VARIABLE: Set in subclass before running
                -- no default
                -- optional
            -- Use only for simple types, use special methods for others
                -- e.g.: write a Datetime using strftime and load w/ strptime
    cls.dump_file 
        -- Filename of file to be dumpled
            -- SUBCLASS VARIABLE: Set in subclass before running
    cls.dump_to_json_file()
        -- Dump file
    """
    
    # Initialize list w/ current jobs
    current_jobs = []
    
    # Class variable list of strings
    var_str_list=None
    quickload_var_str_list=None
    quickload_is_subset=None    #None if quickload_var_str_list and var_str_list haven't been compared yet
                                #True otherwise
                                #Never False: we'll throw an error if the comparison fails

    # Dump file name
    dump_file = "classdump.json"

    def __init__(self, current_jobs=None):
        """ Default init."""
        self.storage_dict = list()
        
        self.__class__.current_jobs.append(self)  #add new object to list of objects  
        # Check passing by reference
        if id(self) != id(self.__class__.current_jobs[-1]):
            raise Exception("Scheduler instance passed to list of Scheduler instances by copying instead of referencing.")



    # Create dumpale JSON dict for a single object
    def __create_json_dict(self):
        self.storage_dict = dict()
        for var_str in self.__class__.var_str_list:     # ignore this error, it's intended
            exec("self.storage_dict['" + var_str + "'] = self." + var_str)



    @classmethod
    def __get_dumpable_list(cls):
        cls.cls_jsonlist = list()    # list to hold all objects
        for job in cls.current_jobs:    
            job.__create_json_dict()                    # create dict for object variables
            cls.cls_jsonlist.append(job.storage_dict)   # append job to list
        return cls.cls_jsonlist



    @classmethod
    def dump_to_json_file(cls):
        """ Write all current Repeater jobs to a repfile.json """
        with open(cls.dump_file, "w") as file:
            json.dump(cls.__get_dumpable_list(), file, indent=2)



    @classmethod
    def quickload_vars(cls, new_obj, obj_in_json):
        # Error checking: quicload_var_str_list has to be a subset of var_str_list
        if cls.quickload_is_subset == None:     # never been checked
            for q_var in cls.quickload_var_str_list:
                if q_var not in cls.var_str_list:
                    raise ValueError(
                        "quickload_var_str-list is not a subset of var_str_list\n" + 
                        "tried to load a variable not in the JSON dump")
            cls.quickload_is_subset = True      # passed check
        # Now quickload into new_obj:
        for quickload_var in cls.quickload_var_str_list:
            exec("new_obj." + quickload_var + " = obj_in_json['"+ quickload_var +"']")


         



def test():
    inst = JSONDumpable()       #make instance
    inst.var1 = 15              #some variable
    inst.var2 = 'foo'           #some variable
    JSONDumpable.var_str_list = ['var1', 'var2']
    JSONDumpable.quickload_var_str_list = ['var1', 'var2']
    JSONDumpable.dump_to_json_file()
    del inst                        #get rid of instance
    JSONDumpable.current_jobs = []  #reset current jobs (idk I think it would happen anyway)
    # Reload instance and print variables
    # Shows that quickload works
    with open(JSONDumpable.dump_file, 'r') as dump:
        objs = json.load(dump)
        for obj in objs:
            new_obj = JSONDumpable()
            JSONDumpable.quickload_vars(new_obj, obj)
    print(JSONDumpable.current_jobs)
    print(JSONDumpable.current_jobs[0].var1)
    print(JSONDumpable.current_jobs[0].var2)
    




if __name__ == "__main__":
    test()