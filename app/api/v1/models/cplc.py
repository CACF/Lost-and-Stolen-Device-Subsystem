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

# noinspection PyProtectedMember
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy import or_, and_
from app import db
# noinspection PyUnresolvedReferences
from ..models.caseincidentdetails import CaseIncidentDetails
# noinspection PyUnresolvedReferences
from ..models.casepersonaldetails import CasePersonalDetails
# noinspection PyUnresolvedReferences
from ..models.devicedetails import DeviceDetails
# noinspection PyUnresolvedReferences
from ..models.deviceimei import DeviceImei
# noinspection PyUnresolvedReferences
from ..models.case import Case
from ..assets.response import CODES

class Cplc(db.Model):
    """Case database model"""
    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.String(20))
    msisdn = db.Column(db.String(20))
    status = db.Column(db.Integer, db.ForeignKey('status.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __init__(self, imei, msisdn, status):
        """Constructor."""
        self.imei = imei
        self.case_status = status
        self.msisdn = msisdn

    @property
    def serialize(self):
        """Serialize data."""
        return {
            "imei": self.imei,
            "msisdn": self.msisdn,
            "created_at": self.created_at,
            "status": self.status
            }

    # pass instrumented list object to get string value
    @staticmethod
    def __get_obj(instr_obj):
        """Return string value from instrumented list object."""
        try:
            if type(instr_obj) == InstrumentedList:
                return instr_obj[0]
            return None
        except Exception:
            raise Exception

    @staticmethod
    def find_data(imei):
        """Check if data already exists."""
        try:
            flag = db.session.query(DeviceImei).join(DeviceImei.devicedetails).join(DeviceDetails.case).\
                filter(and_(or_(Case.case_status == 3, Case.case_status == 2), DeviceImei.imei == imei)).first()
            if flag:
                return {'flag': flag, 'imei': imei}
            return {'flag': None, 'imei': None}
        except Exception:
            db.session.rollback()
            raise Exception

    @classmethod
    def create(cls, imei, msisdn, status):
        """Insert data into database."""
        try:
            flag = Case.find_data(imei)
            if flag.get('flag') is not None:
                return {"code": CODES.get('CONFLICT'), "data": flag.get('imei')}
            else:
                case = cls(imei, msisdn, status)
                db.session.add(case)
                db.session.commit()
                return {"code": CODES.get('OK'), "data": case.tracking_id}
        except Exception:
            db.session.rollback()
            raise Exception
        finally:
            db.session.close()
