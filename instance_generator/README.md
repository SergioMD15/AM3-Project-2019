# AMMMCourseProjectIG

Instance Generator for the course project of AMMM.


## How to run

The instance generator works with Python3 and takes as an input the configuration file with the maximum and minimum values for the different variables of the problem. You can tune this values in the file inside `config/sample_config.dat` (parameters in the file from first to third don't need to be changed). To execute it you can use the following command:

```
python3 Main.py config/sample_config.dat
```

If the values introduced in the config file are not valid for any reason (e.g. a maxValue lower than a maxValue of the associated variable) an error will be raised. Otherwise, a sample data file will be generated into the Instances folder so you can use it to run either the CPLEX project or the metaheuristics one.