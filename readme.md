# Task 2 - Traffic report

* module line_patter_check contains the class LinePatternChecker which creates a regular expression for preprocessing of a log line and capturing named groups that may contain an ip address, datetime, url and http response code. 
* The regular expression checks if read line violates the general structure of the valid line.
* The regular expression accepts only HTTP/1.1 prtocol.
* Captured ip address, datetime, url and http response code are validated in page_report module using python libraries.

### License
Copyright © 2018, [Radosław Żórawicz](https://github.com/radoslaw-zorawicz).