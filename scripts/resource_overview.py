#!/usr/bin/python
# coding: utf-8
#############################
#
#    copyright 2018 Open Interconnect Consortium, Inc. All rights reserved.
#    Redistribution and use in source and binary forms, with or without modification,
#    are permitted provided that the following conditions are met:
#    1.  Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#    2.  Redistributions in binary form must reproduce the above copyright notice,
#        this list of conditions and the following disclaimer in the documentation and/or other materials provided
#        with the distribution.
#
#    THIS SOFTWARE IS PROVIDED BY THE OPEN INTERCONNECT CONSORTIUM, INC. "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE OR
#    WARRANTIES OF NON-INFRINGEMENT, ARE DISCLAIMED. IN NO EVENT SHALL THE OPEN INTERCONNECT CONSORTIUM, INC. OR
#    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#    OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
#    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#############################



import time 
import os    
import json
import random
import sys
import argparse
import traceback
from datetime import datetime
from time import gmtime, strftime
import jsonref
from os import listdir
from os.path import isfile, join
import json
import requests
from unidecode import unidecode



# mandatory resources that should not be in the list.
#file:  oic.wk.d.swagger.json
#file:  oic.wk.introspection.swagger.json
#file:  oic.wk.p.swagger.json
#file:  oic.wk.res.swagger.json

file_ignore_list = [ "oic.wk.res.swagger.json" , "oic.wk.d.swagger.json", "oic.wk.p.swagger.json", "oic.wk.introspection.swagger.json" , "BaseResourceSchemaResURI.swagger.json"]


def find_key_value(rec_dict, searchkey, target, depth=0):
    """
    find the first key with value "target" recursively
    also traverse lists (arrays, oneOf,..) but only returns the first occurance
    returns the dict that contains the search key.
    so the returned dict can be updated by dict[searchkey] = xxx
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param searchkey: target key to search for
    :param target: target value that belongs to key to search for
    :param depth: depth of the search (recursion)
    :return:
    """
    if isinstance(rec_dict, dict):
        # direct key
        for key, value in rec_dict.items():
            #if key == searchkey and value == target:
            if key == searchkey:
                return rec_dict
            elif isinstance(value, dict):
                r = find_key_value(value, searchkey, target, depth+1)
                if r is not None:
                    return r
            elif isinstance(value, list):
                for entry in value:
                    if isinstance(entry, dict):
                        r = find_key_value(entry, searchkey, target, depth+1)
                        if r is not None:
                            return r


def load_json(filename, my_dir=None):
    """
    load the JSON file
    :param filename: filename (with extension)
    :param my_dir: path to the file
    :return: json_dict
    """
    full_path = filename
    if my_dir is not None:
        full_path = os.path.join(my_dir, filename)
    if os.path.isfile(full_path) is False:
        print ("json file does not exist:", full_path)
    linestring = open(full_path, 'r').read()
    json_dict = json.loads(linestring)
    return json_dict

    
    
def write_json(filename, file_data): 
    """
    write the JSON  file
    :param filename: filename (with extension)
    :param file_data: json data to be written to file
    """ 
    fp = open(filename, "w")
    json_string = json.dumps(file_data, indent=2, sort_keys=True)
    fp.write(json_string)
    fp.close()
    
def get_dir_list(dir, ext=None):
    """
    get all files (none recursive) in the specified dir
    :param dir: path to the directory
    :param ext: filter on extension
    :return: list of files (only base_name)
    """
    only_files = [f for f in listdir(dir) if isfile(join(dir, f))]
    # remove .bak files
    new_list = [x for x in only_files if not x.endswith(".bak")]
    if ext is not None:
        cur_list = new_list
        new_list = [x for x in cur_list if x.endswith(ext)]
    return new_list
    

def get_rt(json_data):    
    paths = json_data["paths"]
    for pathname, pathobject in json_data["paths"].items():
        for methodname, methodobject in pathobject.items():
            if methodname in ["get"]:
                responses = methodobject["responses"]
                for responsename, responseobject in responses.items():
                    examples = responseobject["x-example"]
                    #print (examples)
                    if examples is not None:
                        if isinstance(examples, dict):
                            rt_value = examples.get("rt")
                            if rt_value is not None:
                                return examples
            else:
                examples = find_key_value(methodobject, "x-example", None)
                #print (examples)
                if examples is not None:
                    rt = find_key_value(examples, "rt", None)
                    if rt is not None:
                        return rt
                    
                    
                    

def get_title(json_data):    
    info = json_data["info"]
    if info is not None:
        return info["title"]

def process_dir(dir):
    my_array = []
    swag_files = get_dir_list(dir, ext=".swagger.json")
    for file in swag_files:
        print("file: ", file)
        if file in file_ignore_list:
            print("   ignored")
        else:
            json_data = load_json(file,dir)
            
            title = get_title(json_data)
            #print ("  title: ",title["title"])
            
            rt = get_rt(json_data)
            print ("  rt: ",rt["rt"])
            entry = {}
            entry["rt"] = rt["rt"]
            entry["title"] = title
            entry["filename"] = file
            my_array.append(entry)
    
    return my_array
                
        
    


    
#
#   main of script
#
print ("******************************")
print ("*** resource_overview (v1) ***")
print ("******************************")
parser = argparse.ArgumentParser()


parser.add_argument( "-append"     , "--append"    , help="append to file",  nargs='?', const="", required=False)
parser.add_argument( "-outputfile" , "--outputfile", help="json output file to be created",   nargs='?', const="")
parser.add_argument( "-indir" , "--indir", help="input directory",   nargs='?', const="")


args = parser.parse_args()

print("indir         : " + str(args.indir))
print("outputfile    : " + str(args.outputfile))

object_array = process_dir(args.indir)

if args.append is not None:
    print("appending")
    old_array = load_json(args.outputfile)
    object_array += old_array



write_json(args.outputfile, object_array)

    