# xaled-selenium-collection
Collection of selenium automation scripts and helper functions.

## requirements:
- Python3
- Xvbf:  `sudo apt-get install xvfb`
- selenium, pyquery pyvirtualdisplay mitmproxy: `$ sudo pip3 install selenium, pyquery pyvirtualdisplay mitmproxy`
- kutils: `$ sudo pip3 install git+https://github.com/xaled/kutils`
- chromedriver (from https://sites.google.com/a/chromium.org/chromedriver/downloads)
- geckodriver (from https://github.com/mozilla/geckodriver/releases)

## Scripts:
### Aliexpress:
- help : `$ ./aliexpress.py --help`
- example : `$ ./aliexpress.py --headless -u example@email.com -p PaSsWoRd --verbose --protection`

### Chaabinet (bpnet.gbp.ma):
- help : `$ ./chaabinet.py --help`
- example : `$ ./chaabinet.py --headless -u 300000 -p PaSsWoRd`