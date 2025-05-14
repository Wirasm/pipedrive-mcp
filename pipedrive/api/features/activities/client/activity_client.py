import json
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from log_config import logger
from pipedrive.api.base_client import BaseClient


class ActivityClient:
    """Client for Pipedrive Activity API endpoints"""

    def __init__(self, base_client: BaseClient):
        """
        Initialize the Activity client

        Args:
            base_client: BaseClient instance for making API requests
        """
        self.base_client = base_client

    async def create_activity(
        self,
        subject: str,
        type: str,
        owner_id: Optional[int] = None,
        deal_id: Optional[int] = None,
        lead_id: Optional[str] = None,
        person_id: Optional[int] = None, 
        org_id: Optional[int] = None,
        due_date: Optional[str] = None,
        due_time: Optional[str] = None,
        duration: Optional[str] = None,
        busy: Optional[bool] = None,
        done: Optional[bool] = None,
        note: Optional[str] = None,
        location: Optional[Union[str, Dict[str, Any]]] = None,
        public_description: Optional[str] = None,
        priority: Optional[int] = None,
        participants: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new activity in Pipedrive

        Args:
            subject: Subject of the activity
            type: Type of the activity (key_string of an ActivityType)
            owner_id: User ID of the activity owner
            deal_id: ID of the deal linked to the activity
            lead_id: UUID of the lead linked to the activity
            person_id: ID of the person linked to the activity (NOTE: read-only field)
            org_id: ID of the organization linked to the activity
            due_date: Due date in ISO format (YYYY-MM-DD)
            due_time: Due time in HH:MM format
            duration: Duration in HH:MM format
            busy: Whether the activity marks the assignee as busy
            done: Whether the activity is marked as done
            note: Note for the activity
            location: Location of the activity (string or location object)
            public_description: Public description of the activity
            priority: Priority of the activity
            participants: List of participant objects with person_id

        Returns:
            Created activity data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"ActivityClient: Attempting to create activity '{subject}'")

        try:
            payload: Dict[str, Any] = {
                "subject": subject,
                "type": type
            }
            
            # Add optional parameters if provided
            if owner_id is not None:
                payload["owner_id"] = owner_id
            if deal_id is not None:
                payload["deal_id"] = deal_id
            if lead_id is not None:
                payload["lead_id"] = lead_id
            # Note: person_id is a read-only field, use participants instead
            if person_id is not None:
                logger.warning("person_id is a read-only field in Pipedrive API. Use participants instead.")
                payload["person_id"] = person_id
            if org_id is not None:
                payload["org_id"] = org_id
            if due_date is not None:
                payload["due_date"] = due_date
            if due_time is not None:
                payload["due_time"] = due_time
            if duration is not None:
                payload["duration"] = duration
            if busy is not None:
                payload["busy"] = busy
            if done is not None:
                payload["done"] = done
            if note is not None:
                payload["note"] = note
            
            # Handle location which can be a string or object
            if location is not None:
                if isinstance(location, str):
                    payload["location"] = {"value": location}
                else:
                    payload["location"] = location
                    
            if public_description is not None:
                payload["public_description"] = public_description
            if priority is not None:
                payload["priority"] = priority
                
            # Add participants if provided
            if participants is not None:
                payload["participants"] = participants

            # Validate required fields
            if not subject or not subject.strip():
                raise ValueError("Activity subject cannot be empty")
            if not type or not type.strip():
                raise ValueError("Activity type cannot be empty")

            # Log payload with sensitive information redacted
            log_payload = payload.copy()
            logger.debug(
                f"ActivityClient: create_activity payload: {json.dumps(log_payload, indent=2)}"
            )

            # Make API request
            response_data = await self.base_client.request(
                "POST", 
                "/activities", 
                json_payload=payload,
                version="v2"
            )
            return response_data.get("data", {})

        except ValueError as e:
            logger.error(f"Validation error in create_activity: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in create_activity: {str(e)}")
            raise

    async def get_activity(
        self,
        activity_id: int,
        include_fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get an activity by ID from Pipedrive

        Args:
            activity_id: ID of the activity to retrieve
            include_fields: Additional fields to include in the response

        Returns:
            Activity data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"ActivityClient: Attempting to get activity with ID {activity_id}")

        try:
            # Validate activity_id
            if activity_id <= 0:
                raise ValueError(f"Invalid activity ID: {activity_id}. Must be a positive integer.")

            query_params: Dict[str, Any] = {}

            if include_fields:
                query_params["include_fields"] = ",".join(include_fields)

            response_data = await self.base_client.request(
                "GET",
                f"/activities/{activity_id}",
                query_params=query_params if query_params else None,
                version="v2"
            )
            return response_data.get("data", {})

        except ValueError as e:
            logger.error(f"Validation error in get_activity: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in get_activity: {str(e)}")
            raise

    async def list_activities(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        filter_id: Optional[int] = None,
        owner_id: Optional[int] = None,
        deal_id: Optional[int] = None,
        lead_id: Optional[str] = None,
        person_id: Optional[int] = None,
        org_id: Optional[int] = None,
        updated_since: Optional[str] = None,
        updated_until: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None,
        include_fields: Optional[List[str]] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        List activities from Pipedrive with pagination

        Args:
            limit: Maximum number of results to return (default 100, max 500)
            cursor: Pagination cursor for the next page
            filter_id: ID of the filter to apply
            owner_id: Filter by activity owner ID
            deal_id: Filter by associated deal ID
            lead_id: Filter by associated lead ID
            person_id: Filter by associated person ID
            org_id: Filter by associated organization ID
            updated_since: Filter by update time (RFC3339 format)
            updated_until: Filter by update time (RFC3339 format)
            sort_by: Field to sort by (id, update_time, add_time)
            sort_direction: Sort direction (asc, desc)
            include_fields: Additional fields to include

        Returns:
            Tuple of (list of activities, next cursor)

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(
            f"ActivityClient: Attempting to list activities with limit {limit}, cursor '{cursor}'"
        )

        try:
            # Validate limit
            if limit < 1 or limit > 500:
                raise ValueError(f"Invalid limit: {limit}. Must be between 1 and 500.")

            # Validate sort_direction
            if sort_direction and sort_direction not in ["asc", "desc"]:
                raise ValueError(f"Invalid sort_direction: {sort_direction}. Must be 'asc' or 'desc'.")

            # Validate sort_by
            valid_sort_fields = ["id", "update_time", "add_time"]
            if sort_by and sort_by not in valid_sort_fields:
                raise ValueError(f"Invalid sort_by: {sort_by}. Must be one of: {', '.join(valid_sort_fields)}")

            query_params: Dict[str, Any] = {
                "limit": limit,
                "cursor": cursor,
                "filter_id": filter_id,
                "owner_id": owner_id,
                "deal_id": deal_id,
                "lead_id": lead_id,
                "person_id": person_id,
                "org_id": org_id,
                "updated_since": updated_since,
                "updated_until": updated_until,
                "sort_by": sort_by,
                "sort_direction": sort_direction,
            }

            if include_fields:
                query_params["include_fields"] = ",".join(include_fields)

            # Filter out None values
            final_query_params = {k: v for k, v in query_params.items() if v is not None}
            logger.debug(f"ActivityClient: list_activities query_params: {final_query_params}")

            response_data = await self.base_client.request(
                "GET",
                "/activities",
                query_params=final_query_params if final_query_params else None,
                version="v2"
            )

            activities_list = response_data.get("data", [])
            additional_data = response_data.get("additional_data", {})
            next_cursor = (
                additional_data.get("next_cursor")
                if isinstance(additional_data, dict)
                else None
            )
            logger.info(
                f"ActivityClient: Listed {len(activities_list)} activities. Next cursor: '{next_cursor}'"
            )
            return activities_list, next_cursor

        except ValueError as e:
            logger.error(f"Validation error in list_activities: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in list_activities: {str(e)}")
            raise

    async def update_activity(
        self,
        activity_id: int,
        subject: Optional[str] = None,
        type: Optional[str] = None,
        owner_id: Optional[int] = None,
        deal_id: Optional[int] = None,
        lead_id: Optional[str] = None,
        person_id: Optional[int] = None,
        org_id: Optional[int] = None,
        due_date: Optional[str] = None,
        due_time: Optional[str] = None,
        duration: Optional[str] = None,
        busy: Optional[bool] = None,
        done: Optional[bool] = None,
        note: Optional[str] = None,
        location: Optional[Union[str, Dict[str, Any]]] = None,
        public_description: Optional[str] = None,
        priority: Optional[int] = None,
        participants: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing activity in Pipedrive

        Args:
            activity_id: ID of the activity to update
            subject: Updated subject of the activity
            type: Updated type of the activity
            owner_id: Updated user ID of the activity owner
            deal_id: Updated ID of the deal linked to the activity
            lead_id: Updated UUID of the lead linked to the activity
            person_id: Updated ID of the person linked to the activity (NOTE: read-only field)
            org_id: Updated ID of the organization linked to the activity
            due_date: Updated due date in ISO format (YYYY-MM-DD)
            due_time: Updated due time in HH:MM format
            duration: Updated duration in HH:MM format
            busy: Updated busy flag
            done: Updated done flag
            note: Updated note for the activity
            location: Updated location of the activity (string or location object)
            public_description: Updated public description of the activity
            priority: Updated priority of the activity
            participants: Updated list of participant objects with person_id

        Returns:
            Updated activity data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails or no fields are provided to update
        """
        logger.info(f"ActivityClient: Attempting to update activity with ID {activity_id}")

        try:
            # Validate activity_id
            if activity_id <= 0:
                raise ValueError(f"Invalid activity ID: {activity_id}. Must be a positive integer.")

            payload: Dict[str, Any] = {}
            
            # Add fields to update if provided
            if subject is not None:
                payload["subject"] = subject
            if type is not None:
                payload["type"] = type
            if owner_id is not None:
                payload["owner_id"] = owner_id
            if deal_id is not None:
                payload["deal_id"] = deal_id
            if lead_id is not None:
                payload["lead_id"] = lead_id
            # Note: person_id is a read-only field, use participants instead
            if person_id is not None:
                logger.warning("person_id is a read-only field in Pipedrive API. Use participants instead.")
                payload["person_id"] = person_id
            if org_id is not None:
                payload["org_id"] = org_id
            if due_date is not None:
                payload["due_date"] = due_date
            if due_time is not None:
                payload["due_time"] = due_time
            if duration is not None:
                payload["duration"] = duration
            if busy is not None:
                payload["busy"] = busy
            if done is not None:
                payload["done"] = done
            if note is not None:
                payload["note"] = note
                
            # Handle location which can be a string or object
            if location is not None:
                if isinstance(location, str):
                    payload["location"] = {"value": location}
                else:
                    payload["location"] = location
                    
            if public_description is not None:
                payload["public_description"] = public_description
            if priority is not None:
                payload["priority"] = priority
                
            # Add participants if provided
            if participants is not None:
                payload["participants"] = participants

            # Ensure at least one field is being updated
            if not payload:
                logger.warning(
                    f"ActivityClient: update_activity called with no fields to update for ID {activity_id}."
                )
                raise ValueError(
                    "At least one field must be provided for updating an activity."
                )

            # Log payload
            logger.debug(
                f"ActivityClient: update_activity payload for ID {activity_id}: {json.dumps(payload, indent=2)}"
            )

            # Make API request
            response_data = await self.base_client.request(
                "PATCH", 
                f"/activities/{activity_id}", 
                json_payload=payload,
                version="v2"
            )
            return response_data.get("data", {})

        except ValueError as e:
            logger.error(f"Validation error in update_activity: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in update_activity: {str(e)}")
            raise

    async def delete_activity(self, activity_id: int) -> Dict[str, Any]:
        """
        Delete an activity from Pipedrive

        Args:
            activity_id: ID of the activity to delete

        Returns:
            Deletion result data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"ActivityClient: Attempting to delete activity with ID {activity_id}")

        try:
            # Validate activity_id
            if activity_id <= 0:
                raise ValueError(f"Invalid activity ID: {activity_id}. Must be a positive integer.")

            response_data = await self.base_client.request(
                "DELETE", 
                f"/activities/{activity_id}",
                version="v2"
            )

            # Successful delete usually returns: {"success": true, "data": {"id": activity_id}}
            return (
                response_data.get("data", {})
                if response_data.get("success")
                else {"id": activity_id, "error_details": response_data}
            )

        except ValueError as e:
            logger.error(f"Validation error in delete_activity: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in delete_activity: {str(e)}")
            raise

    async def get_activity_types(self) -> List[Dict[str, Any]]:
        """
        Get all activity types from Pipedrive

        Returns:
            List of activity types

        Raises:
            PipedriveAPIError: If the API call fails
        """
        logger.info("ActivityClient: Attempting to get all activity types")

        try:
            response_data = await self.base_client.request(
                "GET", 
                "/activityTypes",
                version="v1"  # Note: Activity Types use v1 API
            )
            
            return response_data.get("data", [])

        except Exception as e:
            logger.error(f"Error in get_activity_types: {str(e)}")
            raise

    async def create_activity_type(
        self,
        name: str,
        icon_key: str,
        color: Optional[str] = None,
        order_nr: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Create a new activity type in Pipedrive

        Args:
            name: Name of the activity type
            icon_key: Icon key for the activity type
            color: Color for the activity type in 6-character HEX format
            order_nr: Order number for sorting activity types

        Returns:
            Created activity type data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"ActivityClient: Attempting to create activity type '{name}'")

        try:
            # Validate required fields
            if not name or not name.strip():
                raise ValueError("Activity type name cannot be empty")
            if not icon_key or not icon_key.strip():
                raise ValueError("Activity type icon_key cannot be empty")

            payload: Dict[str, Any] = {
                "name": name,
                "icon_key": icon_key,
            }
            
            if color is not None:
                payload["color"] = color
            if order_nr is not None:
                payload["order_nr"] = order_nr

            logger.debug(
                f"ActivityClient: create_activity_type payload: {json.dumps(payload, indent=2)}"
            )

            response_data = await self.base_client.request(
                "POST", 
                "/activityTypes", 
                json_payload=payload,
                version="v1"  # Note: Activity Types use v1 API
            )
            
            return response_data.get("data", {})

        except ValueError as e:
            logger.error(f"Validation error in create_activity_type: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in create_activity_type: {str(e)}")
            raise