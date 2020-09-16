#!/bin/bash


cd ../
pytest ./test_cases/openapi_cases -s -v -m openapi --config ./config/conf_test_hd2.json --data ./data/data_test.json

