#!/usr/bin/env python

from zope.interface import implements

from twisted.python.usage import Options
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application.internet import TCPServer
from twisted.application.service import MultiService
from twisted.web.resource import Resource
from twisted.web.server import Site

from dumbserver import expectations as Expectations
from dumbserver import arguments as Arguments
from dumbserver.constants import QUERY_SEPARATOR as query_separator
from dumbserver.constants import QUERY_DELIMITER as query_delimiter
from dumbserver.constants import HEADER_SEPARATOR as header_separator
from dumbserver.constants import HEADER_DELIMITER as header_delimiter
from dumbserver.constants import EXP_STATUS_CODE, EXP_HEADERS, EXP_BODY

configurations = []
expectations = None
    
def convertToString(dictionary, separator, delimiter):
    stringValue = ""
    if dictionary:
        for key in dictionary:
            values = dictionary.get(key)
            if isinstance(values,list):
                for value in values:
                    stringValue += key + separator + value + delimiter
            else:
                stringValue += key + separator + values + delimiter
        stringValue = stringValue[:-1]
    return stringValue
    
def deserializeRequest(request):
    port, method, path = str(request.getHost().port), request.method, request.path
    query = convertToString(request.args, query_separator, query_delimiter)
    headers = convertToString(request.getAllHeaders(), header_separator, header_delimiter)
    body = request.content.getvalue()
    
    return Expectations.Request(port, method, path, query, headers, body)
    
class DumbServerResource(Resource):
    def __init__(self):
        Resource.__init__(self)
    
    def getChild(self, name, request):
        return DumbServerResource()
        
    def render(self, request):
        global expectations
        generic_request = deserializeRequest(request)
        generic_response = {}
        try:
            generic_response = Expectations.getResponseFromExpectations(expectations, generic_request)
        except ValueError, e:
            generic_response[EXP_STATUS_CODE] = 404
            generic_response[EXP_BODY] = str(e)
        
        if EXP_STATUS_CODE in generic_response:
            request.setResponseCode(generic_response[EXP_STATUS_CODE])
        
        if EXP_HEADERS in generic_response:
            headers = generic_response[EXP_HEADERS]
            for header in headers.split(header_delimiter):
                key, value = header.split(header_separator)
                request.setHeader(key, value)
        
        if EXP_BODY in generic_response:
            return generic_response[EXP_BODY]
        
        return str(generic_response)

class Options(Options):
    optParameters = [
        ["configfile", "f", None, "The configuration file containing the list of expectation files and corresponding port numbers to which it should run."],
        ["expectations", "e", None, "Comma separated list of expectation files and corresponding port numbers to which it should run."],
    ]

class DumbserverMultiService(MultiService):
    def __init__(self):
        MultiService.__init__(self)
    
    def startService(self):
        global configurations, expectations
        print "Loaded configurations: " + str(configurations)
        Expectations.display(expectations)
        MultiService.startService(self)
    
class DumbserverServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "dumbserver"
    description = "Mock several REST services in one go!"
    options = Options

    def makeService(self, options):
        global configurations, expectations
        configurations = Arguments.parseArguments(options["configfile"],options["expectations"])
        ports = Arguments.getAllPortsFromConfig(configurations)
        expectations = Expectations.constructExpectationTreeFromConfig(configurations)
        
        site = Site(DumbServerResource())
        service = DumbserverMultiService()
        for port in ports:
            TCPServer(port, site).setServiceParent(service)
        return service

dumbserverService = DumbserverServiceMaker()