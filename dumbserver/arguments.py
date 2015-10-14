#!/usr/bin/env python

import os

def getPathForFile(filename):
    if not os.path.isabs(filename):
        return os.path.join(os.getcwd(), filename)
    else:
        return filename

def getFileNameFromConfig(config):
    return config.split(":")[0]
    
def getPortNumberFromConfig(config):
    splitted_line = config.split(":")
    if len(splitted_line) < 2:
        return "80"
    else:
        return splitted_line[1]

def sanitizeConfig(config):
    filename, port = getPathForFile(getFileNameFromConfig(config)), getPortNumberFromConfig(config)
    return filename+":"+port
    
def parseArguments(configfile, expectations):
    if not configfile and not expectations:
        raise ValueError("No expectations specified. Run 'twistd dumbserver --help' for more info about specifying expectations.")
    
    config = []
    if configfile:
        configfile = getPathForFile(configfile)
        with open(configfile, "r") as file_contents:
            config_from_file = ",".join(file_contents.read().split())
        config.extend(config_from_file.split(","))
    
    if expectations:
        if expectations[len(expectations)-1] == ",":
            expectations = expectations[:-1]
        config.extend(expectations.split(","))
            
    return map(sanitizeConfig, config)

def getAllPortsFromConfig(configurations):
    return [int(getPortNumberFromConfig(entry)) for entry in configurations]