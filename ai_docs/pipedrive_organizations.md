Organizations

Run in Postman
Organizations are companies and other kinds of organizations you are making deals with. Persons can be associated with organizations so that each organization can contain one or more persons.

Get all organizations
Copy link
Returns data about all organizations.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
10

Request
GET/api/v2/organizations
Query parameters
filter_id
integer
If supplied, only organizations matching the specified filter are returned

ids
string
Optional comma separated string array of up to 100 entity ids to fetch. If filter_id is provided, this is ignored. If any of the requested entities do not exist or are not visible, they are not included in the response.

owner_id
integer
If supplied, only organization owned by the specified user are returned. If filter_id is provided, this is ignored.

updated_since
string
If set, only organizations with an update_time later than or equal to this time are returned. In RFC3339 format, e.g. 2025-01-01T10:20:00Z.

updated_until
string
If set, only organizations with an update_time earlier than this time are returned. In RFC3339 format, e.g. 2025-01-01T10:20:00Z.

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

next_activity_id

last_activity_id

open_deals_count

related_open_deals_count

closed_deals_count

related_closed_deals_count

email_messages_count

people_count

activities_count

done_activities_count

undone_activities_count

files_count

notes_count

followers_count

won_deals_count

related_won_deals_count

lost_deals_count

related_lost_deals_count

custom_fields
string
Optional comma separated string array of custom fields keys to include. If you are only interested in a particular set of custom fields, please use this parameter for faster results and smaller response.
A maximum of 15 keys is allowed.

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
"name":"Organization Name"
"owner_id":1
"org_id":1
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"value":"123 Main St"
"country":"USA"
"admin_area_level_1":"CA"
"admin_area_level_2":"Santa Clara"
"locality":"Sunnyvale"
"sublocality":"Downtown"
"route":"Main St"
"street_number":"123"
"postal_code":"94085"
"is_deleted":false
"visible_to":7
1
2
3
"custom_fields":
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
Get all organizations collection
Copy link
Returns all organizations. Please note that only global admins (those with global permissions) can access this endpoint. Users with regular permissions will receive a 403 response. Read more about global permissions here.
This endpoint has been deprecated. Please use GET /api/v2/organizations instead.

Deprecated endpoint

Cost
10

Request
GET/v1/organizations/collection
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

owner_id
integer
If supplied, only organizations owned by the given user will be returned

first_char
string
If supplied, only organizations whose name starts with the specified letter will be returned (case-insensitive)

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"active_flag":true
"owner_id":123
"name":"Pipedrive"
"update_time":"2023-02-08 05:30:20"
"delete_time":null
"add_time":"2023-01-08 05:30:20"
"visible_to":"3"
"label":1
"address":"Mustamäe tee 3a, 10615 Tallinn"
"address_subpremise":""
"address_street_number":"3a"
"address_route":"Mustamäe tee"
"address_sublocality":"Kristiine"
"address_locality":"Tallinn"
"address_admin_area_level_1":"Harju maakond"
"address_admin_area_level_2":""
"address_country":"Estonia"
"address_postal_code":"10616"
"address_formatted_address":"Mustamäe tee 3a, 10616 Tallinn, Estonia"
"cc_email":"org@pipedrivemail.com"
"next_cursor":"eyJhY3Rpdml0aWVzIjoyN30"
Search organizations
Copy link
Searches all organizations by name, address, notes and/or custom fields. This endpoint is a wrapper of /v1/itemSearch with a narrower OAuth scope.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
20

Request
GET/api/v2/organizations/search
Query parameters
term
string
required
The search term to look for. Minimum 2 characters (or 1 if using exact_match). Please note that the search term has to be URL encoded.

fields
string
A comma-separated string array. The fields to perform the search from. Defaults to all of them. Only the following custom field types are searchable: address, varchar, text, varchar_auto, double, monetary and phone. Read more about searching by custom fields here.

Values

address

custom_fields

notes

name

exact_match
boolean
When enabled, only full exact matches against the given term are returned. It is not case sensitive.

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
"result_score":0.316
"id":1
"type":"organization"
"name":"Organization name"
"address":"Mustamäe tee 3a, 10615 Tallinn"
"visible_to":3
"id":1
"custom_fields":
"notes":
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
Get details of an organization
Copy link
Returns the details of a specific organization.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
1

Request
GET/api/v2/organizations/{id}
Path parameters
id
integer
required
The ID of the organization

Query parameters
include_fields
string
Optional comma separated string array of additional fields to include

Values

next_activity_id

last_activity_id

open_deals_count

related_open_deals_count

closed_deals_count

related_closed_deals_count

email_messages_count

people_count

activities_count

done_activities_count

undone_activities_count

files_count

notes_count

followers_count

won_deals_count

related_won_deals_count

lost_deals_count

related_lost_deals_count

custom_fields
string
Optional comma separated string array of custom fields keys to include. If you are only interested in a particular set of custom fields, please use this parameter for faster results and smaller response.
A maximum of 15 keys is allowed.

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"name":"Organization Name"
"owner_id":1
"org_id":1
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"value":"123 Main St"
"country":"USA"
"admin_area_level_1":"CA"
"admin_area_level_2":"Santa Clara"
"locality":"Sunnyvale"
"sublocality":"Downtown"
"route":"Main St"
"street_number":"123"
"postal_code":"94085"
"is_deleted":false
"visible_to":7
1
2
3
"custom_fields":
List activities associated with an organization
Copy link
Lists activities associated with an organization.
This endpoint has been deprecated. Please use GET /api/v2/activities?org_id={id} instead.

Deprecated endpoint

Cost
20

Request
GET/v1/organizations/{id}/activities
Path parameters
id
integer
required
The ID of the organization

Query parameters
start
integer
Pagination start

Default0
limit
integer
Items shown per page

done
number
Whether the activity is done or not. 0 = Not done, 1 = Done. If omitted returns both Done and Not done activities.

Values

0

1

exclude
string
A comma-separated string of activity IDs to exclude from result

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
"reference_type":"scheduler-service"
"reference_id":7
"conference_meeting_client":"871b8bc88d3a1202"
"conference_meeting_url":"https://pipedrive.zoom.us/link"
"conference_meeting_id":"17058746701"
"due_date":"2020-06-09"
"due_time":"10:00"
"duration":"01:00"
"busy_flag":true
"add_time":"2020-06-08 12:37:56"
"marked_as_done_time":"2020-08-08 08:08:38"
"last_notification_time":"2020-08-08 12:37:56"
"last_notification_user_id":7655
"notification_language_id":1
"subject":"Deadline"
"public_description":"This is a description"
"calendar_sync_include_context":""
"location":"Mustamäe tee 3, Tallinn, Estonia"
"org_id":5
"person_id":1101
"deal_id":300
"lead_id":"46c3b0e1-db35-59ca-1828-4817378dff71"
"project_id":null
"active_flag":true
"update_time":"2020-08-08 12:37:56"
"update_user_id":5596
"gcal_event_id":""
"google_calendar_id":""
"google_calendar_etag":""
"source_timezone":""
"rec_rule":"RRULE:FREQ=WEEKLY;BYDAY=WE"
"rec_rule_extension":""
"rec_master_activity_id":1
"series":
"note":"A note for the activity"
"created_by_user_id":1234
"location_subpremise":""
"location_street_number":"3"
"location_route":"Mustamäe tee"
"location_sublocality":"Kristiine"
"location_locality":"Tallinn"
"person_dropbox_bcc":"company@pipedrivemail.com"
"deal_dropbox_bcc":"company+deal300@pipedrivemail.com"
"assigned_to_user_id":1235
"id":"376892,"
"clean_name":"Audio 10:55:07.m4a"
"url":"https://pipedrive-files.s3-eu-west-1.amazonaws.com/Audio-recording.m4a"
"call":2
"meeting":1
"name":"Will Smith"
"activity_count":3
"share":100
"start":0
"limit":100
"more_items_in_collection":true
List updates about organization field values
Copy link
Lists updates about field values of an organization.

API v1
Cost
20

Request
GET/v1/organizations/{id}/changelog
Path parameters
id
integer
required
The ID of the organization

Query parameters
cursor
string
For pagination, the marker (an opaque string value) representing the first item on the next page

limit
integer
Items shown per page

Response
200
OK


Collapse all

Copy code
"success":true
"field_key":"name"
"old_value":"Org 10"
"new_value":"Org 11"
"actor_user_id":26
"time":"2024-02-12 09:14:35"
"change_source":"app"
"change_source_user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
"is_bulk_update_flag":false
"field_key":"51c27e4a19c3bedd91162a9d446707c1f95174ea"
"old_value":"0"
"new_value":"20"
"actor_user_id":26
"time":"2024-02-12 09:10:12"
"change_source":"app"
"change_source_user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
"is_bulk_update_flag":false
"next_cursor":"aWQ6NTQ0"
List deals associated with an organization
Copy link
Lists deals associated with an organization.
This endpoint has been deprecated. Please use GET /api/v2/deals?org_id={id} instead.

Deprecated endpoint

Cost
20

Request
GET/v1/organizations/{id}/deals
Path parameters
id
integer
required
The ID of the organization

Query parameters
start
integer
Pagination start

Default0
limit
integer
Items shown per page

status
string
Only fetch deals with a specific status. If omitted, all not deleted deals are returned. If set to deleted, deals that have been deleted up to 30 days ago will be included.

Defaultall_not_deleted
Values

open

won

lost

deleted

all_not_deleted

sort
string
The field names and sorting mode separated by a comma (field_name_1 ASC, field_name_2 DESC). Only first-level field keys are supported (no nested keys).

only_primary_association
number
If set, only deals that are directly associated to the organization are fetched. If not set (default), all deals are fetched that are either directly or indirectly related to the organization. Indirect relations include relations through custom, organization-type fields and through persons of the given organization.

Values

0

1

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"id":8877
"name":"Creator"
"email":"john.doe@pipedrive.com"
"has_pic":false
"pic_hash":null
"active_flag":true
"value":8877
"id":8877
"name":"Creator"
"email":"john.doe@pipedrive.com"
"has_pic":false
"pic_hash":null
"active_flag":true
"value":8877
"active_flag":true
"name":"Person"
"label":"work"
"value":"person@pipedrive.com"
"primary":true
"label":"work"
"value":"37244499911"
"primary":true
"value":1101
"name":"Organization"
"people_count":2
"owner_id":8877
"address":"Mustamäe tee 3a, 10615 Tallinn"
"active_flag":true
"cc_email":"org@pipedrivemail.com"
"value":5
"stage_id":2
"title":"Deal One"
"value":5000
"currency":"EUR"
"add_time":"2019-05-29 04:21:51"
"update_time":"2019-11-28 16:19:50"
"stage_change_time":"2019-11-28 15:41:22"
"active":true
"deleted":false
"status":"open"
"probability":null
"next_activity_date":"2019-11-29"
"next_activity_time":"11:30:00"
"next_activity_id":128
"last_activity_id":null
"last_activity_date":null
"lost_reason":null
"visible_to":"1"
"close_time":null
"pipeline_id":1
"won_time":"2019-11-27 11:40:36"
"first_won_time":"2019-11-27 11:40:36"
"lost_time":"2019-11-27 11:40:36"
"products_count":0
"files_count":0
"notes_count":2
"followers_count":0
"email_messages_count":4
"activities_count":1
"done_activities_count":0
"undone_activities_count":1
"participants_count":1
"expected_close_date":"2019-06-29"
"last_incoming_mail_time":"2019-05-29 18:21:42"
"last_outgoing_mail_time":"2019-05-30 03:45:35"
"label":"11"
"stage_order_nr":2
"person_name":"Person"
"org_name":"Organization"
"next_activity_subject":"Call"
"next_activity_type":"call"
"owner_name":"Creator"
"cc_email":"company+deal1@pipedrivemail.com"
"org_hidden":false
"person_hidden":false
"start":0
"limit":100
"more_items_in_collection":true
"id":8877
"name":"Creator"
"email":"john.doe@pipedrive.com"
"has_pic":false
"pic_hash":null
"active_flag":true
"id":5
"name":"Organization"
"people_count":2
"owner_id":8877
"address":"Mustamäe tee 3a, 10615 Tallinn"
"active_flag":true
"cc_email":"org@pipedrivemail.com"
"active_flag":true
"id":1101
"name":"Person"
"label":"work"
"value":"person@pipedrive.com"
"primary":true
"label":"work"
"value":"3421787767"
"primary":true
"owner_id":8877
"id":2
"company_id":123
"order_nr":1
"name":"Stage Name"
"active_flag":true
"deal_probability":100
"pipeline_id":1
"rotten_flag":false
"rotten_days":null
"add_time":"2015-12-08 13:54:06"
"update_time":"2015-12-08 13:54:06"
"pipeline_name":"Pipeline"
"pipeline_deal_probability":true
"id":1
"name":"Pipeline"
"url_title":"Pipeline"
"order_nr":0
"active":true
"deal_probability":true
"add_time":"2015-12-08 10:00:24"
"update_time":"2015-12-08 10:00:24"
List files attached to an organization
Copy link
Lists files associated with an organization.

API v1
Cost
20

Request
GET/v1/organizations/{id}/files
Path parameters
id
integer
required
The ID of the organization

Query parameters
start
integer
Pagination start

Default0
limit
integer
Items shown per page. Please note that a maximum value of 100 is allowed.

sort
string
Supported fields: id, update_time

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"user_id":8877
"deal_id":1
"person_id":1
"org_id":1480
"product_id":1
"activity_id":1
"lead_id":"adf21080-0e10-11eb-879b-05d71fb426ec"
"log_id":null
"add_time":"2020-09-16 11:19:36"
"update_time":"2020-09-16 11:19:36"
"file_name":"95781006_794143070992462_4330873630616453120_n_60817458877506f9eb74d03e5ef9ba061915b797998.jpg"
"file_type":"img"
"file_size":95116
"active_flag":true
"inline_flag":false
"remote_location":"s3"
"remote_id":"95781006_794143070992462_4330873630616453120_n.jpg"
"cid":""
"s3_bucket":""
"mail_message_id":""
"mail_template_id":""
"deal_name":"nice deal"
"person_name":""
"people_name":""
"org_name":"Pipedrive Inc."
"product_name":""
"lead_name":"nice lead"
"url":"https://app.pipedrive.com/api/v1/files/304/download"
"name":"95781006_794143070992462_4330873630616453120_n.jpg"
"description":""
"start":0
"limit":100
"more_items_in_collection":true
List updates about an organization
Copy link
Lists updates about an organization.

API v1
Cost
40

Request
GET/v1/organizations/{id}/flow
Path parameters
id
integer
required
The ID of the organization

Query parameters
start
integer
Pagination start

Default0
limit
integer
Items shown per page

all_changes
string
Whether to show custom field updates or not. 1 = Include custom field changes. If omitted, returns changes without custom field updates.

items
string
A comma-separated string for filtering out item specific updates. (Possible values - activity, plannedActivity, note, file, change, deal, follower, participant, mailMessage, mailMessageWithAttachment, invoice, activityFile, document).

Response
200
OK


Collapse all

Copy code
"success":true
"object":"organizationChange"
"timestamp":"2020-09-15 11:55:14"
"id":3694
"item_id":1480
"user_id":9271535
"field_key":"owner_id"
"old_value":9271535
"new_value":8877
"is_bulk_update_flag":null
"log_time":"2020-09-15 11:55:14"
"change_source":"app"
"change_source_user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML like Gecko) Chrome/84.0.4147.135 Safari/537.36"
"new_value_formatted":"Will Smith"
"old_value_formatted":"Robert Smith"
"object":"activity"
"timestamp":"2020-08-07 08:15:00"
"id":8
"company_id":22122
"user_id":1234
"done":false
"type":"deadline"
"reference_type":"scheduler-service"
"reference_id":7
"conference_meeting_client":"871b8bc88d3a1202"
"conference_meeting_url":"https://pipedrive.zoom.us/link"
"conference_meeting_id":"17058746701"
"due_date":"2020-06-09"
"due_time":"10:00"
"duration":"01:00"
"busy_flag":true
"add_time":"2020-06-08 12:37:56"
"marked_as_done_time":"2020-08-08 08:08:38"
"last_notification_time":"2020-08-08 12:37:56"
"last_notification_user_id":7655
"notification_language_id":1
"subject":"Deadline"
"public_description":"This is a description"
"calendar_sync_include_context":""
"location":"Mustamäe tee 3, Tallinn, Estonia"
"org_id":5
"person_id":1101
"deal_id":300
"lead_id":"46c3b0e1-db35-59ca-1828-4817378dff71"
"project_id":null
"active_flag":true
"update_time":"2020-08-08 12:37:56"
"update_user_id":5596
"gcal_event_id":""
"google_calendar_id":""
"google_calendar_etag":""
"source_timezone":""
"rec_rule":"RRULE:FREQ=WEEKLY;BYDAY=WE"
"rec_rule_extension":""
"rec_master_activity_id":1
"series":
"note":"A note for the activity"
"created_by_user_id":1234
"location_subpremise":""
"location_street_number":"3"
"location_route":"Mustamäe tee"
"location_sublocality":"Kristiine"
"location_locality":"Tallinn"
"person_dropbox_bcc":"company@pipedrivemail.com"
"deal_dropbox_bcc":"company+deal300@pipedrivemail.com"
"assigned_to_user_id":1235
"id":"376892,"
"clean_name":"Audio 10:55:07.m4a"
"url":"https://pipedrive-files.s3-eu-west-1.amazonaws.com/Audio-recording.m4a"
"object":"file"
"timestamp":"2020-08-10 11:52:26"
"id":1
"user_id":8877
"deal_id":1
"person_id":1
"org_id":1480
"product_id":1
"activity_id":1
"lead_id":"adf21080-0e10-11eb-879b-05d71fb426ec"
"log_id":null
"add_time":"2020-09-16 11:19:36"
"update_time":"2020-09-16 11:19:36"
"file_name":"95781006_794143070992462_4330873630616453120_n_60817458877506f9eb74d03e5ef9ba061915b797998.jpg"
"file_type":"img"
"file_size":95116
"active_flag":true
"inline_flag":false
"remote_location":"s3"
"remote_id":"95781006_794143070992462_4330873630616453120_n.jpg"
"cid":""
"s3_bucket":""
"mail_message_id":""
"mail_template_id":""
"deal_name":"nice deal"
"person_name":""
"people_name":""
"org_name":"Pipedrive Inc."
"product_name":""
"lead_name":"nice lead"
"url":"https://app.pipedrive.com/api/v1/files/304/download"
"name":"95781006_794143070992462_4330873630616453120_n.jpg"
"description":""
"start":0
"limit":100
"more_items_in_collection":true
"id":123
"name":"Jane Doe"
"email":"jane@pipedrive.com"
"has_pic":1
"pic_hash":"2611ace8ac6a3afe2f69ed56f9e08c6b"
"active_flag":true
"id":1
"name":"Org Name"
"people_count":1
"owner_id":123
"address":"Mustamäe tee 3a, 10615 Tallinn"
"active_flag":true
"cc_email":"org@pipedrivemail.com"
List followers of an organization
Copy link
Lists users who are following the organization.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
10

Request
GET/api/v2/organizations/{id}/followers
Path parameters
id
integer
required
The ID of the organization

Query parameters
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
"user_id":1
"add_time":"2021-01-01T00:00:00Z"
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
List mail messages associated with an organization
Copy link
Lists mail messages associated with an organization.

API v1
Cost
20

Request
GET/v1/organizations/{id}/mailMessages
Path parameters
id
integer
required
The ID of the organization

Query parameters
start
integer
Pagination start

Default0
limit
integer
Items shown per page

Response
200
OK


Collapse all

Copy code
"success":true
"object":"mailMessage"
"timestamp":"2020-09-16 13:38:17"
"id":1
"id":1
"email_address":"mail@example.org"
"name":"Test"
"linked_person_id":1
"linked_person_name":""
"mail_message_party_id":1
"id":1
"email_address":"mail@example.org"
"name":"Test"
"linked_person_id":1
"linked_person_name":""
"mail_message_party_id":1
"id":1
"email_address":"mail@example.org"
"name":"Test"
"linked_person_id":1
"linked_person_name":""
"mail_message_party_id":1
"id":1
"email_address":"mail@example.org"
"name":"Test"
"linked_person_id":1
"linked_person_name":""
"mail_message_party_id":1
"body_url":"https://example.org"
"nylas_id":"8cfw8n7l4iy24xxxxxxxxx"
"account_id":"ao5gpry0zykr1xxxxxxxxx"
"user_id":1
"mail_thread_id":1
"subject":"test subject"
"snippet":"test subject"
"mail_tracking_status":"opened"
"mail_link_tracking_enabled_flag":0
"read_flag":1
"draft":""
"s3_bucket":"pipedrive-mail-live-fr"
"s3_bucket_path":"e9cf-6081745/77777/nylas/111/1111/body"
"draft_flag":0
"synced_flag":1
"deleted_flag":0
"external_deleted_flag":false
"has_body_flag":1
"sent_flag":0
"sent_from_pipedrive_flag":0
"smart_bcc_flag":0
"message_time":"2019-11-14T06:02:06.000Z"
"add_time":"2019-11-14T06:02:06.000Z"
"update_time":"2019-11-14T07:15:49.000Z"
"has_attachments_flag":1
"has_inline_attachments_flag":0
"has_real_attachments_flag":1
"mua_message_id":"8cfw8n7l4iy24lfhnexxxxxx-0@mailer.nylas.com"
"template_id":1
"item_type":"mailMessage"
"timestamp":"2020-09-16T13:37:50.000Z"
"company_id":6081745
"start":0
"limit":100
"more_items_in_collection":true
List permitted users
Copy link
List users permitted to access an organization.

API v1
Cost
10

Request
GET/v1/organizations/{id}/permittedUsers
Path parameters
id
integer
required
The ID of the organization

Response
200
OK


Collapse all

Copy code
"success":true
123
777
List persons of an organization
Copy link
Lists persons associated with an organization.
If a company uses the Campaigns product, then this endpoint will also return the data.marketing_status field.
This endpoint has been deprecated. Please use GET /api/v2/persons?org_id={id} instead.

Deprecated endpoint

Cost
20

Request
GET/v1/organizations/{id}/persons
Path parameters
id
integer
required
The ID of the organization

Query parameters
start
integer
Pagination start

Default0
limit
integer
Items shown per page

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"company_id":12
"id":123
"name":"Jane Doe"
"email":"jane@pipedrive.com"
"has_pic":1
"pic_hash":"2611ace8ac6a3afe2f69ed56f9e08c6b"
"active_flag":true
"value":123
"name":"Org Name"
"people_count":1
"owner_id":123
"address":"Mustamäe tee 3a, 10615 Tallinn"
"active_flag":true
"cc_email":"org@pipedrivemail.com"
"value":1234
"name":"Will Smith"
"first_name":"Will"
"last_name":"Smith"
"open_deals_count":2
"related_open_deals_count":2
"closed_deals_count":3
"related_closed_deals_count":3
"participant_open_deals_count":1
"participant_closed_deals_count":1
"email_messages_count":1
"activities_count":1
"done_activities_count":1
"undone_activities_count":2
"files_count":2
"notes_count":2
"followers_count":3
"won_deals_count":3
"related_won_deals_count":3
"lost_deals_count":1
"related_lost_deals_count":1
"active_flag":true
"value":"12345"
"primary":true
"label":"work"
"value":"12345@email.com"
"primary":true
"label":"work"
"primary_email":"12345@email.com"
"first_char":"w"
"update_time":"2020-05-08 05:30:20"
"add_time":"2017-10-18 13:23:07"
"visible_to":"3"
"marketing_status":"no_consent"
"item_type":"person"
"item_id":25
"active_flag":true
"add_time":"2020-09-08 08:17:52"
"update_time":"0000-00-00 00:00:00"
"added_by_user_id":967055
"128":"https://pipedrive-profile-pics.s3.example.com/f8893852574273f2747bf6ef09d11cfb4ac8f269_128.jpg"
"512":"https://pipedrive-profile-pics.s3.example.com/f8893852574273f2747bf6ef09d11cfb4ac8f269_512.jpg"
"value":4
"next_activity_date":"2019-11-29"
"next_activity_time":"11:30:00"
"next_activity_id":128
"last_activity_id":34
"last_activity_date":"2019-11-28"
"last_incoming_mail_time":"2019-05-29 18:21:42"
"last_outgoing_mail_time":"2019-05-30 03:45:35"
"label":1
1
2
3
"org_name":"Organization name"
"owner_name":"Jane Doe"
"cc_email":"org@pipedrivemail.com"
"start":0
"limit":100
"more_items_in_collection":true
"id":1
"name":"Org Name"
"people_count":1
"owner_id":123
"address":"Mustamäe tee 3a, 10615 Tallinn"
"active_flag":true
"cc_email":"org@pipedrivemail.com"
"id":123
"name":"Jane Doe"
"email":"jane@pipedrive.com"
"has_pic":1
"pic_hash":"2611ace8ac6a3afe2f69ed56f9e08c6b"
"active_flag":true
List followers changelog of an organization
Copy link
Lists changelogs about users have followed the organization.

API v2
Cost
10

Request
GET/api/v2/organizations/{id}/followers/changelog
Path parameters
id
integer
required
The ID of the organization

Query parameters
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
"action":"added"
"actor_user_id":1
"follower_user_id":1
"time":"2024-01-01T00:00:00Z"
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
Add an organization
Copy link
Adds a new organization.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
5

Request
POST/api/v2/organizations
Body parameters
application/json

name
string
The name of the organization

owner_id
integer
The ID of the user who owns the organization

add_time
string
The creation date and time of the organization

update_time
string
The last updated date and time of the organization

visible_to
integer
The visibility of the organization

label_ids
array
The IDs of labels assigned to the organization

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"name":"Organization Name"
"owner_id":1
"org_id":1
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"value":"123 Main St"
"country":"USA"
"admin_area_level_1":"CA"
"admin_area_level_2":"Santa Clara"
"locality":"Sunnyvale"
"sublocality":"Downtown"
"route":"Main St"
"street_number":"123"
"postal_code":"94085"
"is_deleted":false
"visible_to":7
1
2
3
"custom_fields":
Add a follower to an organization
Copy link
Adds a user as a follower to the organization.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
5

Request
POST/api/v2/organizations/{id}/followers
Path parameters
id
integer
required
The ID of the organization

Body parameters
application/json

user_id
integer
required
The ID of the user to add as a follower

Response
201
Created


Collapse all

Copy code
"success":true
"user_id":1
"add_time":"2021-01-01T00:00:00Z"
Update an organization
Copy link
Updates the properties of a organization.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
5

Request
PATCH/api/v2/organizations/{id}
Path parameters
id
integer
required
The ID of the organization

Body parameters
application/json

name
string
The name of the organization

owner_id
integer
The ID of the user who owns the organization

add_time
string
The creation date and time of the organization

update_time
string
The last updated date and time of the organization

visible_to
integer
The visibility of the organization

label_ids
array
The IDs of labels assigned to the organization

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"name":"Organization Name"
"owner_id":1
"org_id":1
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"value":"123 Main St"
"country":"USA"
"admin_area_level_1":"CA"
"admin_area_level_2":"Santa Clara"
"locality":"Sunnyvale"
"sublocality":"Downtown"
"route":"Main St"
"street_number":"123"
"postal_code":"94085"
"is_deleted":false
"visible_to":7
1
2
3
"custom_fields":
Merge two organizations
Copy link
Merges an organization with another organization. For more information, see the tutorial for merging two organizations.

API v1
Cost
40

Request
PUT/v1/organizations/{id}/merge
Path parameters
id
integer
required
The ID of the organization

Body parameters
application/json

merge_with_id
integer
required
The ID of the organization that the organization will be merged with

Response
200
OK


Collapse all

Copy code
"success":true
"id":123
Delete multiple organizations in bulk
Copy link
Marks multiple organizations as deleted. After 30 days, the organizations will be permanently deleted.
This endpoint has been deprecated. Please use DELETE /api/v2/organizations/{id} instead.

Deprecated endpoint

Cost
10

Request
DELETE/v1/organizations
Query parameters
ids
string
required
The comma-separated IDs that will be deleted

Response
200
OK


Collapse all

Copy code
"success":true
123
100
Delete an organization
Copy link
Marks a organization as deleted. After 30 days, the organization will be permanently deleted.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
3

Request
DELETE/api/v2/organizations/{id}
Path parameters
id
integer
required
The ID of the organization

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
Delete a follower from an organization
Copy link
Deletes a user follower from the organization.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
3

Request
DELETE/api/v2/organizations/{id}/followers/{follower_id}
Path parameters
id
integer
required
The ID of the organization

follower_id
integer
required
The ID of the following user

Response
200
OK


Collapse all

Copy code
"success":true
"user_id":1