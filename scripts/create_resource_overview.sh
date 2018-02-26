#!/bin/bash
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
#
# usage
# sh create_resource_overview.sh 
#  This script generates:
#  - ../oic.resourcemap-content.json
#  this is the overview of resource types and their description that can be generated from swagger files in github repos.
#  currently supported github repo: IoTDataModels


#git clone https://github.com/openconnectivityfoundation/core.git  --branch master
#git clone https://github.com/openconnectivityfoundation/core.git  --branch master
git clone https://github.com/OpenInterConnect/IoTDataModels.git --branch master


python3 resource_overview.py --outputfile ../oic.resourcemap-content.json --indir IoTDataModels 
#python3 resource_overview.py --outputfile ../oic.resourcemap-content.json --indir core/swagger2.0 -append
#python3 resource_overview.py --outputfile ../oic.resourcemap-content.json --indir core-extensions/swagger2.0 -append

rm -rf IoTDataModels
rm -rf core
rm -rf core-extensions