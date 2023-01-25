### Print HTML as PDF

[print_html_pdfs.py](print_html_pdfs.py) is a script for printing html pages as pdf from the command line.  
More usage instructions in the script itself.

**Requirements:** Chrome (application)

#### Installation:

1. Run:
```
pip3 install selenium webdriver_manager
brew install chromedriver
```

2. After successfully installing chromedriver, look for the installation location. it should say something like:
```
==> Linking Binary 'chromedriver' to '/opt/homebrew/bin/chrome
```

3. Navigate to chromedriver installation location:
```
cd /opt/homebrew/bin
# or possibly
cd /usr/local/bin
```

4. If you have a macbook, run:
```
xattr -cr chromedriver
```
(This will allow this mac to bypass restrictions on the downloaded executable.)


#### Reference:

  * printToPdf: https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-printToPDF
  * chromedriver printToPdf example: https://stackoverflow.com/questions/73675431/printing-a-pdf-with-selenium-chrome-driver-in-headless-mode
