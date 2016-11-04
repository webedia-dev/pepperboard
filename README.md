# Pepperboard

Pepperboard is a simple and modular dashboard toolkit for SaltStack. It also permits you to create your own dashboards.

For now, it needs to be run directly on the salt-master server

#### Index
1. [Installation](#installation)
2. [Usage](#usage)
3. [Dashboards](#dashboards)
4. [Development](#development)
5. [TODO](#todo)
6. [Licence and copyright](#licence-and-copyright)

# Installation
## Dependencies
  * Python modules :
    * futures
    * psutil
    * salt
    * pypandoc (only when built from source)
  * External tools :
    * pandoc (for pypandoc)
    * salt-master (needs to be run on the salt master)

## Installation
From the upstream repository :
```
pip install -e git+https://github.com/webedia-dev/pepperboard.git
```
From a copy of the upstream repository :
```
git clone https://github.com/webedia-dev/pepperboard.git
cd pepperboard
python setup.py install
```

# Usage
  * Simple list of available arguments :
    * --help|-h : Prints an awesome help message
    * --output=|-o : comma separated values of files to write dashboards given with the \"-d\" argument.
    * --dashboards=|-d : comma separated values of dashboards.
    * --threads=|-t : comma separated values of threads count to be used (must be greater than 0). Prefix the number by "f" if you want more threads than CPU cores count.
    * --grains=|-g : comma separated values of grains to be used with the mgrains dashboard. This argument implies "-d 'mgrains'".
    * --list|-l : List available dashboards.
  * List available dashboards :```pepperboard -l```
    * Example output :
    ```
    highstates
    upgrades
    mgrains
    ```
  * Generate 1 dashboard using default threads count : ```pepperboard -d 'upgrades' -o '/var/www/upgrades.html'```
  * -o and -d arguments are CSV list, if you want multiples dashboards, simply separate them using a comma :```pepperboard -d 'upgrades,highstates' -o '/var/www/upgrades.html,/var/www/highstates.html'```
    * In this example, the upgrades dashboard will be written in /var/www/upgrades.html and the highstates dashboard will be written in /var/www/highstates.html.
  * Optional arguments
    * --threads|-t : Specify thread count for dashboards (must be greater than 0), it's a list, the same as -o and -d arguments.
      * If you want to use more threads than CPU cores, add "f" before the thread count.
        * Example : "f32" will force the dashboard to be generated using 32 threads even though the CPU hasn't enough CPU cores.
    * --grains|-g : Specify the grains to be included in the mgrains dashboard.
      * Example : ```pepperboard -d 'upgrades,highstates,mgrains' -o '/var/www/upgrades.html,/var/www/highstates.html,/var/www/customgrains.html' -g 'manufacturer,productname,serialnumber'```
      * When this argument is specified we can omit "mgrains" in the dashboard list.

# Dashboards
  * upgrades : Displays a list of upgradable packages for each minion (equivalent to "salt '*' pkg.list_upgrades")
  * highstates : Displays a list of unsynchronised states for each minion (equivalent to "salt '*' state.highstate test=True)
  * mgrains : Displays a list of grains for each minion

# Development
  * Create a new dashboard : Simply add a new python script in the dashboard package
  * It needs to have one of these functions (in this priority order) :
    * gendata(input, nthreads) : Only returns a dictionnary containing these fields, the HTML and everything related to the dashboard design is not managed by this function :
      * Arguments :
        * input (mixed or None) : Can be one of the following
            * List of inputs to be used in the dashboard (like the grains list in mgrains dashboard)
            * None : Set it to None if you want to manage the input directly in the gendata function
        * nthreads (int or None) : Threads count for generating the dashboard
            * Can be set to None for either using the default thread count or not using threads at all.
      * It returns a dictionnary with the following keys (all mandatory)  :
        * ncol : Columns count for the dashboard (int type)
        * headers : List of headers (list type)
        * data : Dictionnary containing the content of the dashboard (dict type)
            * In case you have 1 data column (ncol == 2) :
                * This dictionnary only contains string type values.
            * In case you have more than 1 data column (ncol > 2) :
                * This dictionnary contains 1 dictionnary per table line with the key being the first column header.
    * gendash(output, nthreads) : Generates the complete dashboard.
      * Arguments :
        * output (str) : Absolute path of the output file.
        * nthreads (int or None) : Threads count for generating the dashboard
            * Can be set to None for either using the default thread count or not using threads at all.

# TODO
  * Add more "security" code to sanitize inputs and module loading.
  * Fix this README file and general documentation.
  * Upload it to Pypi.
  * Use pepper to use salt-api.
  * Get the OS logos from PNG/JPG files instead of having base64 directly in python code.
  * Make the dashboard list a little bit prettier.

# Licence and copyright


Copyright 2016 Cyril Lavier <cyril.lavier@webedia-group.com> - <cyril.lavier@davromaniak.eu>


Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.