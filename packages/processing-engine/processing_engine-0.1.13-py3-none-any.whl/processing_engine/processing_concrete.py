"""
Concrete implementations of the abstract classes in processing_abstract.py.

2024-02-08 14:40:25
- Added Concrete implementation of SalesforceIntegrationAdapter

"""

from processing_engine.dda_constants import *
from processing_engine.dda_models import *
from processing_engine.processing_abstract import *
from processing_engine.job_service import JobService
from processing_engine.class_helpers import Utils


from typing import List, Dict
import json
import datetime
import pytz
from datetime import timedelta

class TimeslotProcessing(ProcessingStrategy):
    """
    Basic enhancement strategy, simply returns the dataframe as is.


    Stages and models the data to be published to the database.:

    1. Receives: List[EventData] with organization data embued in it.
    3. [x] Collapse events with similar span_guid events (local)
    4. [x] Timeslots Creation
    5. Categorization jobs (if needed) NOT required as for 2024-02-08 16:34:38
    6. PUBLISH EVENTS: Check if there is the same events
    7. PUBLISH TIMESLOTS: Check if there are the same timeslots, filter out the ones that are already present.


    """

    def __init__(self, jobService: JobService):
        self.jobService = jobService

    def enhance(self, eventDataList: List[EventData]):
        """Enhances the events in the following ways:
        - Populates local time related columns
        - splitEvents: List[Event]
        - Creates timeslots for the events.
        - Filters or Updates which timeslots are to be published.
        - Updates the events end_time if an earlier one was present on the database.

        """

        # Graving an EventDataList Picks the Jobs
        collapsedEvents: List[EventData] = self.collapseEventsSimilarEventGUID(eventDataList)
        events, timeslots = self.splitEvents(collapsedEvents)

        self.publishTimeslots(timeslots)
        self.publishEvents(events)
    
    def collapseEventsSimilarEventGUID(self, eventDataList: List[EventData]) -> List[EventData]:
        """Collapses the events with similar span_guid events.
        Non-Method intended to be used for collapsing the correct events.
        Modifies the eventDataList in place given the first clicks, keystrokes when ocllapsing.

        2024-02-08 16:19:37
        - Make sure to collapse clicks and keystrokes as well.
        
        Which come with the following format:
            
        NOTE: 
        Mouseclicks and keystrokes are expected to have the following format:
        Separated in minutes.
        {
            %Y-%m-%d %H:%M:: [count],
            2024-02-08 16:19: 1,
            2024-02-08 16:20: 2,
            ...
            [minute]: [count]
        }

        """
        event_guid_min_max_memory = {}
        collapsed_events: List[EventData] = []


        def addClicksAndKeystrokes(collapsedEvent: EventData, idx: int, eventDataList: List[EventData]) -> None:
            """
            Adds the clicks and keystrokes to the reference event.
            NOTE: This is an impure function, it modifies the eventDataList in place.

            """

            ref_event = eventDataList[idx]
            if ref_event is None:
                return


            if collapsedEvent.mouse_clicks != {} and ref_event.mouse_clicks != {} and ref_event.mouse_clicks is not None:
                for unique_minutestamp, clicks in collapsedEvent.mouse_clicks.items():
                    ref_event.mouse_clicks[unique_minutestamp] = ref_event.mouse_clicks[unique_minutestamp] + clicks if unique_minutestamp in ref_event.mouse_clicks else clicks
            if collapsedEvent.keystrokes != {} and ref_event.keystrokes != {} and ref_event.keystrokes is not None: 
                for unique_minutestamp, keystrokes in collapsedEvent.keystrokes.items():
                    ref_event.keystrokes[unique_minutestamp] = ref_event.keystrokes[unique_minutestamp] + keystrokes if unique_minutestamp in ref_event.keystrokes else keystrokes
            

        for idx, collapsedEvent in enumerate(eventDataList):
            if collapsedEvent.event_guid not in event_guid_min_max_memory:
                min_max_event_data = {
                    "min": collapsedEvent.timestamp,
                    "max": collapsedEvent.end_time,
                    "idx": idx # keeps track and updates the first time reference.
                    
                }
                event_guid_min_max_memory[collapsedEvent.event_guid] = min_max_event_data
            else:
                min_max_event_data = event_guid_min_max_memory[collapsedEvent.event_guid]
                if collapsedEvent.end_time > min_max_event_data["max"]:
                    min_max_event_data["max"] = collapsedEvent.end_time
                    reference_id = min_max_event_data["idx"]
                    addClicksAndKeystrokes(collapsedEvent, reference_id, eventDataList)
        
        # Now, lets add the collapsed events.
        collapsed_events: List[EventData] = []
        for min_max_event_data in event_guid_min_max_memory.values():
            collapsedEvent: EventData = eventDataList[min_max_event_data["idx"]]
            collapsedEvent.timestamp = min_max_event_data["min"]
            collapsedEvent.end_time = min_max_event_data["max"]
            collapsed_events.append(collapsedEvent)

        return collapsed_events
    
    def defineTimeslot(self, curr_time: datetime.datetime, eventData: EventData) -> Timeslot:
        # Calulcate the ts1 as the minute of the day. e.g. 00:00:00 -> 0, 00:01:00 -> 1, 00:02:00 -> 2
        
        timestamp_datetime: datetime.datetime = curr_time
        timestamp_local_datetime: datetime.datetime = timestamp_datetime.astimezone(pytz.timezone(eventData.local_timezone))


        # Extract UTC Date Time Components
        hour = timestamp_datetime.hour
        minute = timestamp_datetime.minute
        day = timestamp_datetime.day
        month = timestamp_datetime.month
        year = timestamp_datetime.year

        timestamp_isocalendar = timestamp_datetime.isocalendar()
        week =  timestamp_isocalendar[1]
        weekday = timestamp_datetime.weekday()

        # Extract Local Date Time Components
        hour_local = timestamp_local_datetime.hour
        minute_local = timestamp_local_datetime.minute
        day_local = timestamp_local_datetime.day
        month_local = timestamp_local_datetime.month
        year_local = timestamp_local_datetime.year

        timestamp_local_isocalendar = timestamp_local_datetime.isocalendar()
        week_local =  timestamp_local_isocalendar[1]
        weekday_local = timestamp_local_datetime.weekday()

        ts1 = timestamp_datetime.hour * 60 + timestamp_datetime.minute
        ts5 = ts1 // 5
        ts10 = ts1 // 10
        ts15 = ts1 // 15

        tl1 = timestamp_local_datetime.hour * 60 + timestamp_local_datetime.minute
        tl5 = tl1 // 5
        tl10 = tl1 // 10
        tl15 = tl1 // 15


        # Find mouseclicks and keyboard strokes at this specific time.


        year_month_day_minute = Utils.datetimeToYearMonthDayMinute(timestamp_datetime)
        
        return Timeslot(
            event_guid = eventData.event_guid,
            organization_guid = eventData.organization_guid,

            hour = hour,
            minute = minute,
            day = day,
            month = month,
            year = year,
            week = week,
            weekday = weekday,

            hour_local = hour_local,
            minute_local = minute_local,
            day_local = day_local,
            month_local = month_local,
            year_local = year_local,
            week_local = week_local,
            weekday_local = weekday_local,
            
            mouse_clicks= eventData.mouse_clicks[year_month_day_minute] if eventData.mouse_clicks is not None and year_month_day_minute in eventData.mouse_clicks else 0,
            keystrokes = eventData.keystrokes[year_month_day_minute] if eventData.keystrokes is not None and year_month_day_minute in eventData.keystrokes else 0,
            processing_guid= eventData.processing_guid,

            ts1= ts1,
            ts5= ts5,
            ts10= ts10,
            ts15= ts15,

            tl1= tl1,
            tl5= tl5,
            tl10= tl10,
            tl15= tl15,

            event_end_time= eventData.end_time,
        )

    def splitEvents(self, eventDataList: List[EventData]) -> (List[Event], List[Timeslot]): # type: ignore
        """Creates the timeslots from the events.
        - The timeslots are created from the events.
        - The timeslots are assumed to be in the same timezone.

        @return: List[Event], List[Timeslot]  # The events and the timeslots created from the eventDatas.

        """

        events_list: List[Event] = []
        timeslots_lists: List[Timeslot] = []

        for eventData in eventDataList:
            event: Event = Event(
                guid = eventData.event_guid,
                organization_guid = eventData.organization_guid,
                organization_id = eventData.organization_id,

                user_id = eventData.user_id,
                application = eventData.application,
                app = eventData.app,
                app_type = eventData.app_type,

                operation = eventData.operation,
                operation_type = eventData.operation_type,
                
                integration_name = eventData.integration_name,

                local_timezone= eventData.local_timezone,
                timestamp = eventData.timestamp,
                
                end_time = eventData.end_time,
                timestamp_local = eventData.timestamp_local,
                end_time_local = eventData.end_time_local,
                duration = eventData.duration,
                description = eventData.description,
                url = eventData.url,
                site = eventData.site,
                files = eventData.files,
                file_count = eventData.file_count,
                size = eventData.size,

                action_type = eventData.action_type,
                geolocation= eventData.geolocation,
                ipv4 = eventData.ipv4,
                local_ipv4= eventData.local_ipv4,
                
                email_subject= eventData.email_subject,
                from_address= eventData.from_address,
                to_address= eventData.to_address,
                email_cc = eventData.email_cc,
                email_bcc = eventData.email_bcc,
                email_imid = eventData.email_imid,
                phone_result = eventData.phone_result,
                record_url = eventData.record_url,
                recording_url = eventData.recording_url,
                record_id = eventData.record_id,

                tags = eventData.tags,
            )
            events_list.append(event)
            
            # now, for every 1 minute, compute the required timeslots.
            timeslots = self.createTimeslots(eventData)
            if timeslots is not None and timeslots != []:
                timeslots_lists.extend(timeslots)
        return events_list, timeslots_lists

    def createTimeslots(self, eventData: EventData) -> List[Timeslot]:
        """
        Creates timeslots for the events, Splits every 1 minute to find the timeslots.
        """
        if eventData.end_time is None or eventData.duration is None:
            return None
        
        timeslots: List[Timeslot] = []
        curr_time = Utils.parseDate(eventData.timestamp)
        end_time = Utils.parseDate(eventData.end_time)



        if eventData.end_time is not None and eventData.duration is not None and eventData.duration > 0:
            while curr_time <= end_time:
                timeslot = self.defineTimeslot(curr_time, eventData)
                timeslots.append(timeslot)
                curr_time = curr_time + timedelta(minutes=1)

        else:
            # If the end_time is not present, then we can only create the timeslots for the duration of the event.

            timeslot = self.defineTimeslot(curr_time, eventData)
            timeslots.append(timeslot)
        
        return timeslots

    def publishTimeslots(self, timeslots: List[Timeslot], autocorrection = True) -> bool:
        """
        Publishes the timeslots to the database.

        2024-02-15 16:24:26
        - The following procedure was skipped, as it is irrrelevant for ANY front end application using the timeslots. AS the only thing that matters is that there is ONE timeslot with the correct keystrokes, and the second, that even if they are duplicated, they have the same event_guid. Which means
        When fetching and running unique(event_guids), the events related will actually be correct.
        Fetches all the timeslots with the organization_guid catching where the event_guid IN (unique event_guids).
        If the timeslots are not present, it 
        - This will produce a KNOWN bug, which doesnt matter for the front end application, as the timeslots are only used for the timeslot data, and the events are used for the events data.
        Instead the prodcedure will only used to INSERT ALL times.

        @return bool: True if the timeslots were published successfully, False otherwise.
        """



        column_names_timeslots = Timeslot.get_publishing_keys()
        insert_sql = f"INSERT INTO timeslot ({', '.join(column_names_timeslots)}) VALUES ({', '.join(['%s'] * len(column_names_timeslots))})"
        jobService = self.jobService

        def cleanQueryArgument(queryArgument):
            # If the queryArg is a list or dict, format it into a way that is query insertable
            if isinstance(queryArgument, (dict)):
                # If the is List and the first element is a dict, then it is a list of objects
                return json.dumps(queryArgument)
            if isinstance(queryArgument, List) and len(queryArgument) >0 and isinstance(queryArgument[0], dict):
                # return an array of strings of the json
                for(i, item) in enumerate(queryArgument):
                    queryArgument[i] = cleanQueryArgument(item)
            
            return queryArgument
        


        # Clean the query arguments 
        for timeslot in timeslots:
            values = []
            for column_name in column_names_timeslots:
                values.append(cleanQueryArgument(getattr(timeslot, column_name)))
            try:
                jobService.cursor.execute(insert_sql, values)
            except Exception as e:
                jobService.addLogMessage(jobService, f"Error inserting timeslot: {e}", f"Error inserting timeslot: {e}", "Error")
                return False
            
            jobService.connection.commit()
            

        return True
        
    def publishEvents(self, events: List[Event]) -> bool:
        """
        Fetch if there are the same events, creates two lists:
        - if they don't exist, then insert them.
        - if they exist, then ONLY update their end_time.
        """
        events_guids = [event.guid for event in events]
        select_sql = f"SELECT guid, end_time, end_time_local FROM event WHERE guid IN ({', '.join(['%s'] * len(events_guids))})"
        self.jobService.cursor.execute(select_sql, events_guids)
        existing_events = self.jobService.cursor.fetchall()
        mockEvents:  Dict[str, DatabaseEvent] = {} # Data structure containing only {guid, end_time, end_time_local}
        for existing_event in existing_events:
            mockEvent = DatabaseEvent()
            mockEvent.guid = existing_event['guid']
            mockEvent.end_time = existing_event['end_time']
            mockEvent.end_time_local = existing_event['end_time_local']
            mockEvents[mockEvent.guid] = mockEvent
        
        eventsToInsert: List[Event] = []
        eventsToUpdate: List[DatabaseEvent] = []

        for event in events:
            if event.guid in mockEvents:
                event_end_time = event.end_time.replace(tzinfo=pytz.UTC)
                mock_event_end_time = mockEvents[event.guid].end_time.replace(tzinfo=pytz.UTC)
                
                if event_end_time > mock_event_end_time:
                    databaseEvent = DatabaseEvent()
                    databaseEvent.guid = event.guid
                    databaseEvent.end_time = event.end_time
                    databaseEvent.end_time_local = event.end_time_local
                    eventsToUpdate.append(
                        databaseEvent
                    )
            else:
                eventsToInsert.append(event)
        self.updateEvents(eventsToUpdate)
        self.insertEvents(eventsToInsert)

    def updateEvents(self, events: List[DatabaseEvent]) -> bool:
        """
        Updates the the endtimes to the database.

        @return bool: True if the events were published successfully, False otherwise.
        """
        
        update_sql = f"UPDATE event SET end_time = %s, end_time_local = %s WHERE guid = %s"
        jobService = self.jobService
        for event in events:
            values = [event.end_time, event.end_time_local, event.guid]
            try:
                self.job_service.addLogMessage(
                    log_message = f"Updating event at guid {event.guid}",
                    log_detail = f"Updating event: {values}",
                    log_type = "Info"
                )
                jobService.cursor.execute(update_sql, values)
            except Exception as e:
                self.job_service.addLogMessage(
                    log_message = f"Error updating event at guid {event.guid}",
                    log_detail = f"Error updating event: {e}",
                    log_type = "Error"
                )
                return False
            
            jobService.connection.commit()
        return True

            
    def insertEvents(self, events: List[Event]) -> bool:
        """
        Inserts the events to the database.

        @return bool: True if the events were published successfully, False otherwise.
        """
        column_names_events = Event.get_publishing_keys()
        insert_sql = f"INSERT INTO event ({', '.join(column_names_events)}) VALUES ({', '.join(['%s'] * len(column_names_events))})"
        def cleanQueryArgument(queryArgument):
            # If the queryArg is a list or dict, format it into a way that is query insertable
            if isinstance(queryArgument, (dict)):
                # If the is List and the first element is a dict, then it is a list of objects
                return json.dumps(queryArgument)
            if isinstance(queryArgument, List) and len(queryArgument) >0 and isinstance(queryArgument[0], dict):
                # return an array of strings of the json
                for(i, item) in enumerate(queryArgument):
                    queryArgument[i] = cleanQueryArgument(item)
            
            return queryArgument

        # Clean the query arguments 
        jobService = self.jobService
        for event in events:
            values = []
            for column_name in column_names_events:
                values.append(cleanQueryArgument(getattr(event, column_name)))
            try:
                jobService.cursor.execute(insert_sql, values)
            except Exception as e:
                jobService.addLogMessage(jobService, f"Error inserting event: {e}", f"Error inserting event: {e}", "Error")
                return False
            
            jobService = self.jobService
            jobService.connection.commit()
            jobService.connection.commit()
            

        return True

class JobManager():
    """Management of the enhancement process.
    - In charge of posting processingTracker once the job is handled at start. 

    - Once processing is processed (including errors), it should post the processingTracker with the error count, endtime.
    - In charge of Updating processingTracker to Error.

    """






