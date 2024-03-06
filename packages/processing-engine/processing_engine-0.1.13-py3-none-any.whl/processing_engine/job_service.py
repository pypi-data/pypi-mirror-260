from typing import List
import psycopg2

import logging
import psycopg2.extras
from processing_engine.dda_models import LogMessage
from processing_engine.class_helpers import Utils

class JobService():
    """
    Tracks errors and log Messages, single instance of connection requirements, passed around. Gets reset and instantiated by the Enhancement Manager each time a new event is processed.
    To keep track of:
    - DBengine: DBengine to be used to query the database.
    - processing_guid

    - last_error_message
    - last_error_time

    - item count
    - s3_key
    - integration_name
    - integration_version

    - adapter used.
    - organization_guid

    - array of log_messages

    Methods:
    - Filter count of error messages
    - Add Error Message



    Messages Log Tracking requires of.
    - log_date
    - event_guid
    - log_type
    - log_message
    - log_detail
    """

    def __init__(self,  
                 username: str, password: str, host: str, database: str,
                 organization_guid: str, connector_guid: str, processing_guid: str,
                 integration_name: str, job_parameters: dict):
        
        # Key Parameters: postgresql credentials
        self.connection = psycopg2.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )

        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )

        self.cursor.execute(
            f"SELECT id FROM organization WHERE guid = '{organization_guid}'")
        organization_id = self.cursor.fetchone()
        if organization_id is None:
            raise ValueError("Organization not found")

        self.connector_guid = connector_guid

        # For processiing type, you do need to 

        self.organization_guid = organization_guid
        self.processing_guid = processing_guid
        self.integration_name = integration_name

        self.integration_version = Utils.NoneSafe(job_parameters, 'integration_version')
        self.s3_key = Utils.NoneSafe(job_parameters, 's3_key')
        self.item_count = Utils.NoneSafe(job_parameters, 'item_count')
        self.adapter = Utils.NoneSafe(job_parameters, 'adapter') # Adapter used to process the data.
        self.event_date = Utils.NoneSafe(job_parameters, 'event_date')

        self.log_messages: List[LogMessage] = []
        self.last_error_message = None
        self.last_error_time = None

    def addLogMessage(self, log_message: str, log_detail: str, log_type: str = 'Error', log_console: bool = True):
        self.log_messages.append(LogMessage(log_type, log_message, log_detail))
        if log_type == 'Error':
            self.last_error_message = log_message
            self.last_error_time = Utils.getNow()
            logging.error(log_message, log_detail)
        else:
            logging.info(log_message, log_detail)
        
    def startProcessingStatus(self):
        query = f"""
            INSERT INTO processing_tracker (
                processing_guid,
                status,
                source_guid,
                s3_key,
                connector_guid,
                organization_guid,
                integration_name,
                integration_version,
                source_date,
                task,
                start_time,
                received_time,
                item_count
            ) VALUES (
                '{self.processing_guid}',
                'PROCESSING',
                '{self.processing_guid}',
                '{self.s3_key}',
                '{self.connector_guid}',
                '{self.organization_guid}',
                '{self.integration_name}',
                '{self.integration_version}',
                '{self.event_date}',
                'TIMESLOT PROCESSING',
                '{Utils.getNow()}',
                '{Utils.getNow()}',
                {self.item_count}
            )
        """
        self.cursor.execute(query)
        self.connection.commit()
        
    def changeProcessingStatus(self, status: str):
        self.cursor.execute(
            f"UPDATE processing_tracker SET status = '{status}' WHERE processing_guid = '{self.processing_guid}'"
        )
        self.connection.commit()

    def endProcessingStatus(self):
        # Calculate the count of errors:
        _error_messages = [x for x in self.log_messages if x.log_type == 'Error']
        count_error_messages = len(_error_messages)

        
        end_time = Utils.getNow()
        query = f"""
            UPDATE processing_tracker SET 
                status = 'COMPLETE',
                end_time = '{end_time}'
        """
        
        last_error_message = self.last_error_message
        if last_error_message is not None:
            last_error_log = _error_messages[-1] if count_error_messages > 0 else None
            last_error_datetime = last_error_log.log_date if last_error_log is not None else None
            last_error_datetime = last_error_datetime.strftime('%Y-%m-%d %H:%M:%S') if last_error_datetime is not None else None
            query += f""",
                error_count = {count_error_messages},
                last_error_message = '{last_error_message}',
                last_error_time = '{last_error_datetime}',
                error_sample = '{last_error_log.log_detail}' 
            """

        query += f"WHERE processing_guid = '{self.processing_guid}'"
        self.cursor.execute(
            query= query
        )
        self.connection.commit()

    # destroy overwrite. ensure that the connection is closed.
    def __del__(self):
        self.connection.close()
        self.cursor.close()
        self.connection = None
        self.cursor = None
