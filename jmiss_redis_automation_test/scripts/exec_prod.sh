#!/bin/bash


cd ../
pytest ./test_cases/openapi_cases -s -v -m openapi --config ./config/conf_hb.json --data ./data/instance_data_hb.json

