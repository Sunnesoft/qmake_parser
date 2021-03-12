#Copy sources from qmake \*.pro (\*.pri) 
___

#Abstract
Script provides copy files from Qt project directory, which structure 
pointed in qmake *.pro or *.pri file in SOURCES and HEADERS fields.

#Launch
```shell
cd /your/path/to/main.py/   
python3 main.py
```

#Configure
For configure script please change *config.json*. Here is example:
```json
{
  //Input path
    "in_path": "./test/test_pro/", 
  //Output path
    "out_path": "./test/out/", 
  //Single file for parsing
    "pro": "test_pro.pro", 
  //Set tockens (key of obj) wich will be replaced by string (value of obj)
    "vars": {"$$PWD/": ""}, 
  //It's option allow include and exclude `contains`-blocks to processing,
  //If you set "CONFIG":"SECOND", that will be processed only 
  // contains(CONFIG,SECOND){...} section;
  //If you set "CONFIG":"SECOND FIRST", that will be processed 
  // previous and contains(CONFIG,FIRST){...} section;
    "cfg": {"CONFIG": "SECOND FIRST"}
}
```

#Note
This source use regular expressions for parse project file. It's a bad 
practice. But it's the simplest way to decide this local task. 
Script recursively processed blocks but it not processed unary 
conditions and chains of conditions. For example,
```text
contains(CONFIG, ONE) {
    contains(CONFIG, TWO){
        ...
    }
    
    contains(CONFIG, FREE){
        ...
    }
    ...
}

contains(CONFIG, TWO){
    ...
}
```
will processed correctly if you want to parse all TWO sections. If you want
to parse only TWO sections which are in ONE section script returns incorrect
result.