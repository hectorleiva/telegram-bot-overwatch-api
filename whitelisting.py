#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Include and determines if user passed is whitelisted
import sys

whitelisted_chat_ids = [sys.argv[2]]

def determineWhiteListedUsers(chat_id):
    if chat_id in whitelisted_chat_ids:
        return True
    else:
        return False
