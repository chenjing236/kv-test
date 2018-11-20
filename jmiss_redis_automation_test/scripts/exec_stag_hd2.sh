#!/bin/bash


cd ../
pytest ./test_cases/openapi_cases -s -v -m openapi --config ./config/conf_stage.json --data ./data/instance_data_stage.json