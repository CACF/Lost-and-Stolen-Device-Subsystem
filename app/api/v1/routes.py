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

from flask_restful import Api
from .resources.common import BaseRoutes
from .resources.admin import FetchImei, FetchMsisdn
from .resources.system import IncidentNature, CaseStatus
from .resources.case import CaseRoutes, CaseList, InsertCase, UpdateCase
from .resources.search import Search

# noinspection PyUnresolvedReferences
from .assets.error_handlers import *
from app.common.apidoc import ApiDocs
from app import app

api = Api(app, prefix='/api/v1', errors=CustomErrors)
apidoc = ApiDocs(app, app.config['system_config']['system']['version'])

# noinspection PyTypeChecker
api.add_resource(BaseRoutes, '/')
# noinspection PyTypeChecker
api.add_resource(FetchImei, '/imei/<imei>')
# noinspection PyTypeChecker
api.add_resource(FetchMsisdn, '/msisdn/<msisdn>')
# noinspection PyTypeChecker
api.add_resource(IncidentNature, '/incident_types')
# noinspection PyTypeChecker
api.add_resource(CaseStatus, '/status_types')
# noinspection PyTypeChecker
api.add_resource(CaseRoutes, '/case/<tracking_id>')
# noinspection PyTypeChecker
api.add_resource(InsertCase, '/case')
# noinspection PyTypeChecker
api.add_resource(UpdateCase, '/update_case/<tracking_id>')
# noinspection PyTypeChecker
api.add_resource(CaseList, '/cases')
# noinspection PyTypeChecker
api.add_resource(Search, '/search')

docs = apidoc.init_doc()


def register():
    """Method to register routes for docs."""
    for route in [BaseRoutes, FetchImei, FetchMsisdn, IncidentNature, CaseStatus, CaseList, Search,
                  CaseRoutes, InsertCase, UpdateCase]:
        docs.register(route)


register()
