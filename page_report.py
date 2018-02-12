import re
from IPy import IP
from http import HTTPStatus
from enum import IntEnum
from urllib.parse import urlparse
import time


def build_ip_regex_group():
    ip_name_group="ip"
    ip_regex="(?P<{}>[^\[\s]*)\s".format(ip_name_group)
    return ip_regex

def build_datetime_regex_group():
    datetime_name_group = "datetime"
    datetime_regex = "\[(?P<{}>[^\[]*)\]\s".format(datetime_name_group)
    return datetime_regex

def build_address_http_request_regex_group():
    http_mehtods = "GET|HEAD|PUT|POST|DELETE|OPTIONS|TRACE|CONNECT|PATCH"
    address_name_group = "address"
    http_request_regex = "\"({})\s(?P<{}>\S+)\s+(HTTP/1.1)\"\s".format(http_mehtods, address_name_group)
    return http_request_regex

def build_response_code_regex_group():
    response_code_name_group="code"
    http_response_code_regex = "(?P<{}>\d\d\d)\s".format(response_code_name_group)
    return http_response_code_regex

def build_bytes_regex_group():
    bytes_name_group = "bytes"
    bytes_regex = "(?P<{}>\d+)".format(bytes_name_group)
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


def build_line_pattern(str):
    regex_string = "^"
    regex_string += build_ip_regex_group()
    regex_string += build_datetime_regex_group()
    regex_string += build_address_http_request_regex_group()
    regex_string += build_response_code_regex_group()
    regex_string = regex_string + build_bytes_regex_group() + "$"

    pattern = re.compile(regex_string)
    req = "10.4.180.222 [28/Jan/2018:10:02:32 +0100] \"GET http://clearcode.cc/ HTTP/1.1\" 200 1080"
    groups = [x.groupdict() for x in pattern.finditer(req)]