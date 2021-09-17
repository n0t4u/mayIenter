# May I enter?

May I enter is an automatic tool written in Python 3 that performs authorization checks based on user cookies or authorization headers.

### ¡Still in development!

## Installation
Simple installation, simple usage
```sh
$ git clone https://github.com/n0t4u/mayIenter.git
$ cd mayIenter
$ python3 -m pip install -r requirements.txt
$ chmod +x mayIenter.py
```
## Usage
Use the tool [DRAFMe.py](https://github.com/n0t4u/DRAFMe), or another spider, to crawl all the routes of the domain you are auditing.
Export the results in a file and filter them by the domain you want to check (grep "example.com").
Run mayIenter.

```sh
$ python3 mayIenter.py #Interative menu

$ python3 mayIenter.py -d "User1:Cookie1,User2:Cookie2" -f "path/to/file" #Command line
```

## TO DO
Add Auth header support
Support undefined number of users, not just 2 + anon

## Author 
n0t4u

## License
GNU General Public License Version 3

## Disclaimer
This tool is only purposed for Ethical Hacking audits. The author is not responsible for any use by third parties.