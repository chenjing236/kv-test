#!/bin/bash

for((i=0;i<5;i++))
do
	sh ./mongo_smoke_test_cases &
done
exit 0
