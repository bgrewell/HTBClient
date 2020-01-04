# HTBClient
`HTBClient` is a python module that interfaces with the hackthebox.eu REST API. Since their API doesn't appear to be 
complete there are features that are currently missing such as challenges. These will be added once they have REST
endpoints but I have decided not to implement them now by scraping the site as I felt that would be too fragile and
would add a significant amount of throw away code.

## Overview Video

`insert youtube link here`

## Installation
There are several options for installation, i'll cover the common ones below. 

Installation of the latest version in PyPi via pip
```
python3 -m pip install htbclient
```

Installation of the latest version in the github repository
```
python3 -m pip install git+https://github.com/BGrewell/HTBClient
```

## Usage
`HTBClient` can be used as a stand-alone script or imported into your own project. An example of this is my `htb-repo` 
project which is a skeleton that I use to organize all the various challenges and boxes from hackthebox.eu. This repo 
works by having a basic folder layout to organize challenges and machines, then it uses the `HTBClient` to connect to 
the websites REST API and creates a folder for each machine that is found on the site but not on the file system, it 
also creates some metadata files and scripts to help with tracking and controlling the machines. To find out more about 
the `htb-repo` project click on [this link](https://github.com/BGrewell/htb-repo) to visit the repository.

#### Setting Username/Password
If you are using `HTBClient` as a module then you need to pass the username and password when you
create your instance. When using `HTBClient` as a module it is recommended that you get your username
and password from an environmental variable or some place other than hard-coding it in your source
that way if you source is shared you do not accidentally publish your credentials as well.

when running `htbclient.py` as a script you should set your credentials as environmental variables then
run the script as normal. 

Example
```
export HTB_USER=bob@somewebsite.net
export HTB_PASS=2jli9z9e2l34jlz98890@skx9!2a&
python3 htbclient.py <command> <arguments>
```

