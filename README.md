# Moved to https://bitbucket.org/jagguli/aioweb

# A Web Framework using pep-3156 async constructs.

 - templating: curently mustache, but can be overriden using custom renderers
 - database: couchdb, aim to make it usable with other nosql db.

## Setup:

to set up a dev env and install python dependencies you should be able to use buildout2 [https://pypi.python.org/pypi/zc.buildout/2.0.0]

    wget http://downloads.buildout.org/2/bootstrap.py
    python bootstrap.py
  
## Configuration:

 - copy default.ini in the conf dir and fillout to your needs, will default to values in default.ini

<pre>
[default]
hostname= # currently unused
staticroot=static
[couchdb]
username=couchuser
password=couchpassword
database=aiowebtest
</pre>


## Running:

There is a working example app in the src/supplementme which I'm trying to develop.
to run it 

    python3 bin/launch.py supplementme
 
The example app dependencies:
 - dojo [https://dojotoolkit.org/] 
 - jasmine [http://pivotal.github.io/jasmine/]

## Tests:
The tests are mostly up to date :)
  - find the tests along with the *.py files.

Any constructive criticism would be much appreciated. 
