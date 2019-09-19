from elasticsearch import Elasticsearch
from datetime import datetime

es=Elasticsearch([{'host':'localhost','port':9200}])


class ElasticSearchResource:

    @staticmethod
    def insert_doc(document, tracking_id, status):
        new_doc = {
            "device_details": document['device_details'],
            "incident_details": document['incident_details'],
            "get_blocked": document['case_details']['get_blocked'],
            "updated_at": datetime.now(),
            "created_at": datetime.now(),
            "personal_details": document['personal_details'],
            "tracking_id": tracking_id,
            "creator": document['loggedin_user'],
            "status": status
        }
        es.index(index='lsds', id=new_doc['tracking_id'], body=new_doc)
        return None

    @staticmethod
    def get_doc(tracking_id):
        res = es.get(index='lsds', id=tracking_id)
        return res

    @staticmethod
    def update_doc(tracking_id, doc_to_update):
        es.update(index='lsds', id=tracking_id, doc_type="_doc", body=doc_to_update)
        return None

    # @staticmethod
    # def search_doc(doc_to_search):


""" Testing """

ElasticSearchResource.update_doc("IamID123", {"doc": {"personal_details": {"gin" : "1234567880", "address" : "N/A",
                                                                           "dob" : "2000-09-07", "number" : "N/A",
                                                                           "full_name" : "test user", "email" : "N/A"}}})
print(ElasticSearchResource.get_doc("IamID123"))


