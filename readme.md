# Task 2 - Traffic report

* module line_patter_check contains the class LinePatternChecker which create a regular expressian that do preprocessing of a log line and capture named groups that may contain ip address, datetime, url and http response code. 
* The regular expression also check if read line does violage general structure of valid line:
<IPv4 address> [<datetime>] "<HTTP request>" <HTTP response code> <bytes sent>
* The regular expression accepts on HTTP/1.1 prtocol.
* Captured ip address, datetime, url and http response code are valide in page_report module using python libraries.

### License
Copyright © 2018, [Radosław Żórawicz](https://github.com/radoslaw-zorawicz).