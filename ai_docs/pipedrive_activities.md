Activities

Run in Postman
Activities are appointments/tasks/events on a calendar that can be associated with a deal, a lead, a person and an organization. Activities can be of different type (such as call, meeting, lunch or a custom type - see ActivityTypes object) and can be assigned to a particular user. Note that activities can also be created without a specific date/time.

Get all activities assigned to a particular user
Copy link
Returns all activities assigned to a particular user.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
10

Request
GET/api/v2/activities
Query parameters
filter_id
integer
If supplied, only activities matching the specified filter are returned

ids
string
Optional comma separated string array of up to 100 entity ids to fetch. If filter_id is provided, this is ignored. If any of the requested entities do not exist or are not visible, they are not included in the response.

owner_id
integer
If supplied, only activities owned by the specified user are returned. If filter_id is provided, this is ignored.

deal_id
integer
If supplied, only activities linked to the specified deal are returned. If filter_id is provided, this is ignored.

lead_id
string
If supplied, only activities linked to the specified lead are returned. If filter_id is provided, this is ignored.

person_id
integer
If supplied, only activities whose primary participant is the given person are returned. If filter_id is provided, this is ignored.

org_id
integer
If supplied, only activities linked to the specified organization are returned. If filter_id is provided, this is ignored.

updated_since
string
If set, only activities with an update_time later than or equal to this time are returned. In RFC3339 format, e.g. 2025-01-01T10:20:00Z.

updated_until
string
If set, only activities with an update_time earlier than this time are returned. In RFC3339 format, e.g. 2025-01-01T10:20:00Z.

sort_by
string
The field to sort by. Supported fields: id, update_time, add_time.

Defaultid
Values

id

update_time

add_time

sort_direction
string
The sorting direction. Supported values: asc, desc.

Defaultasc
Values

asc

desc

include_fields
string
Optional comma separated string array of additional fields to include

Values

attendees

limit
integer
For pagination, the limit of entries to be returned. If not provided, 100 items will be returned. Please note that a maximum value of 500 is allowed.

cursor
string
For pagination, the marker (an opaque string value) representing the first item on the next page

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"subject":"Activity Subject"
"type":"activity_type"
"owner_id":1
"is_deleted":false
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"deal_id":5
"lead_id":"abc-def"
"person_id":6
"org_id":7
"project_id":8
"due_date":"2021-01-01"
"due_time":"15:00:00"
"duration":"01:00:00"
"busy":true
"done":true
"marked_as_done_time":"2021-01-01T00:00:00Z"
"value":"123 Main St"
"country":"USA"
"admin_area_level_1":"CA"
"admin_area_level_2":"Santa Clara"
"locality":"Sunnyvale"
"sublocality":"Downtown"
"route":"Main St"
"street_number":"123"
"postal_code":"94085"
"person_id":1
"primary":true
"email":"some@email.com"
"name":"Some Name"
"status":"accepted"
"is_organizer":true
"person_id":1
"user_id":1
"conference_meeting_client":"google_meet"
"conference_meeting_url":"https://meet.google.com/abc-xyz"
"conference_meeting_id":"abc-xyz"
"public_description":"Public Description"
"priority":263
"note":"Note"
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
Get all activities (BETA)
Copy link
Returns all activities. This is a cursor-paginated endpoint that is currently in BETA. For more information, please refer to our documentation on pagination. Please note that only global admins (those with global permissions) can access these endpoints. Users with regular permissions will receive a 403 response. Read more about global permissions here.

API v1
Cost
10

Request
GET/v1/activities/collection
Query parameters
cursor
string
For pagination, the marker (an opaque string value) representing the first item on the next page

limit
integer
For pagination, the limit of entries to be returned. If not provided, 100 items will be returned. Please note that a maximum value of 500 is allowed.

since
string
The time boundary that points to the start of the range of data. Datetime in ISO 8601 format. E.g. 2022-11-01 08:55:59. Operates on the update_time field.

until
string
The time boundary that points to the end of the range of data. Datetime in ISO 8601 format. E.g. 2022-11-01 08:55:59. Operates on the update_time field.

user_id
integer
The ID of the user whose activities will be fetched. If omitted, all activities are returned.

done
boolean
Whether the activity is done or not. false = Not done, true = Done. If omitted, returns both done and not done activities.

type
string
The type of the activity, can be one type or multiple types separated by a comma. This is in correlation with the key_string parameter of ActivityTypes.

Response
200
OK


Collapse all

Copy code
"success":true
"id":8
"company_id":22122
"user_id":1234
"done":false
"type":"deadline"
"conference_meeting_client":"871b8bc88d3a1202"
"conference_meeting_url":"https://pipedrive.zoom.us/link"
"conference_meeting_id":"17058746701"
"due_date":"2022-06-09"
"due_time":"10:00"
"duration":"01:00"
"busy_flag":true
"add_time":"2020-06-08 12:37:56"
"marked_as_done_time":"2020-08-08 08:08:38"
"subject":"Deadline"
"public_description":"This is a description"
"location":"Mustamäe tee 3, Tallinn, Estonia"
"org_id":5
"person_id":1101
"deal_id":300
"lead_id":"46c3b0e1-db35-59ca-1828-4817378dff71"
"project_id":null
"active_flag":true
"update_time":"2020-08-08 12:37:56"
"update_user_id":5596
"source_timezone":""
"location_subpremise":""
"location_street_number":"3"
"location_route":"Mustamäe tee"
"location_sublocality":"Kristiine"
"location_locality":"Tallinn"
"location_admin_area_level_1":"Harju maakond"
"location_admin_area_level_2":""
"location_country":"Estonia"
"location_postal_code":"10616"
"location_formatted_address":"Mustamäe tee 3, 10616 Tallinn, Estonia"
"next_cursor":"eyJhY3Rpdml0aWVzIjoyN30"
Get details of an activity
Copy link
Returns the details of a specific activity.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
1

Request
GET/api/v2/activities/{id}
Path parameters
id
integer
required
The ID of the activity

Query parameters
include_fields
string
Optional comma separated string array of additional fields to include

Values

attendees

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"subject":"Activity Subject"
"type":"activity_type"
"owner_id":1
"is_deleted":false
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"deal_id":5
"lead_id":"abc-def"
"person_id":6
"org_id":7
"project_id":8
"due_date":"2021-01-01"
"due_time":"15:00:00"
"duration":"01:00:00"
"busy":true
"done":true
"marked_as_done_time":"2021-01-01T00:00:00Z"
"value":"123 Main St"
"country":"USA"
"admin_area_level_1":"CA"
"admin_area_level_2":"Santa Clara"
"locality":"Sunnyvale"
"sublocality":"Downtown"
"route":"Main St"
"street_number":"123"
"postal_code":"94085"
"person_id":1
"primary":true
"email":"some@email.com"
"name":"Some Name"
"status":"accepted"
"is_organizer":true
"person_id":1
"user_id":1
"conference_meeting_client":"google_meet"
"conference_meeting_url":"https://meet.google.com/abc-xyz"
"conference_meeting_id":"abc-xyz"
"public_description":"Public Description"
"priority":263
"note":"Note"
Add an activity
Copy link
Adds a new activity. Includes more_activities_scheduled_in_context property in response's additional_data which indicates whether there are more undone activities scheduled with the same deal, person or organization (depending on the supplied data). For more information, see the tutorial for adding an activity.

Starting from 30.09.2024, activity attendees will receive updates only if the activity owner has an active calendar sync

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
5

Request
POST/api/v2/activities
Body parameters
application/json

subject
string
The subject of the activity

type
string
The type of the activity

owner_id
integer
The ID of the user who owns the activity

deal_id
integer
The ID of the deal linked to the activity

lead_id
string
The ID of the lead linked to the activity

person_id
integer
The ID of the person linked to the activity

org_id
integer
The ID of the organization linked to the activity

project_id
integer
The ID of the project linked to the activity

due_date
string
The due date of the activity

due_time
string
The due time of the activity

duration
string
The duration of the activity

busy
boolean
Whether the activity marks the assignee as busy or not in their calendar

done
boolean
Whether the activity is marked as done or not

location
object
Location of the activity

participants
array
The participants of the activity

attendees
array
The attendees of the activity

public_description
string
The public description of the activity

priority
integer
The priority of the activity. Mappable to a specific string using activityFields API.

note
string
The note of the activity

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"subject":"Activity Subject"
"type":"activity_type"
"owner_id":1
"is_deleted":false
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"deal_id":5
"lead_id":"abc-def"
"person_id":6
"org_id":7
"project_id":8
"due_date":"2021-01-01"
"due_time":"15:00:00"
"duration":"01:00:00"
"busy":true
"done":true
"marked_as_done_time":"2021-01-01T00:00:00Z"
"value":"123 Main St"
"country":"USA"
"admin_area_level_1":"CA"
"admin_area_level_2":"Santa Clara"
"locality":"Sunnyvale"
"sublocality":"Downtown"
"route":"Main St"
"street_number":"123"
"postal_code":"94085"
"person_id":1
"primary":true
"email":"some@email.com"
"name":"Some Name"
"status":"accepted"
"is_organizer":true
"person_id":1
"user_id":1
"conference_meeting_client":"google_meet"
"conference_meeting_url":"https://meet.google.com/abc-xyz"
"conference_meeting_id":"abc-xyz"
"public_description":"Public Description"
"priority":263
"note":"Note"
Update an activity
Copy link
Updates an activity. Includes more_activities_scheduled_in_context property in response's additional_data which indicates whether there are more undone activities scheduled with the same deal, person or organization (depending on the supplied data).

Starting from 30.09.2024, activity attendees will receive updates only if the activity owner has an active calendar sync

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
5

Request
PATCH/api/v2/activities/{id}
Path parameters
id
integer
required
The ID of the activity

Body parameters
application/json

subject
string
The subject of the activity

type
string
The type of the activity

owner_id
integer
The ID of the user who owns the activity

deal_id
integer
The ID of the deal linked to the activity

lead_id
string
The ID of the lead linked to the activity

person_id
integer
The ID of the person linked to the activity

org_id
integer
The ID of the organization linked to the activity

project_id
integer
The ID of the project linked to the activity

due_date
string
The due date of the activity

due_time
string
The due time of the activity

duration
string
The duration of the activity

busy
boolean
Whether the activity marks the assignee as busy or not in their calendar

done
boolean
Whether the activity is marked as done or not

location
object
Location of the activity

participants
array
The participants of the activity

attendees
array
The attendees of the activity

public_description
string
The public description of the activity

priority
integer
The priority of the activity. Mappable to a specific string using activityFields API.

note
string
The note of the activity

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"subject":"Activity Subject"
"type":"activity_type"
"owner_id":1
"is_deleted":false
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"deal_id":5
"lead_id":"abc-def"
"person_id":6
"org_id":7
"project_id":8
"due_date":"2021-01-01"
"due_time":"15:00:00"
"duration":"01:00:00"
"busy":true
"done":true
"marked_as_done_time":"2021-01-01T00:00:00Z"
"value":"123 Main St"
"country":"USA"
"admin_area_level_1":"CA"
"admin_area_level_2":"Santa Clara"
"locality":"Sunnyvale"
"sublocality":"Downtown"
"route":"Main St"
"street_number":"123"
"postal_code":"94085"
"person_id":1
"primary":true
"email":"some@email.com"
"name":"Some Name"
"status":"accepted"
"is_organizer":true
"person_id":1
"user_id":1
"conference_meeting_client":"google_meet"
"conference_meeting_url":"https://meet.google.com/abc-xyz"
"conference_meeting_id":"abc-xyz"
"public_description":"Public Description"
"priority":263
"note":"Note"
Delete multiple activities in bulk
Copy link
Marks multiple activities as deleted. After 30 days, the activities will be permanently deleted.

API v1
Cost
10

Request
DELETE/v1/activities
Query parameters
ids
string
required
The comma-separated IDs of activities that will be deleted

Response
200
OK


Collapse all

Copy code
"success":true
625
627
Delete an activity
Copy link
Marks an activity as deleted. After 30 days, the activity will be permanently deleted.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
3

Request
DELETE/api/v2/activities/{id}
Path parameters
id
integer
required
The ID of the activity

Response
200
OK


Collapse all

Copy code
"success":true
"id":1


ActivityFields

Run in Postman
Activity fields represent different fields that an activity has.

Get all activity fields
Copy link
Returns all activity fields.

API v1
Cost
20

Request
GET/v1/activityFields
Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"key":"title"
"name":"Title"
"order_nr":2
"field_type":"varchar"
"add_time":"2019-02-04 13:58:03"
"update_time":"2019-02-04 13:58:03"
"last_updated_by_user_id":1
"created_by_user_id":1
"active_flag":true
"edit_flag":false
"index_visible_flag":true
"details_visible_flag":true
"add_visible_flag":true
"important_flag":false
"bulk_edit_allowed":true
"searchable_flag":false
"filtering_allowed":true
"sortable_flag":true
"options":null
"mandatory_flag":true
"id":2
"key":"9dc80c50d78a15643bfc4ca79d76156a73a1ca0e"
"name":"Customer Type"
"order_nr":1
"field_type":"enum"
"add_time":"2019-02-04 13:58:03"
"update_time":"2019-02-04 13:58:03"
"last_updated_by_user_id":1
"created_by_user_id":1
"active_flag":true
"edit_flag":true
"index_visible_flag":true
"details_visible_flag":true
"add_visible_flag":false
"important_flag":false
"bulk_edit_allowed":true
"searchable_flag":false
"filtering_allowed":true
"sortable_flag":true
"id":190
"label":"Private person"
"id":191
"label":"Company"
"id":192
"label":"Government"
"mandatory_flag":true
"start":0
"limit":100
"more_items_in_collection":false

ActivityTypes

Run in Postman
Activity types represent different kinds of activities that can be stored. Each activity type is presented to the user with an icon and a name. Additionally, a color can be defined (not implemented in the Pipedrive app as of today). Activity types are linked to activities via ActivityType.key_string = Activity.type. The key_string will be generated by the API based on the given name of the activity type upon creation, and cannot be changed. Activity types should be presented to the user in an ordered manner, using the ActivityType.order_nr value.

Get all activity types
Copy link
Returns all activity types.

API v1
Cost
20

Request
GET/v1/activityTypes
Response
200
OK


Collapse all

Copy code
"success":true
"id":4
"order_nr":1
"name":"Deadline"
"key_string":"deadline"
"icon_key":"deadline"
"active_flag":true
"color":"FFFFFF"
"is_custom_flag":false
"add_time":"2019-10-04 16:24:55"
"update_time":"2020-03-11 13:53:01"
"id":5
"order_nr":2
"name":"Call"
"key_string":"call"
"icon_key":"call"
"active_flag":true
"color":"FFFFFF"
"is_custom_flag":false
"add_time":"2019-12-21 19:44:01"
"update_time":"2019-12-21 19:44:01"
Add new activity type
Copy link
Adds a new activity type.

API v1
Cost
10

Request
POST/v1/activityTypes
Body parameters
application/json

name
string
required
The name of the activity type

icon_key
string
required
Icon graphic to use for representing this activity type

Values

task

email

meeting

deadline

call

lunch

calendar

downarrow

document

smartphone

camera

scissors

cogs

bubble

uparrow

checkbox

signpost

shuffle

addressbook

linegraph

picture

car

world

search

clip

sound

brush

key

padlock

pricetag

suitcase

finish

plane

loop

wifi

truck

cart

bulb

bell

presentation

color
string
A designated color for the activity type in 6-character HEX format (e.g. FFFFFF for white, 000000 for black)

Response
200
OK


Collapse all

Copy code
"success":true
"id":12
"order_nr":1
"name":"Video call"
"key_string":"video_call"
"icon_key":"camera"
"active_flag":true
"color":"aeb31b"
"is_custom_flag":true
"add_time":"2020-09-01 10:16:23"
"update_time":"2020-09-01 10:16:23"
Update an activity type
Copy link
Updates an activity type.

API v1
Cost
10

Request
PUT/v1/activityTypes/{id}
Path parameters
id
integer
required
The ID of the activity type

Body parameters
application/json

name
string
The name of the activity type

icon_key
string
Icon graphic to use for representing this activity type

Values

task

email

meeting

deadline

call

lunch

calendar

downarrow

document

smartphone

camera

scissors

cogs

bubble

uparrow

checkbox

signpost

shuffle

addressbook

linegraph

picture

car

world

search

clip

sound

brush

key

padlock

pricetag

suitcase

finish

plane

loop

wifi

truck

cart

bulb

bell

presentation

color
string
A designated color for the activity type in 6-character HEX format (e.g. FFFFFF for white, 000000 for black)

order_nr
integer
An order number for this activity type. Order numbers should be used to order the types in the activity type selections.

Response
200
OK


Collapse all

Copy code
"success":true
"id":12
"order_nr":1
"name":"Video call"
"key_string":"video_call"
"icon_key":"camera"
"active_flag":true
"color":"aeb31b"
"is_custom_flag":true
"add_time":"2020-09-01 10:16:23"
"update_time":"2020-09-01 14:12:09"
Delete multiple activity types in bulk
Copy link
Marks multiple activity types as deleted.

API v1
Cost
10

Request
DELETE/v1/activityTypes
Query parameters
ids
string
required
The comma-separated activity type IDs

Response
200
OK


Collapse all

Copy code
"success":true
1
2
3
Delete an activity type
Copy link
Marks an activity type as deleted.

API v1
Cost
6

Request
DELETE/v1/activityTypes/{id}
Path parameters
id
integer
required
The ID of the activity type

Response
200
OK


Collapse all

Copy code
"success":true
"id":12
"order_nr":1
"name":"Video call"
"key_string":"video_call"
"icon_key":"camera"
"active_flag":false
"color":"aeb31b"
"is_custom_flag":true
"add_time":"2020-09-01 10:16:23"
"update_time":"2020-09-01 19:59:59"

