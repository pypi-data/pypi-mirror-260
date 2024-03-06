"""
Abstract classes for processing engine.

2024-02-08 14:41:22
- Added IntegrationDataAdapter
- Added IdentitiesBasedIntegrationAdapter wwhch fetches organization data based on the platform entity
- Added ConnectorBasedIntegrationAdapter which fetches organization data based on the connector entity
- Added ProcessingStrategy which is an abstract class for processing strategies


"""

from abc import ABC, abstractmethod
from typing import List

from processing_engine.dda_models import *
from processing_engine.dda_constants import *
from processing_engine.job_service import JobService
from processing_engine.class_helpers import Utils

from pytz import timezone
import math
from dateutil import parser
from datetime import timedelta
from dateutil.parser import parse


class IntegrationDataAdapter(ABC):
    """
    Selects the type of Processing Engine to be used for events depending on the integration type.
    Receives a dict and returns a dataframe.

    """

    integration_name = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not cls.integration_name:
            raise TypeError(f"IntegrationDataAdapter subclass {cls.__name__} must declare integration_name")

    @abstractmethod
    def retrieveOrganizationData(self, jobService: JobService) -> dict:
        
        """
        Retrieves in the following format:
        For Identity Associated:

        event_data (List[dict]): _description_
            organization_data (dict): Organization data should be formatted as:
            {
                organization_guid: str,
                [user_identity]: {
                    timezone: str,
                    user_id: int
                }

            }

        For Connector associated (such as windows, salesforce):
        Since the same user is guaranteed for this entire data cluster. Expect only a single requirement.
        {
            organization_guid: str,
            timezone: str,
            user_id: int
        }

        """
        pass

    @abstractmethod
    def adapt(self, event_datas: List[dict], jobService: JobService) -> EventData:
        """Adapts the data from the raw json to standarized EventData type. 
        
        - Creates organization_data depending on the adapter class. (That requires of a specific identity.)
        - Checks for errors in the event_data. (Checks organization data, timestamp)
        - Populates the dataframe with the organization_data.
        - Compute duration if end_time is present.

        Args:
            event_data (List[dict]): [{Structure depends on each integration.}]

        """
        pass

    def checkConsistency(self, eventData: EventData, jobService: JobService) -> dict:
        """
        This is to be called after merging both the raw event and its respective user/organization data
        Ensure that the 
        - processing_guid is present
        - timestamp is present 
        - that the user_id is present 
        - Ensure that user timezone present.
        - Ensure platform_name is present.
        - Ensure that organization_id is present
        - Ensure that organization_guid is present

        Also handle the following consistencies:
        - If there is a duration and timstamp: then populate end_time
        - If there is an end_time and timestamp: then populate duration
        - Populate local end_time, local_timestamp if they do not exists (or are None)
        - Populate Domain Site if url exists and usable.
        - Ensure that the keystroke, and mouseclicks follow: {1: 2.... [minute]: [count]} format. If not follows the format, then it is set to an empty dictionary.


        Adapts all date related fileds to datetime objects if they are not.

        """

        if not eventData.event_guid or eventData.event_guid is None:
            jobService.addLogMessage(
                log_message=f"Event Guid not found in the event.",
                log_detail=f"Event GuidID not found in the event.\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}",
                log_type="Error"
                )
            return {}

        if not eventData.processing_guid or eventData.processing_guid is None:
            jobService.addLogMessage(
                log_message=f"Processing_guid not found in the event.",
                log_detail=f"Processing_guid not found in the event.\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}",
                log_type="Error"
                )
            return {}

        if not eventData.timestamp or eventData.timestamp is None:
            jobService.addLogMessage(
                log_message=f"Timestamp not found in the event",
                log_detail=f"Timestamp not found in the event.\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}\n\
                        processing_guid {eventData.processing_guid}",
                log_type="Error"
                )
            
            return {}

        
        if not eventData.user_id or eventData.user_id is None:
            jobService.addLogMessage(
                log_message=f"User_id not found in the event.",
                log_detail=f"User_id not found in the event.\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}\n\
                        processing_guid {eventData.processing_guid}",
                log_type="Error"
                )
            return {}
        
        if not eventData.local_timezone or eventData.local_timezone is None:
            jobService.addLogMessage(
                log_message=f"Timezone not found in the event.",
                log_detail=f"Timezone not found in the event.\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}\n\
                        processing_guid {eventData.processing_guid}",
                log_type="Error"
                )
            return {}
        
        if not eventData.integration_name or eventData.integration_name is None or eventData.integration_name == "":
            jobService.addLogMessage(
                log_message=f"Platform_name not found in the event.",
                log_detail=f"Platform_name not found in the event.\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}\n\
                        processing_guid {eventData.processing_guid}",
                log_type="Error"
                )
            return {}
        
        if not eventData.organization_id or eventData.organization_id is None:
            jobService.addLogMessage(
                log_message=f"Organization_id not found in the event.",
                log_detail=f"Organization_id not found in the event.\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}",
                log_type="Error"
                )
            return {}
        
        if not eventData.organization_guid or eventData.organization_guid is None:
            jobService.addLogMessage(
                log_message=f"Organization_guid not found in the event.",
                log_detail=f"Organization_guid not found in the event.\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}",
                log_type="Error"
                )
            return {}

            
        # Populate duration if it does not exists and endtime is usable.
        if eventData.end_time is not None and eventData.timestamp is not None:
            end_time = Utils.parseDate(eventData.end_time)
            timestamp = Utils.parseDate(eventData.timestamp)
            duration = (end_time - timestamp).total_seconds()
            eventData.duration = math.ceil(duration)

        # Populate endtime if it does not exists and duration is usable.
        if eventData.duration is not None and eventData.duration > 0:
            duration_seconds = timedelta(seconds=eventData.duration)
            timestamp = Utils.parseDate(eventData.timestamp)
            eventData.end_time = (timestamp + duration_seconds).isoformat()

        # Populate local timestamp if they do not exists.
        if eventData.timestamp_local is None:
            timestamp = Utils.parseDate(eventData.timestamp)
            local_timestamp = timestamp.astimezone(timezone(eventData.local_timezone))
            eventData.timestamp_local = local_timestamp.isoformat()

        # Populate local endtime if it does not exists and endtime is usable.
        if eventData.end_time is not None and (eventData.end_time_local is None  or eventData.end_time_local == ''):
            endtime = Utils.parseDate(eventData.end_time)
            eventData.end_time_local = endtime.astimezone(timezone(eventData.local_timezone))



        # Ensure that the keystroke, and mouseclicks follow: {[minutetimestamp]: [count]} format.
        if eventData.keystrokes is not None and eventData.keystrokes != {}:
            if not all(isinstance(x, int) for x in eventData.keystrokes.values()):
                jobService.addLogMessage(
                    log_message=f"Keystrokes not in the right format.",
                    log_detail="Keystrokes not in the right format.\n\
                        using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}\n\
                            processing_guid {event.processing_guid}, Obtained ",
                    log_type="Error"
                    )
                eventData.keystrokes = {}
        else:
            eventData.keystrokes = {}

        # Fill values done at the end. Such as populating end_time, local_end_time if they do not exists yet.
        if eventData.end_time is None:
            eventData.end_time = eventData.timestamp
            eventData.duration = 0
        if eventData.end_time_local is None:
            eventData.end_time_local = eventData.timestamp_local



        # Check if timestamp exists. That is a parsable valid date.
        if eventData.timestamp is not None:
            try:
                Utils.parseDate(eventData.timestamp)
            except ValueError:
                jobService.addLogMessage(
                    log_message=f"Timestamp not in the right format.",
                    log_detail="Timestamp not in the right format.\n\
                        using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}\n\
                            processing_guid {eventData.processing_guid}, Obtained ",
                    log_type="Error"
                    )
                return {}
        
        # Check if end_time exists. That is a parsable valid date.
        if eventData.end_time is not None:
            try:
                Utils.parseDate(eventData.end_time)
            except ValueError:
                jobService.addLogMessage(
                    log_message=f"End_time not in the right format.",
                    log_detail="End_time not in the right format.\n\
                        using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}\n\
                            processing_guid {eventData.processing_guid}, Obtained ",
                    log_type="Error"
                    )
                return {}
        
        # ADAPT all datetime fields to datetime objects
        eventData.timestamp = Utils.parseDate(eventData.timestamp)
        eventData.end_time = Utils.parseDate(eventData.end_time)
        eventData.timestamp_local = Utils.parseDate(eventData.timestamp_local)
        eventData.end_time_local = Utils.parseDate(eventData.end_time_local)
        
        return eventData

class IdentitiesBasedIntegrationAdapter(IntegrationDataAdapter):

    integration_name = 'identities_based_adapter'
    def retrieveOrganizationData(self, jobService: JobService) -> dict:
        """
        Retrieves in the following format:
        different users might be for each of this organization, that can be identified throguht the organization_guid and integration_name
        {
            organization_guid: str,
            organization_id: int,
            [user_identity]: {
                timezone: str,
                user_id: int
            }
        }

        2024-02-20 10:40:58
        - Removed tiying Identity with Platform
        """
        
        cursor = jobService.cursor
        res = {
            "organization_guid": jobService.organization_guid,
        }

        # Retrieve organization_id 
        cursor.execute(
            f"SELECT id FROM organization WHERE guid = '{jobService.organization_guid}'"
        )
        cursor_response_organization = cursor.fetchone()
        
        if not cursor_response_organization:
            jobService.addLogMessage(
                log_message=f"Organization not found in the database. from organization {jobService.organization_guid}",
                log_detail="Organization not found in the database. from organization {jobService.organization_guid}\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}",
                log_type="Error"
                )
            # This should be a breaking error
            raise Exception("Organization not found in the database.")
    
        res["organization_id"] = cursor_response_organization[0]

        # Get all identities identified for the organization for x platform:  
        
        cursor.execute(
            f"SELECT user_id, identity FROM identity WHERE organization_guid = '{jobService.organization_guid}'"
        )
        cursor_response_identities = cursor.fetchall()

        if not cursor_response_identities:
            jobService.addLogMessage(
                log_message=f"User not found in the database. from organization {jobService.organization_guid}",
                log_detail="User not found in the database. from organization {jobService.organization_guid}\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}",
                log_type="Error"
                )
            # This should be a breaking error
            raise Exception("identities not found in the database for organization.")
        
        # Fetch the user_id and timezone for all users in X organization
        
        cursor.execute(
            f"SELECT id, timezone FROM users WHERE organization_guid = '{jobService.organization_guid}'"
        )
        cursor_response_users = cursor.fetchall()

        if not cursor_response_users:
            jobService.addLogMessage(
                log_message=f"User not found in the database. from organization {jobService.organization_guid}",
                log_detail="User not found in the database. from organization {jobService.organization_guid}\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}",
                log_type="Error"
                )
            # This should be a breaking error
            raise Exception("User not found in the database for organization.")

        # Create a map of user_id to timezone
        user_data_map = {}
        for user in cursor_response_users:
            user_data_map[user[0]] = user[1]


        for user in cursor_response_identities:
            res[user[1]] = {
                "user_id": user[0],
                "timezone":  user_data_map[user[0]]
            }

            
        return res
    
class ConnectorBasedIntegrationAdapter(IntegrationDataAdapter):
    integration_name = 'connector_based_adapter'
    def retrieveOrganizationData(self, jobService: JobService) -> dict:
        """
        Retrieves in the following format:
        Since the same user is guaranteed for this entire data cluster. Expect only a single requirement.
        {
            organization_guid: str,
            organization_id: int,
            timezone: str,
            user_id: int
        }
        """
        
        cursor = jobService.cursor
        res = {
            "organization_guid": jobService.organization_guid,

        } # nod to leetcode xd


        
        # Retrieve organization_id 
        cursor.execute(
            f"SELECT id FROM organization WHERE guid = '{jobService.organization_guid}'"
        )
        cursor_response_organization = cursor.fetchone()

        if not cursor_response_organization:
            jobService.addLogMessage(
                log_message=f"Organization not found in the database. from organization {jobService.organization_guid}",
                log_detail="Organization not found in the database. from organization {jobService.organization_guid}\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}",
                log_type="Error"
                )
            # This should be a breaking error
            raise Exception("Organization not found in the database.")
        
        res["organization_id"] = cursor_response_organization[0]

        # Check for the user_id where connector is X
        cursor.execute(
            f"SELECT c.user_id, u.timezone FROM connector AS c JOIN users AS u ON u.id = c.user_id WHERE c.guid = '{jobService.connector_guid}';"
        )
        cursor_response = cursor.fetchone()     


        
        if cursor_response:
            res["user_id"] = cursor_response[0]
            res["timezone"] = cursor_response[1]
        else:
            jobService.addLogMessage(
                log_message=f"User not found in the database. from connector {jobService.connector_guid}",
                log_detail="User not found in the database. from connector {jobService.connector_guid}\n\
                    using integration_name {self.integration_name} and organization_guid {jobService.organization_guid}",
                log_type="Error"
                )
            # This should be a breaking error
            raise Exception("User not found in the database for connector.")

        return res
    

class ProcessingStrategy(ABC):
    """
    
    Enriches data from a standard Pandas dataframe format to another(s).
    Once enriched, in charge of POSTING and UPDATING the the database.


    Must implement:
    - Instantiate with JobService()
    - enhance()
    """

    def __init__(self, job_service: JobService):
        self.job_service = job_service


    @abstractmethod
    def enhance(self, event_data: List[dict], jobService: JobService):
        pass


