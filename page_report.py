import re
import ipaddress
from http import HTTPStatus
from enum import IntEnum
from urllib.parse import urlparse
import time

class LinePatternChecker:

    ip_name_group = "ip"
    datetime_name_group = "datetime"
    response_code_name_group = "code"
    address_name_group = "address"


    def build_pattern():
        regex_string = "^"
        regex_string += LinePatternChecker.build_ip_regex_group()
        regex_string += LinePatternChecker.build_datetime_regex_group()
        regex_string += LinePatternChecker.build_address_http_request_regex_group()
        regex_string += LinePatternChecker.build_response_code_regex_group()
        regex_string = regex_string + LinePatternChecker.build_bytes_regex_group() + "$"
        
        pattern = re.compile(regex_string)
        return pattern

    def build_ip_regex_group():
        ip_regex="(?P<{}>[^\[\s]*)\s".format(LinePatternChecker.ip_name_group)
        return ip_regex

    def build_datetime_regex_group():
        datetime_regex = "\[(?P<{}>[^\[]*)\]\s".format(LinePatternChecker.datetime_name_group)
        return datetime_regex

    def build_address_http_request_regex_group():
        http_mehtods = "GET|HEAD|PUT|POST|DELETE|OPTIONS|TRACE|CONNECT|PATCH"
        address_name_group = "address"
        http_request_regex = "\"({})\s(?P<{}>\S+)\s+(HTTP/1.1)\"\s".format(http_mehtods, LinePatternChecker.address_name_group)
        return http_request_regex

    def build_response_code_regex_group():
        http_response_code_regex = "(?P<{}>\d\d\d)\s".format(LinePatternChecker.response_code_name_group)
        return http_response_code_regex

    def build_bytes_regex_group():
        bytes_regex = "(\d+)"
        return bytes_regex

def get_address(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def is_valid_http_code(code):
    int_http_response_codes = list(map(int, HTTPStatus))
    http_response_codes = list(map(str, int_http_response_codes))
    return code in http_response_codes

def is_valid_datetime(datetime):
    try:
        time.strptime(datetime,'%d/%b/%Y:%H:%M:%S %z')
    except ValueError:
        return False
    return True

def is_valid_ipv4_address(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    return True

def parse():
    pattern = LinePatternChecker.build_pattern()
    requests = ["10.4.180.222 [28/Jan/2018:10:02:32 +0100] \"GET http://clearcode.cc/ HTTP/1.1\" 200 1080"]
    groups = [x.groupdict() for x in pattern.finditer(requests[0])]
    print(groups)