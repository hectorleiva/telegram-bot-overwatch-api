#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Include and determines if user passed is whitelisted
import sys
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

whitelisted_chat_ids = [int(sys.argv[2])]
logger.info('the white listed ids: %s', whitelisted_chat_ids)

def determineWhiteListedUsers(chat_id):
    if chat_id in whitelisted_chat_ids:
        return True
    else:
        return False
