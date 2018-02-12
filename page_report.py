from line_pattern_checker import LinePatternChecker
import ipaddress
from http import HTTPStatus
from enum import IntEnum
from urllib.parse import urlparse
import time
import os
import sys


def get_stripped_url(url):
    '''
    Return stripped url
    :param str url: Url to strip
    '''
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Strip ending slash if needed:
    if path and path[len(path) - 1] == '/':
        path = path[:-1]
    # Make stripped url from net location
    # and path (may be empty):
    return parsed_url.netloc + path


def is_valid_http_code(code):
    '''
    Return True if 'code' is valid HTTP response code
    :param str code: Code to validate
    '''

    # Map all HTTP codes from endum list of integers
    int_http_response_codes = list(map(int, HTTPStatus))
    http_response_codes = list(map(str, int_http_response_codes))
    return code in http_response_codes


def is_valid_datetime(datetime):
    '''
    Return True if datetime has valid format 
    :param str datetime: Datetime to validate
    '''
    try:
        time.strptime(datetime, '%d/%b/%Y:%H:%M:%S %z')
    except ValueError:
        return False
    return True


def is_valid_ipv4_address(ip):
    '''
    Return True 'ip' is valid ip address
    :param str ip: Ip to validate
    '''
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    return True


def are_groups_valid(groups):
    '''
    Return True if regex groups captured from read line contain 
    valid url, ip, datetime and http response code.
    :param dict groups: Captured groups from read line
    '''
    if not groups:
        return False
    address = get_stripped_url(groups[LinePatternChecker.address_name_group])
    ip_valid = is_valid_ipv4_address(groups[LinePatternChecker.ip_name_group])
    datetime_valid = is_valid_datetime(
        groups[LinePatternChecker.datetime_name_group])
    http_code_valid = is_valid_http_code(
        groups[LinePatternChecker.response_code_name_group])
    if address and ip_valid and datetime_valid and http_code_valid:
        return True
    return False


def get_groups(pattern_iter):
    '''
    Return dictionary with groups and their names obtained
    from passed iterator
    :param iterator pattern_iter: Iterator over named regex groups
    '''
    groups = {}
    for item in pattern_iter:
        groups.update(item.groupdict())
    return groups

    '''
    Parse file
    '''


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
            if not are_groups_valid(groups):
                invalid_lines += 1
                continue
            address = get_stripped_url(
                groups[LinePatternChecker.address_name_group])
            if address in report:
                report[address] += 1
            else:
                report[address] = 1

    # Sort the report by the number of requests in descending order, and if two
    # URLs are requested equally often, they are sorted lexicographically
    sorted_report = sorted(report.items(), key=lambda x: (-x[1], x[0]))

    for key, value in sorted_report:
        sys.stdout.write("\"%s\",%d\n" % (key, report[key]))

    if invalid_lines != 0:
        sys.stderr.write("Invalid log lines: %s\n" % str(invalid_lines))


parse()
