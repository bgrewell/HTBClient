# HTBClient

## Usage

### Setting Username/Password
If you are using `HTBClient` as a module then you need to pass the username and password when you
create your instance. When using `HTBClient` as a module it is recommended that you get your username
and password from an environmental variable or some place other than hard-coding it in your source
that way if you source is shared you do not accidentally publish your credentials as well.

when running `htbclient.py` as a script you should set your credentials as environmental variables then
run the script as normal. 

Example
```
export HTB_USER=<username>
export HTB_PASS=<password>
python3 htbclient.py <command> <arguments>
```