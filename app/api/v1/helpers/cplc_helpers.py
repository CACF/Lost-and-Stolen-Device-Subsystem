"""
Copyright (c) 2018-2019 Qualcomm Technologies, Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the limitations in the disclaimer below) provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    Neither the name of Qualcomm Technologies, Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
    The origin of this software must not be misrepresented; you must not claim that you wrote the original software. If you use this software in a product, an acknowledgment is required by displaying the trademark/log as per the details provided here: https://www.qualcomm.com/documents/dirbs-logo-and-brand-guidelines
    Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.
    This notice may not be removed or altered from any source distribution.

NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                                                               #
"""

import os
from app import app
import pandas as pd
import uuid
import tempfile
from ..models.cplc import Cplc
from ..models.case import Case
from ..helpers.common_resources import CommonResources


class CplcCommonResources:
    """Common functionality used across the system."""
    @staticmethod
    def save_file(file):
        tempdir = tempfile.mkdtemp()
        filepath = os.path.join(tempdir, file.filename)
        file.save(filepath)
        return filepath

    @staticmethod
    def clean_data(data):
        data = pd.DataFrame(data)
        matched = data['imei'].str.match('^[a-fA-F0-9]{14,16}$')
        filtered_data = data[matched].T.to_dict().values()
        return filtered_data

    @staticmethod
    def block(filtered_data):
        failed_list = []
        success_list = []
        for data in filtered_data:
            flag = Case.find_data(data['imei'])
            if flag.get('flag') is not None:
                failed_list.append({"imei": data['imei'], "status": "Exists in LSDS"})
            else:
                subscribers = CommonResources.subscribers(data['imei'])
                if subscribers['subscribers']:
                    for subs in subscribers['subscribers']:
                        if subs['msisdn'] == data['msisdn']:
                            Cplc.create(data['imei'], data['msisdn'], 2)
                            success_list.append(data['imei'])
                        else:
                            failed_list.append({"imei": data['imei'], "status": "Data does not match"})
                else:
                    failed_list.append({"imei": data['imei'], "status": "Data does not match"})
        return failed_list, success_list

    @staticmethod
    def unblock(filtered_data):
        failed_list = []
        success_list = []
        for data in filtered_data:
            flag = Cplc.get_case(data['imei'])
            if flag and flag.get('status')!=1:
                failed_list.append({"imei": data['imei'], "status": "Already Exists and unblocked"})
            else:
                Cplc.update_status(data['imei'])
                success_list.append(data['imei'])
        return failed_list, success_list

    @staticmethod
    def generate_report(failed_list):
        """Return non compliant report for DVS bulk request."""
        try:
            if failed_list:
                complaint_report = pd.DataFrame(failed_list)
                report_name = 'cplc_failed_imeis' + str(uuid.uuid4()) + '.tsv'
                complaint_report.to_csv(os.path.join(app.config['dev_config']['UPLOADS']['report_dir'], report_name), sep= '\t')
            else:
                report_name = "report not generated."
            return report_name
        except Exception as e:
            app.logger.info("Error occurred while generating report.")
            app.logger.exception(e)
            raise e

    @staticmethod
    def process(file):
        data = CplcCommonResources.save_file(file)
        clean_data = CplcCommonResources.clean_data(data)
        failed_list, success_list = CplcCommonResources.block(clean_data)
        report = CplcCommonResources.generate_report(failed_list)
        return {
            "success": len(success_list),
            "failed": len(failed_list),
            "report_name": report
        }
