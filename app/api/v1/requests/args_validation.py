"""
 SPDX-License-Identifier: BSD-4-Clause-Clear

 Copyright (c) 2018-2019 Qualcomm Technologies, Inc.

 All rights reserved.

 Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the
 limitations in the disclaimer below) provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this list of conditions and the following
   disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
   disclaimer in the documentation and/or other materials provided with the distribution.
 * All advertising materials mentioning features or use of this software, or any deployment of this software, or
   documentation accompanying any distribution of this software, must display the trademark/logo as per the details
   provided here: https://www.qualcomm.com/documents/dirbs-logo-and-brand-guidelines
 * Neither the name of Qualcomm Technologies, Inc. nor the names of its contributors may be used to endorse or promote
   products derived from this software without specific prior written permission.

 SPDX-License-Identifier: ZLIB-ACKNOWLEDGEMENT

 Copyright (c) 2018-2019 Qualcomm Technologies, Inc.

 This software is provided 'as-is', without any express or implied warranty. In no event will the authors be held liable
 for any damages arising from the use of this software.

 Permission is granted to anyone to use this software for any purpose, including commercial applications, and to alter
 it and redistribute it freely, subject to the following restrictions:

 * The origin of this software must not be misrepresented; you must not claim that you wrote the original software. If
   you use this software in a product, an acknowledgment is required by displaying the trademark/logo as per the details
   provided here: https://www.qualcomm.com/documents/dirbs-logo-and-brand-guidelines
 * Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.
 * This notice may not be removed or altered from any source distribution.

 NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY
 THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.                                                               #
"""

import re
from app import app, my_logger
from flask_babel import _


def validate_imei(imei):
    """Validate IMEI format."""
    my_logger.info('Validate IMEI format.')
    match = re.match('^[a-fA-F0-9]{14,16}$', imei)
    min_imei_length = app.config['system_config']['global'].get('min_imei_length')
    max_imei_length = app.config['system_config']['global'].get('max_imei_length')
    if len(imei) < min_imei_length:
        my_logger.info('Imei length too short.')
        raise ValueError(_("imei too short, should contain at least %(min)s characters", min=min_imei_length))
    if len(imei) > max_imei_length:
        my_logger.info('Imei length too long.')
        raise ValueError(_("imei too long, cannot contain more than %(max)s characters", max=max_imei_length))
    if match is None:
        my_logger.info('Imei is Invalid.')
        raise ValueError(_("invalid imei"))


def validate_msisdn(msisdn):
    """Validate MSISDN format."""
    my_logger.info('Validate MSISDN format.')
    match = re.match('^\+?[0-9]{7,15}$', msisdn)
    if match is None:
        my_logger.info('Msisdn match Invalid')
        raise ValueError(_("invalid msisdn"))
