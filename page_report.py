import re
import ipaddress
from http import HTTPStatus
from enum import IntEnum
from urllib.parse import urlparse
import time
import os
import sys

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
    path = parsed_url.path
    if path and path[len(path) - 1] == '/':
        path = path[:-1]
    return parsed_url.netloc + path

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

def line_valid(groups):
    if not groups:
        return False
    address = get_address(groups[LinePatternChecker.address_name_group])
    ip_valid =  is_valid_ipv4_address(groups[LinePatternChecker.ip_name_group])
    datetime_valid = is_valid_datetime(groups[LinePatternChecker.datetime_name_group])
    http_code_valid = is_valid_http_code(groups[LinePatternChecker.response_code_name_group])
    if address and ip_valid and datetime_valid and http_code_valid:
        return True
    return False

def get_groups(pattern_iter):
    groups = {}
    for item in pattern_iter:
        groups.update(item.groupdict())
    return groups

def parse():
    if len(sys.argv) != 2:
        sys.stderr.write("Missing file name\n")
        return
    filename = sys.argv[1]
    pattern = LinePatternChecker.build_pattern()
    
    invalid_lines = 0
    report = {}
    with open(filename) as log:
        for line in log:
            groups = get_groups(pattern.finditer(line))
            if not line_valid(groups):
                invalid_lines += 1
                continue
            address = get_address(groups[LinePatternChecker.address_name_group])
            if address in report:
                report[address] += 1
            else:
                report[address] = 1

    sorted_report = sorted(report.items(), key=lambda x: (-x[1], x[0]))
    
    for key, value in sorted_report:
        sys.stdout.write("\"%s\",%d\n"%(key,report[key]))

    if invalid_lines != 0:
        sys.stderr.write("Invalid log lines: %s\n"%str(invalid_lines))

parse()