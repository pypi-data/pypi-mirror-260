import re
import logging
from typing import List
from processing_engine.dda_models import EventData, Event, Timeslot
from processing_engine.job_service import JobService
from processing_engine.class_helpers import Utils
from processing_engine.processing_abstract import IntegrationDataAdapter, ConnectorBasedIntegrationAdapter, IdentitiesBasedIntegrationAdapter


class PGEngineIntegrationAdapter(IntegrationDataAdapter):
    """
    Adapts the data from the Postgres database to a Pandas dataframe.
    Joins the pandas with correct organization.user data.
    """
    integration_name = "PGEngine"

    def retrieveOrganizationData(jobService: JobService) -> dict:
        """Returns the organization Data required for the required joint fields for having a dataframe.
        """
        # Retrieves in the following format:
        cursor = jobService.cursor
        # cursor.execute
        return {}


    def adapt(self, event_datas: List[dict], jobService: JobService) -> List[dict]:
        
        return []

class WindowsIntegrationAdapter(ConnectorBasedIntegrationAdapter):
    """
    Adapts the data from the Windows raw json to a List of EventData.
    Uses the Job Service to log errors and messages.

    Updates in interactions were updated to accomodate the following:
     
    "interactions": [ {"date":"2023-11-10T09:00“,"key": 42,"mouse":22},
    {"date":"2023-11-10T09:01“,"key": 18,"mouse":20},
    {"date":"2023-11-10T09:04“,"key": 2,"mouse":0}
    ]
    """

    integration_name = "Windows"
    

    def adapt(self, event_datas: List[dict], jobService: JobService) -> List[EventData]:
        # Fetch first the the organization data
        organization_data = self.retrieveOrganizationData(jobService)
        adapted_events = []

        # Join the data with the each event data provided
        for event_raw in event_datas:
            collected_timestamp = Utils.parseDate(Utils.NoneSafe(event_raw, 'event_date'))
            # Get the dayminuteformat
            end_time = Utils.NoneSafe(event_raw, 'event_end_date')
            unique_minutestamp = Utils.datetimeToYearMonthDayMinute(collected_timestamp)


            # We use the endtime instead to categorize our clicks. Since between shared events they share timestamps.
            if end_time is not None:
                end_time = Utils.parseDate(end_time)
                unique_minutestamp = Utils.datetimeToYearMonthDayMinute(collected_timestamp)


            interactions = Utils.NoneSafe(event_raw, "interactions")
            """
            "interactions": [ {"date":"2023-11-10T09:00“,"key": 42,"mouse":22},
                        {"date":"2023-11-10T09:01“,"key": 18,"mouse":20},
                        {"date":"2023-11-10T09:04“,"key": 2,"mouse":0}
                    ]
            """
            mouse_clicks = {}
            keystrokes = {}
            if interactions is not None:
                for interaction in interactions:
                    unique_minutestamp = interaction['date']
                    if 'mouse' in interaction:
                        # {unique_minutestamp: interaction['mouse']}
                        mouse_clicks[unique_minutestamp] = interaction['mouse']                    
                    if 'key' in interaction:
                        # {unique_minutestamp: interaction['key']}
                        keystrokes[unique_minutestamp] = interaction['key']
                        


            event_data = EventData(
                event_guid = Utils.NoneSafe(event_raw, 'guid'),
                processing_guid=jobService.processing_guid,
                user_id = organization_data['user_id'],
                organization_guid = jobService.organization_guid,
                organization_id = organization_data['organization_id'], # FAIL IF KEY NOT PRESENT
                integration_name = self.integration_name,

                application= Utils.NoneSafe(event_raw, "name"),
                app = Utils.NoneSafe(event_raw, "window_title"),
                app_type = None,
                operation =  Utils.NoneSafe(event_raw, "activity"),
                operation_type = None,
                staging_detail_guid = Utils.NoneSafe(event_raw, "guid"),
                local_timezone=organization_data['timezone'],
                
                timestamp = collected_timestamp,
                end_time = Utils.NoneSafe(event_raw, 'event_end_date'),
                timestamp_local = None,

                end_time_local=None,
                duration=None,

                description = Utils.NoneSafe(event_raw, 'description'),
                url = None,
                site=None,
                files = None,
                file_count=None,
                action_type="ACTIVITY", # By default all the actions are active for salesforce platform.
                geolocation=None,
                ipv4=None,
                local_ipv4=None,
                size=None,
                # Generated
                email_subject=None,
                from_address=None,
                to_address=None,
                email_cc = None,
                email_bcc = None,
                email_imid = None,
                phone_result=None,
                
                record_url=None,
                recording_url=None,
                record_id=None,

                tags=None,

                mouse_clicks=mouse_clicks,
                keystrokes=keystrokes,
            )

            event_data = self.checkConsistency(event_data, jobService)
            if event_data is not None and event_data is not False and event_data is not {}:
                adapted_events.append(event_data)

        return adapted_events

class SalesforceIntegrationAdapter(IdentitiesBasedIntegrationAdapter):
    """
    Adapts the data from the Salesforce raw json to a Pandas dataframe.
    """

    integration_name = "Salesforce"


    def adapt(self, event_datas: List[dict], jobService: JobService) -> List[EventData]:
        # Fetch first the the organization data
        organization_data = self.retrieveOrganizationData(jobService)
        adapted_events = []


        # Join the data with the each event data provided
        for event_raw in event_datas:
            # Convert them to EventDataFormat
            user_key_salesforce = Utils.NoneSafe(event_raw, 'Actor__c')
            if user_key_salesforce is None or user_key_salesforce not in organization_data:
                jobService.addLogMessage(
                    log_message=f"Organization data does not contain the user key {user_key_salesforce} ",
                    log_detail=f"Organization data: user key {user_key_salesforce} {organization_data} - Event data: {event_raw} for {self.integration_name} adapter",
                    log_type='Alert'
                )
                continue # Should not fail the entire block.
            
            
            tags_str = Utils.NoneSafe(event_raw, "Tags__c")
            tags_list = tags_str.split(";") if tags_str is not None else None
            
            event_data = EventData(
                event_guid = Utils.NoneSafe(event_raw, 'Id'),
                processing_guid=jobService.processing_guid,
                user_id = organization_data[user_key_salesforce]['user_id'],
                organization_guid = jobService.organization_guid,
                organization_id = organization_data['organization_id'], # FAIL IF KEY NOT PRESENT
                integration_name = self.integration_name,

                application= self.integration_name.upper(),
                app = None,
                app_type = None,
                operation =  Utils.NoneSafe(event_raw, 'Activity__c'),
                operation_type = None,
                staging_detail_guid = Utils.NoneSafe(event_raw, 'Id'),
                local_timezone=organization_data[user_key_salesforce]['timezone'],
                
                timestamp = Utils.parseDate(Utils.NoneSafe(event_raw, 'ActionDate__c')),
                end_time = None, # Not present in the Salesforce Platform Integration
                timestamp_local = None,

                end_time_local=None,
                duration=Utils.NoneSafe(event_raw, 'Duration__c'),

                description = Utils.NoneSafe(event_raw, 'Description__c'),
                url = Utils.NoneSafe(event_raw, 'URL__c'),
                site=None,
                files = None,
                file_count=None,
                action_type="ACTIVITY", # By default all the actions are active for salesforce platform.
                geolocation=None,
                ipv4=None,
                local_ipv4=None,
                size=None,
                # Generated
                email_subject=Utils.NoneSafe(event_raw, "Subject__c"),
                from_address=Utils.NoneSafe(event_raw, "From__c"),
                to_address=Utils.NoneSafe(event_raw, "To__c"),
                email_cc = Utils.NoneSafe(event_raw, "CC__c"),
                email_bcc = Utils.NoneSafe(event_raw, "BCC__c"),
                email_imid = Utils.NoneSafe(event_raw, "MessageId__c"),
                phone_result=None,
                
                record_url=Utils.NoneSafe(event_raw, "Record_Link__c"),
                recording_url=Utils.NoneSafe(event_raw, "RecordId__c"),
                record_id=Utils.NoneSafe(event_raw, "RecordId__c"),

                tags=tags_list,

                mouse_clicks=None,
                keystrokes=None,
            )

            event_data = self.checkConsistency(event_data, jobService)
            if event_data is None or event_data is False or event_data == {}:
                continue
            adapted_events.append(event_data)

        return adapted_events

class EmailIntegrationAdapter(IdentitiesBasedIntegrationAdapter):
    """
    Adapts the data from the Email raw json to a Pandas dataframe.
    """

    integration_name = "Email"
    

    def adapt(self, event_datas: List[dict], jobService: JobService) -> List[EventData]:

        # Fetch first the the organization data
        organization_data = self.retrieveOrganizationData(jobService)
        adapted_events = []

        # Join the data with the each event data provided
        for event_raw in event_datas:
            # Convert them to EventDataFormat
            eventdata = self.extract_email_data(event_raw)
            from_address = Utils.NoneSafe(eventdata, "from")
            
            if from_address is None or from_address not in organization_data:
                jobService.addLogMessage(
                    log_message=f"Organization data does not contain the user key {from_address} ",
                    log_detail=f"Organization data: user key {from_address} {organization_data} - Event data: {event_raw} for {self.integration_name} adapter",
                    log_type='Error'
                )
                return None
            
            
            event_data = EventData(
                event_guid = Utils.NoneSafe(eventdata, 'messageId'),
                processing_guid=jobService.processing_guid,
                user_id = organization_data[from_address]['user_id'],
                organization_guid = jobService.organization_guid,
                organization_id = organization_data['organization_id'], # FAIL IF KEY NOT PRESENT
                integration_name = self.integration_name,

                application= self.integration_name.upper(),
                app = Utils.NoneSafe(eventdata, "Object__c"),
                app_type = None,
                operation =  'SEND',
                operation_type = None,
                staging_detail_guid = Utils.NoneSafe(eventdata, 'guid'),
                local_timezone=organization_data[from_address]['timezone'],
                
                timestamp = Utils.parseDate(Utils.NoneSafe(eventdata, 'timestamp')),
                end_time = Utils.parseDate(Utils.NoneSafe(eventdata, 'timestamp')),
                timestamp_local = None,

                end_time_local=None,
                duration=None,

                description = None,
                url = None,
                site=None,
                files = None,
                file_count=None,
                action_type="ACTIVITY", # By default all the actions are active for Email platform.
                geolocation=None,
                ipv4=None,
                local_ipv4=None,
                size=None,
                # Generated
                email_subject=Utils.NoneSafe(eventdata, "subject"),
                from_address=Utils.NoneSafe(eventdata, "from"),
                to_address=Utils.NoneSafe(eventdata, "to"),
                email_cc = Utils.NoneSafe(eventdata, "cc"),
                email_bcc = Utils.NoneSafe(eventdata, "bcc"),
                email_imid = Utils.NoneSafe(eventdata, "message_id"),
                phone_result=None,
                
                record_url=None,
                recording_url=None,
                record_id=None,

                tags=[],

                mouse_clicks=None,
                keystrokes=None,
            )

            event_data = self.checkConsistency(event_data, jobService)
            if event_data is not None and event_data is not False and event_data is not {}:
                adapted_events.append(event_data)

        return adapted_events
    
    
    def extract_emails(self, input_string, update_connector_flag = True, getJustOne = False):
            email_pattern = r'\"([^<>,\s^"]+@[^<>,\s]+(?:\s*,\s*[^<>,\s]+@[^<>,\s^"]+)*)"|([^<>,\s^"]+@[^<>,\s]+(?:\s*,\s*[^<>,\s]+@[^<>,\s^"]+)*)'

            # Find all matches using the regex pattern
            matches = re.findall(email_pattern, input_string)
            
            # Extract the first group if it exists, otherwise use the second group
            cleaned_matches = [match[0] if match[0] else match[1] for match in matches]
            
            cleaned_matches = list(set(cleaned_matches))
            
            if getJustOne:
                cleaned_matches = cleaned_matches[0]

            return cleaned_matches

    def extract_email_data(self, input_dict):
        # Extract data from the dictionary structure
        timestamp = input_dict['ses']['mail']['timestamp']
        source = input_dict['ses']['mail']['source']
        messageId = input_dict['ses']['mail']['messageId']
        destination = input_dict['ses']['mail']['destination']
        headers = input_dict['ses']['mail']['headers']

        # Initialize data fields
        date = ""
        from_email = ""
        to = ""
        cc = ""
        subject = ""
        message_id = ""

        # Extract data from headers
        for header in headers:
            name = header['name']
            value = header['value']
            if name == "Date":
                date = value
            elif name == "From":
                from_email = self.extract_emails(value, getJustOne=True)
            elif name == "To":
                to = self.extract_emails(value)
            elif name == "CC":
                cc = self.extract_emails(value)
            elif name == "Subject":
                subject = value
            elif name == "Message-ID":
                message_id = value

        # Create a dictionary to store the extracted data
        extracted_data = {
            "timestamp": timestamp,
            "source": source,
            "messageId": messageId,
            "destination": destination,
            "date": date,
            "from": from_email,
            "to": to,
            "cc": cc,
            "subject": subject,
            "message_id": message_id
        }

        return extracted_data

class ChromeIntegrationAdapter(ConnectorBasedIntegrationAdapter):

    integration_name = "Chrome"

    def adapt(self, event_datas: List[dict], jobService: JobService):
        

        organization_data = self.retrieveOrganizationData(jobService)
        adapted_events = []

        

        def aggregateFileSizes(files):
            
            if(files is None):
                return 0
            
            total_size = 0
            for file in files:
                total_size += Utils.NoneSafe(file, "size", 0)
            return total_size
        
        def eventActiveStatus(event):
            """Determines if the event ACTIVITY Status for Chrome Extension if the type it will return ACTIVE unless the event type is idle
            Passive if it is download or upload

            Args:
                event (str): Event  should contain type key.

            Returns:
                str: ACTIVE | IDLE | PASSIVE
            """
            # if the type is idle, then it is IDLE
            event_type = Utils.NoneSafe(event, "type")

            if(event_type == "idle"): return "IDLE"
            if(event_type == "download"): return "PASSIVE"
            if(event_type == "upload"): return "PASSIVE"
            return "ACTIVE"
            
        def getSumFeats(dictObject, field, *args):
            """
            Get the sum of numeric values for the specified keys from the dictionary.
            """
            total = 0
            check_dict = Utils.NoneSafe(dictObject, field)
            if check_dict is None:
                return 0
            

            for key in args:
                value = check_dict.get(key)
                if isinstance(value, (int, float)):
                    total += value
            return total

        for event_raw in event_datas:
            files = Utils.NoneSafe(event_raw, "files")
            collected_date = Utils.parseDate(Utils.NoneSafe(event_raw, 'timestamp'))
            unique_minutestamp = Utils.datetimeToYearMonthDayMinute(collected_date)

            end_time = Utils.parseDate(Utils.NoneSafe(event_raw, 'endTime'))
            if end_time is not None:
                unique_minutestamp = Utils.datetimeToYearMonthDayMinute(end_time)
            

            event_data = EventData(
                event_guid = Utils.NoneSafe(event_raw, 'guid'),
                processing_guid=jobService.processing_guid,
                user_id = organization_data['user_id'],
                organization_guid = jobService.organization_guid,
                organization_id = organization_data['organization_id'], # FAIL IF KEY NOT PRESENT
                integration_name = self.integration_name,

                application= "Chrome",
                app = Utils.NoneSafe(event_raw, "domain"),
                app_type = None,
                operation =  Utils.NoneSafe(event_raw, "type"),
                operation_type = None,
                staging_detail_guid = Utils.NoneSafe(event_raw, "guid"),
                local_timezone=organization_data['timezone'],

                timestamp = collected_date,
                end_time=end_time,
                timestamp_local = None,
                end_time_local=None,
                duration=None,
                description=None,
                url=Utils.NoneSafe(event_raw, 'url'),
                site=Utils.NoneSafe(event_raw, 'domain'),
                files = files,
                file_count= len(files) if files is not None else 0,
                action_type=eventActiveStatus(event_raw),
                geolocation=None,
                ipv4=None,
                local_ipv4=None,
                size=aggregateFileSizes(files),

                email_subject=None,
                from_address=None,
                to_address=None,
                email_cc = None,
                email_bcc = None,
                email_imid = None,
                phone_result=None,

                record_url=None,
                recording_url=None,
                record_id=None,

                tags=None,

                mouse_clicks={
                    unique_minutestamp: getSumFeats(event_raw, "interactions", "auxclick", "click", "dblclick", "mousedown", "mouseup", "mouseover", "mouseout", "contextmenu")},
                keystrokes={
                    unique_minutestamp: getSumFeats(event_raw, "interactions", "keyboard")},
            )

            event_data = self.checkConsistency(event_data, jobService)
            if event_data is not None and event_data is not False and event_data is not {}:
                adapted_events.append(event_data)

        return adapted_events










