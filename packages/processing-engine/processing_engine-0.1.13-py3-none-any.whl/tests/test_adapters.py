
from processing_engine.dda_models import *
from processing_engine.job_service import *
from processing_engine.processing_abstract import *
from processing_engine.processing_concrete import *
from processing_engine.adapters import *



import pytest
import json
import pprint

class TestAdapter:

    @pytest.fixture(scope='function')
    def job_service_salesforce(self):
        job_service = JobService(
            username="postgres",
            password="dDueller123araM=!",
            host="test-ddanalytics-rds-v2.cpcwi20k2qgg.us-east-1.rds.amazonaws.com",
            database="v1_2",
            organization_guid="0238bfa6-2a89-42fe-8a67-fde4c80391ea",
            connector_guid="4c374db5-8e37-428e-b988-92ce9879165a",
            processing_guid="65dc302d-d591-4634-a531-a5eae45e182b",
            integration_name="Salesforce",
            job_parameters={}
        )
        return job_service



    def test_adapts_salesforce(self, job_service_salesforce):
        salesforce_integration_adapter = SalesforceIntegrationAdapter()
        sample_events = json.load(open('tests/data/events_sf.json'))
        
        adapted_events: List[EventData] = salesforce_integration_adapter.adapt(sample_events, job_service_salesforce)

        print("=========== Adapted Event Sample from Salesforce ============")
        pprint.pprint(adapted_events[0].__dict__)

        assert adapted_events[0].user_id == 277
        assert adapted_events[0].local_timezone == "America/Los_Angeles"


    def test_adapts_windows(self, job_service_salesforce):
        windows_integration_adapter = WindowsIntegrationAdapter()
        sample_events = json.load(open('tests/data/events_windows.json'))

        adapted_events: List[EventData] = windows_integration_adapter.adapt(sample_events, job_service_salesforce)
        print("=========== Adapted Event Sample from Windows ============")
        pprint.pprint(adapted_events[0].__dict__)

    
