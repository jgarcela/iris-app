#!/bin/bash
nohup python3.11 -m web > web.log 2>&1 &
nohup python3.11 -m api > api.log 2>&1 &
