#######################################################################################################################
#                                                                                                                     #
# Copyright (c) 2018 Qualcomm Technologies, Inc.                                                                      #
#                                                                                                                     #
# All rights reserved.                                                                                                #
#                                                                                                                     #
# Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the      #
# limitations in the disclaimer below) provided that the following conditions are met:                                #
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following  #
#   disclaimer.                                                                                                       #
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the         #
#   following disclaimer in the documentation and/or other materials provided with the distribution.                  #
# * Neither the name of Qualcomm Technologies, Inc. nor the names of its contributors may be used to endorse or       #
#   promote products derived from this software without specific prior written permission.                            #
# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED  #
# BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED #
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT      #
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR   #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE,      #
# DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,      #
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,   #
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                                                                  #
#                                                                                                                     #
#######################################################################################################################

import json
from flask import Response
from app import app
from .response import CODES, MESSAGES, MIME_TYPES


# custom base 404 error handler
# noinspection PyUnusedLocal
@app.errorhandler(CODES.get('NOT_FOUND'))
def not_found_handler(error):
    """handles 404 error"""
    data = {
        'message': MESSAGES.get('RESOURCE_NOT_FOUND')
    }

    response = Response(json.dumps(data), status=CODES.get('NOT_FOUND'),
                        mimetype=MIME_TYPES.get('APPLICATION_JSON'))
    return response


# flask-restful custom errors
CustomErrors = {
    'MethodNotAllowed': {
        'message': 'method not allowed',
        'status': 405,
    }
}
