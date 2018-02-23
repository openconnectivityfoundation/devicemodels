#!/usr/bin/env bash



#git clone https://github.com/openconnectivityfoundation/core.git  --branch master
#git clone https://github.com/openconnectivityfoundation/core.git  --branch master
#git clone https://github.com/OpenInterConnect/IoTDataModels.git --branch master


python3 resource_overview.py --outputfile ../oic.resourcemap-content.json --indir core/swagger2.0
python3 resource_overview.py --outputfile ../oic.resourcemap-content.json --indir core-extensions/swagger2.0 -append
python3 resource_overview.py --outputfile ../oic.resourcemap-content.json --indir IoTDataModels -append