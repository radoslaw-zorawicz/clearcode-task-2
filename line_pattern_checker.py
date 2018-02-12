import re


class LinePatternChecker:

    # Names of regex capture groups:
    ip_name_group = "ip"
    datetime_name_group = "datetime"
    response_code_name_group = "code"
    address_name_group = "address"

    def build_pattern():
        '''
        Build regular expression that matches the format
        <IPv4 address> [<datetime>] "<HTTP request>"<HTTP response code> <bytes sent>
        The gegurar expression does not validate ip address, datetime, http request
        and response code.
        '''
        regex_string = "^"
        regex_string += LinePatternChecker.build_ip_regex_group()
        regex_string += LinePatternChecker.build_datetime_regex_group()
        regex_string += LinePatternChecker.build_address_http_request_regex_group()
        regex_string += LinePatternChecker.build_response_code_regex_group()
        regex_string = regex_string + LinePatternChecker.build_bytes_regex_group() + "$"

        pattern = re.compile(regex_string)
        return pattern

    def build_ip_regex_group():
        '''
        Return pattern of ip address capture group.
        '''
        # Capture all non whitespace charactres up to first space
        ip_regex = "(?P<{}>[^\[\s]*)\s".format(LinePatternChecker.ip_name_group)
        return ip_regex

    def build_datetime_regex_group():
        '''
        Return pattern of datetime address capture group.
        '''
        # Capture all charactres betweween square brackets followed by space
        datetime_regex = "\[(?P<{}>[^\[]*)\]\s".format(
            LinePatternChecker.datetime_name_group)
        return datetime_regex

    def build_address_http_request_regex_group():
        '''
        Return pattern of datetime HTTP request capture group.
        '''
        # Capture HTTP method name followed by any number of non whitespace charactres
        # one space and 'HTTP/1.1' string.
        http_mehtods = "GET|HEAD|PUT|POST|DELETE|OPTIONS|TRACE|CONNECT|PATCH"
        address_name_group = "address"
        http_request_regex = "\"({})\s(?P<{}>\S+)\s+(HTTP/1.1)\"\s".format(
            http_mehtods, LinePatternChecker.address_name_group)
        return http_request_regex

    def build_response_code_regex_group():
        '''
        Return pattern of HTTP response code capture group.
        '''
        # Capture any three digits followeb by a space
        http_response_code_regex = "(?P<{}>\d\d\d)\s".\
            format(LinePatternChecker.response_code_name_group)
        return http_response_code_regex

    def build_bytes_regex_group():
        '''
        Return pattern of number of bytes
        '''
        # Capture at least one digt number
        bytes_regex = "(\d+)"
        return bytes_regex
