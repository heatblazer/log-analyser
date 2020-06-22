Statistics analyzer tool
========================

Tool for parsing logs from their specific format, and display thier statistics in `matplot` graph. 


How to build or contribute to project:
- Python 3 intepreter
- `pip install progress`
- `pip install matplot`
- requires `json` module
- requires `csv` module

Create a single exe:
- Use `pyinstaller App.py --onefile`

Usage: [TODO]
- see example how to generate a parser from `db_ver1.json`
- Run `App.exe` as a standalone in command line: `App.exe myjson.json` if no argument provided, app will use `db_ver1.json` assuming it's in the same dir.
- When `matplot` shows graphs, you can use the submenu, too slide forward or zoom specific parts of graphs.  

DSL from `json` file
====================
```
{
	"main-separator" : "PacketRouter Statistics:",
	"opt-separator": "====",
	"main-delimiter" : ":",
	"short-export" : false, 	
	"ui-mode" : false, 
	"path" : "C:\\SomerRootFolder",
		"group1": {			
			"name" : "Some Statistics:",
			"fields" : ["Some filter"] 
		},
		"group2" : {
			"mandatory" : false,
			"name" : "Provisioning statistics:",
			"fields" : ["Number of Something", "Number of Targets"]
		},
		"group3" : {
			"name" : "Power Statistics:",
			"fields" : ["powerful fileds"]
		},
		group-n : {
			"name" : "blabla",
			"fields" : ["list of blablas"]
		}
}
```

- `main-separator` - `string` if not set to anything `PacketRouter Statistics:` will be set by default for frame cut.
- `opt-separator` - `string` if not set to anything `====` will be used to `strstr()` at least `=` counts to cut off duplicated sub-frames
- `main-delimiter` : `char` or `string` if not set `:` will be used to split desired lines.
- `ui-mode` - `true` or `false` enable \ disable plotter or CSV exporter. 
- `short-export` - `true` or `false` it will export a minimal report for only one entry per `PacketRouter Statistics:` frame
- `path` - folder  logs (up to 18)
- `group` - parser to be generated dynamically. 
- `name` - Group of statistics to be matched 
- `fields` - sub fields from specific group to match (ex. `NUmber of valid packets...`)
- `mandatory` - `true` or `false` it will mark a specific group items to be mandatory or not [TODO]
[TODO]: add more info 

Limitations:
============
~~- Parsing does not support duplicated fields per `Packet Router Statistics` context. Ex. Plugins won't be resolved.~~ 
- `ui-mode` does not support more than 18 subplots, adding more will break the UI layouts and hampers visualisations.

Run:
====
Download form Bin\Win32 `App.exe` and `db_ver1.json` and double clikc on it to verify all is working.

Example view:
==
![](Figure_1.png)


csv file example output:
========================
![](Capture2.PNG)


Notes:
- Please ignore `App.exe` warning ` MATPLOTLIBDATA environment variable was deprecated in Matplotlib 3.1 and will be removed in 3.3.` it's python's stuff not relevant to the application. 

[TODO: @oksana: add more to readme]
