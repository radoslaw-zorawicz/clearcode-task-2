# Task 2 - Traffic report

* module line_pattern_checker contains the class LinePatternChecker which allows to build a regular expression for preprocessing lines of a log.
* The regular expression captures named groups that may contain an ip address, datetime, url and http response code. 
* It checks if a read line violates the general structure of the format.
* Parser accepts only HTTP/1.1 prtocol.
* Captured ip address, datetime, url and http response code are validated in page_report module with python libraries.

### License
Copyright © 2018, [Radosław Żórawicz](https://github.com/radoslaw-zorawicz).