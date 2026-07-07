#!/bin/bash
nohup python3.11 -m web > ../logs/web.log 2>&1 &
nohup python3.11 -m api > ../logs/api.log 2>&1 &
