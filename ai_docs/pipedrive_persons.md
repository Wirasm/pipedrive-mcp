Persons

Run in Postman
Persons are your contacts, the customers you are doing deals with. Each person can belong to an organization. Persons should not be confused with users.

Get all persons
Copy link
Returns data about all persons. Fields ims, postal_address, notes, birthday, and job_title are only included if contact sync is enabled for the company.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
10

Request
GET/api/v2/persons
Query parameters
filter_id
integer
If supplied, only persons matching the specified filter are returned

ids
string
Optional comma separated string array of up to 100 entity ids to fetch. If filter_id is provided, this is ignored. If any of the requested entities do not exist or are not visible, they are not included in the response.

owner_id
integer
If supplied, only persons owned by the specified user are returned. If filter_id is provided, this is ignored.

org_id
integer
If supplied, only persons linked to the specified organization are returned. If filter_id is provided, this is ignored.

updated_since
string
If set, only persons with an update_time later than or equal to this time are returned. In RFC3339 format, e.g. 2025-01-01T10:20:00Z.

updated_until
string
If set, only persons with an update_time earlier than this time are returned. In RFC3339 format, e.g. 2025-01-01T10:20:00Z.

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
Optional comma separated string array of additional fields to include. marketing_status and doi_status can only be included if the company has marketing app enabled.

Values

next_activity_id

last_activity_id

open_deals_count

related_open_deals_count

closed_deals_count

related_closed_deals_count

participant_open_deals_count

participant_closed_deals_count

email_messages_count

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

last_incoming_mail_time

last_outgoing_mail_time

marketing_status

doi_status

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
"name":"Person Name"
"first_name":"Person"
"last_name":"Name"
"owner_id":1
"org_id":1
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"value":"email1@email.com"
"primary":true
"label":"work"
"value":"email2@email.com"
"primary":false
"label":"home"
"value":"12345"
"primary":true
"label":"work"
"value":"54321"
"primary":false
"label":"home"
"is_deleted":false
"visible_to":7
1
2
3
"picture_id":1
"custom_fields":
"notes":"Notes from contact sync"
"value":"skypeusername"
"primary":true
"label":"skype"
"value":"whatsappusername"
"primary":false
"label":"whatsapp"
"birthday":"2000-12-31"
"job_title":"Manager"
"value":"123 Main St"
"country":"USA"
"admin_area_level_1":"CA"
"admin_area_level_2":"Santa Clara"
"locality":"Sunnyvale"
"sublocality":"Downtown"
"route":"Main St"
"street_number":"123"
"postal_code":"94085"
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
Get all persons collection
Copy link
Returns all persons. Please note that only global admins (those with global permissions) can access this endpoint. Users with regular permissions will receive a 403 response. Read more about global permissions here.
This endpoint has been deprecated. Please use GET /api/v2/persons instead.

Deprecated endpoint

Cost
10

Request
GET/v1/persons/collection
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
If supplied, only persons owned by the given user will be returned

first_char
string
If supplied, only persons whose name starts with the specified letter will be returned (case-insensitive)

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"active_flag":true
"owner_id":123
"org_id":1234
"name":"Will Smith"
"value":"12345"
"primary":true
"label":"work"
"value":"56789"
"primary":false
"label":"home"
"value":"12345@email.com"
"primary":true
"label":"work"
"update_time":"2023-02-08 05:30:20"
"delete_time":null
"add_time":"2023-01-08 05:30:20"
"visible_to":"3"
"picture_id":12
"label":1
"cc_email":"org@pipedrivemail.com"
"next_cursor":"eyJhY3Rpdml0aWVzIjoyN30"
Search persons
Copy link
Searches all persons by name, email, phone, notes and/or custom fields. This endpoint is a wrapper of /v1/itemSearch with a narrower OAuth scope. Found persons can be filtered by organization ID.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
20

Request
GET/api/v2/persons/search
Query parameters
term
string
required
The search term to look for. Minimum 2 characters (or 1 if using exact_match). Please note that the search term has to be URL encoded.

fields
string
A comma-separated string array. The fields to perform the search from. Defaults to all of them. Only the following custom field types are searchable: address, varchar, text, varchar_auto, double, monetary and phone. Read more about searching by custom fields here.

Values

custom_fields

email

notes

phone

name

exact_match
boolean
When enabled, only full exact matches against the given term are returned. It is not case sensitive.

organization_id
integer
Will filter persons by the provided organization ID. The upper limit of found persons associated with the organization is 2000.

include_fields
string
Supports including optional fields in the results which are not provided by default

Values

person.picture

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
"result_score":0.5092
"id":1
"type":"person"
"name":"Jane Doe"
"+372 555555555"
"jane@pipedrive.com"
"visible_to":3
"id":1
"id":1
"name":"Organization name"
"address":null
"custom_fields":
"notes":
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
Get details of a person
Copy link
Returns the details of a specific person. Fields ims, postal_address, notes, birthday, and job_title are only included if contact sync is enabled for the company.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
1

Request
GET/api/v2/persons/{id}
Path parameters
id
integer
required
The ID of the person

Query parameters
include_fields
string
Optional comma separated string array of additional fields to include. marketing_status and doi_status can only be included if the company has marketing app enabled.

Values

next_activity_id

last_activity_id

open_deals_count

related_open_deals_count

closed_deals_count

related_closed_deals_count

participant_open_deals_count

participant_closed_deals_count

email_messages_count

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

last_incoming_mail_time

last_outgoing_mail_time

marketing_status

doi_status

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
"name":"Person Name"
"first_name":"Person"
"last_name":"Name"
"owner_id":1
"org_id":1
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"value":"email1@email.com"
"primary":true
"label":"work"
"value":"email2@email.com"
"primary":false
"label":"home"
"value":"12345"
"primary":true
"label":"work"
"value":"54321"
"primary":false
"label":"home"
"is_deleted":false
"visible_to":7
1
2
3
"picture_id":1
"custom_fields":
"notes":"Notes from contact sync"
"value":"skypeusername"
"primary":true
"label":"skype"
"value":"whatsappusername"
"primary":false
"label":"whatsapp"
"birthday":"2000-12-31"
"job_title":"Manager"
"value":"123 Main St"
"country":"USA"
"admin_area_level_1":"CA"
"admin_area_level_2":"Santa Clara"
"locality":"Sunnyvale"
"sublocality":"Downtown"
"route":"Main St"
"street_number":"123"
"postal_code":"94085"
List activities associated with a person
Copy link
Lists activities associated with a person.
This endpoint has been deprecated. Please use GET /api/v2/activities?person_id={id} instead.

Deprecated endpoint

Cost
20

Request
GET/v1/persons/{id}/activities
Path parameters
id
integer
required
The ID of the person

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
Whether the activity is done or not. 0 = Not done, 1 = Done. If omitted, returns both Done and Not done activities.

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
List updates about person field values
Copy link
Lists updates about field values of a person.

API v1
Cost
20

Request
GET/v1/persons/{id}/changelog
Path parameters
id
integer
required
The ID of the person

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
"field_key":"51c27e4a19c3bedd91162a9d446707c1f95174ea"
"old_value":null
"new_value":"200"
"actor_user_id":26
"time":"2024-02-12 09:14:35"
"change_source":"app"
"change_source_user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
"is_bulk_update_flag":false
"field_key":"email"
"old_value":"john.doe@pipedrive.com"
"new_value":"jane.doe@pipedrive.com"
"actor_user_id":26
"time":"2024-02-12 09:10:12"
"change_source":"app"
"change_source_user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
"is_bulk_update_flag":false
"next_cursor":"aWQ6NTQ0"
List deals associated with a person
Copy link
Lists deals associated with a person.
This endpoint has been deprecated. Please use GET /api/v2/deals?person_id={id} instead.

Deprecated endpoint

Cost
20

Request
GET/v1/persons/{id}/deals
Path parameters
id
integer
required
The ID of the person

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
List files attached to a person
Copy link
Lists files associated with a person.

API v1
Cost
20

Request
GET/v1/persons/{id}/files
Path parameters
id
integer
required
The ID of the person

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
List updates about a person
Copy link
Lists updates about a person.
If a company uses the Campaigns product, then this endpoint's response will also include updates for the marketing_status field.

API v1
Cost
40

Request
GET/v1/persons/{id}/flow
Path parameters
id
integer
required
The ID of the person

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
Whether to show custom field updates or not. 1 = Include custom field changes. If omitted returns changes without custom field updates.

items
string
A comma-separated string for filtering out item specific updates. (Possible values - call, activity, plannedActivity, change, note, deal, file, dealChange, personChange, organizationChange, follower, dealFollower, personFollower, organizationFollower, participant, comment, mailMessage, mailMessageWithAttachment, invoice, document, marketing_campaign_stat, marketing_status_change).

Response
200
OK


Expand all

Copy code
"success":true
List followers of a person
Copy link
Lists users who are following the person.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
10

Request
GET/api/v2/persons/{id}/followers
Path parameters
id
integer
required
The ID of the person

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
List mail messages associated with a person
Copy link
Lists mail messages associated with a person.

API v1
Cost
20

Request
GET/v1/persons/{id}/mailMessages
Path parameters
id
integer
required
The ID of the person

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
List users permitted to access a person.

API v1
Cost
10

Request
GET/v1/persons/{id}/permittedUsers
Path parameters
id
integer
required
The ID of the person

Response
200
OK


Collapse all

Copy code
"success":true
123
777
List products associated with a person
Copy link
Lists products associated with a person.

API v1
Cost
20

Request
GET/v1/persons/{id}/products
Path parameters
id
integer
required
The ID of the person

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
"id":123
"company_id":1938610
"creator_user_id":599218
"user_id":599218
"person_id":25
"org_id":1
"stage_id":2
"title":"tervist"
"value":3342.79
"currency":"EUR"
"add_time":"2017-10-18 13:23:07"
"first_add_time":"2017-10-18 13:23:07"
"update_time":"2020-09-18 12:12:54"
"stage_change_time":"2020-05-07 11:44:00"
"active":true
"deleted":false
"status":"open"
"probability":null
"next_activity_date":"2020-01-17"
"next_activity_time":null
"next_activity_id":7
"last_activity_id":null
"last_activity_date":null
"lost_reason":null
"visible_to":"3"
"close_time":null
"pipeline_id":1
"won_time":null
"first_won_time":null
"lost_time":null
"products_count":6
"files_count":1
"notes_count":0
"email_messages_count":0
"activities_count":1
"done_activities_count":0
"undone_activities_count":1
"participants_count":2
"expected_close_date":null
"last_incoming_mail_time":"2020-09-18 12:12:54"
"last_outgoing_mail_time":"2020-09-18 12:12:54"
"label":null
"id":4
"company_id":1938610
"name":"1234"
"code":"444"
"description":"123"
"unit":""
"tax":0
"category":"40"
"active_flag":true
"selectable":true
"first_char":"1"
"visible_to":"3"
"owner_id":967055
"files_count":null
"add_time":"2020-01-28 11:54:41"
"update_time":"2020-09-18 11:54:36"
"deal_id":5
"start":0
"limit":100
"more_items_in_collection":true
List followers changelog of a person
Copy link
Lists changelogs about users have followed the person.

API v2
Cost
10

Request
GET/api/v2/persons/{id}/followers/changelog
Path parameters
id
integer
required
The ID of the person

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
Add a person
Copy link
Adds a new person. If the company uses the Campaigns product, then this endpoint will also accept and return the marketing_status field.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
5

Request
POST/api/v2/persons
Body parameters
application/json

name
string
The name of the person

owner_id
integer
The ID of the user who owns the person

org_id
integer
The ID of the organization linked to the person

add_time
string
The creation date and time of the person

update_time
string
The last updated date and time of the person

emails
array
The emails of the person

phones
array
The phones of the person

visible_to
integer
The visibility of the person

label_ids
array
The IDs of labels assigned to the person

marketing_status
string
If the person does not have a valid email address, then the marketing status is not set and no_consent is returned for the marketing_status value when the new person is created. If the change is forbidden, the status will remain unchanged for every call that tries to modify the marketing status. Please be aware that it is only allowed once to change the marketing status from an old status to a new one.

Value	Description
no_consent	The customer has not given consent to receive any marketing communications
unsubscribed	The customers have unsubscribed from ALL marketing communications
subscribed	The customers are subscribed and are counted towards marketing caps
archived	The customers with subscribed status can be moved to archived to save consent, but they are not paid for
Values

no_consent

unsubscribed

subscribed

archived

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"name":"Person Name"
"first_name":"Person"
"last_name":"Name"
"owner_id":1
"org_id":1
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"value":"email1@email.com"
"primary":true
"label":"work"
"value":"email2@email.com"
"primary":false
"label":"home"
"value":"12345"
"primary":true
"label":"work"
"value":"54321"
"primary":false
"label":"home"
"is_deleted":false
"visible_to":7
1
2
3
"picture_id":1
"custom_fields":
"notes":"Notes from contact sync"
"value":"skypeusername"
"primary":true
"label":"skype"
"value":"whatsappusername"
"primary":false
"label":"whatsapp"
"birthday":"2000-12-31"
"job_title":"Manager"
"value":"123 Main St"
"country":"USA"
"admin_area_level_1":"CA"
"admin_area_level_2":"Santa Clara"
"locality":"Sunnyvale"
"sublocality":"Downtown"
"route":"Main St"
"street_number":"123"
"postal_code":"94085"
Add a follower to a person
Copy link
Adds a user as a follower to the person.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
5

Request
POST/api/v2/persons/{id}/followers
Path parameters
id
integer
required
The ID of the person

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
Add person picture
Copy link
Adds a picture to a person. If a picture is already set, the old picture will be replaced. Added image (or the cropping parameters supplied with the request) should have an equal width and height and should be at least 128 pixels. GIF, JPG and PNG are accepted. All added images will be resized to 128 and 512 pixel wide squares.

API v1
Cost
10

Request
POST/v1/persons/{id}/picture
Path parameters
id
integer
required
The ID of the person

Body parameters
multipart/form-data

file
string
required
One image supplied in the multipart/form-data encoding

Formatbinary
crop_x
integer
X coordinate to where start cropping form (in pixels)

crop_y
integer
Y coordinate to where start cropping form (in pixels)

crop_width
integer
The width of the cropping area (in pixels)

crop_height
integer
The height of the cropping area (in pixels)

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"item_type":"person"
"item_id":25
"active_flag":true
"add_time":"2020-09-08 08:17:52"
"update_time":"0000-00-00 00:00:00"
"added_by_user_id":967055
"128":"https://pipedrive-profile-pics.s3.example.com/f8893852574273f2747bf6ef09d11cfb4ac8f269_128.jpg"
"512":"https://pipedrive-profile-pics.s3.example.com/f8893852574273f2747bf6ef09d11cfb4ac8f269_512.jpg"
Update a person
Copy link
Updates the properties of a person.
If the company uses the Campaigns product, then this endpoint will also accept and return the marketing_status field.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
5

Request
PATCH/api/v2/persons/{id}
Path parameters
id
integer
required
The ID of the person

Body parameters
application/json

name
string
The name of the person

owner_id
integer
The ID of the user who owns the person

org_id
integer
The ID of the organization linked to the person

add_time
string
The creation date and time of the person

update_time
string
The last updated date and time of the person

emails
array
The emails of the person

phones
array
The phones of the person

visible_to
integer
The visibility of the person

label_ids
array
The IDs of labels assigned to the person

marketing_status
string
If the person does not have a valid email address, then the marketing status is not set and no_consent is returned for the marketing_status value when the new person is created. If the change is forbidden, the status will remain unchanged for every call that tries to modify the marketing status. Please be aware that it is only allowed once to change the marketing status from an old status to a new one.

Value	Description
no_consent	The customer has not given consent to receive any marketing communications
unsubscribed	The customers have unsubscribed from ALL marketing communications
subscribed	The customers are subscribed and are counted towards marketing caps
archived	The customers with subscribed status can be moved to archived to save consent, but they are not paid for
Values

no_consent

unsubscribed

subscribed

archived

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"name":"Person Name"
"first_name":"Person"
"last_name":"Name"
"owner_id":1
"org_id":1
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"value":"email1@email.com"
"primary":true
"label":"work"
"value":"email2@email.com"
"primary":false
"label":"home"
"value":"12345"
"primary":true
"label":"work"
"value":"54321"
"primary":false
"label":"home"
"is_deleted":false
"visible_to":7
1
2
3
"picture_id":1
"custom_fields":
"notes":"Notes from contact sync"
"value":"skypeusername"
"primary":true
"label":"skype"
"value":"whatsappusername"
"primary":false
"label":"whatsapp"
"birthday":"2000-12-31"
"job_title":"Manager"
"value":"123 Main St"
"country":"USA"
"admin_area_level_1":"CA"
"admin_area_level_2":"Santa Clara"
"locality":"Sunnyvale"
"sublocality":"Downtown"
"route":"Main St"
"street_number":"123"
"postal_code":"94085"
Merge two persons
Copy link
Merges a person with another person. For more information, see the tutorial for merging two persons.

API v1
Cost
40

Request
PUT/v1/persons/{id}/merge
Path parameters
id
integer
required
The ID of the person

Body parameters
application/json

merge_with_id
integer
required
The ID of the person that will not be overwritten. This person’s data will be prioritized in case of conflict with the other person.

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"company_id":12
"owner_id":123
"org_id":123
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
"value":"some@email.com"
"primary":true
"label":"work"
"first_char":"w"
"update_time":"2020-05-08 05:30:20"
"add_time":"2017-10-18 13:23:07"
"visible_to":"3"
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
"merge_what_id":456
Delete multiple persons in bulk
Copy link
Marks multiple persons as deleted. After 30 days, the persons will be permanently deleted.
This endpoint has been deprecated. Please use DELETE /api/v2/persons/{id} instead.

Deprecated endpoint

Cost
10

Request
DELETE/v1/persons
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
456
Delete a person
Copy link
Marks a person as deleted. After 30 days, the person will be permanently deleted.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
3

Request
DELETE/api/v2/persons/{id}
Path parameters
id
integer
required
The ID of the person

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
Delete a follower from a person
Copy link
Deletes a user follower from the person.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
3

Request
DELETE/api/v2/persons/{id}/followers/{follower_id}
Path parameters
id
integer
required
The ID of the person

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
Delete person picture
Copy link
Deletes a person’s picture.

API v1
Cost
6

Request
DELETE/v1/persons/{id}/picture
Path parameters
id
integer
required
The ID of the person

Response
200
OK


Collapse all

Copy code
"success":true
"id":12


PersonFields

Run in Postman
Person fields represent the near-complete schema for a person in the context of the company of the authorized user. Each company can have a different schema for their persons, with various custom fields. In the context of using person fields as a schema for defining the data fields of a person, it must be kept in mind that some types of custom fields can have additional data fields which are not separate person fields per se. Such is the case with monetary, daterange and timerange fields – each of these fields will have one additional data field in addition to the one presented in the context of person fields. For example, if there is a monetary field with the key ffk9s9 stored on the account, ffk9s9 would hold the numeric value of the field, and ffk9s9_currency would hold the ISO currency code that goes along with the numeric value. To find out which data fields are available, fetch one person and list its keys.

Get all person fields
Copy link
Returns data about all person fields.
If a company uses the Campaigns product, then this endpoint will also return the data.marketing_status field.

API v1
Cost
20

Request
GET/v1/personFields
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
Get one person field
Copy link
Returns data about a specific person field.

API v1
Cost
2

Request
GET/v1/personFields/{id}
Path parameters
id
integer
required
The ID of the field

Response
200
OK


Collapse all

Copy code
"success":true
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
Add a new person field
Copy link
Adds a new person field. For more information, see the tutorial for adding a new custom field.

API v1
Cost
10

Request
POST/v1/personFields
Body parameters
application/json

name
string
required
The name of the field

options
array
When field_type is either set or enum, possible options must be supplied as a JSON-encoded sequential array of objects. Example: [{"label":"New Item"}]

add_visible_flag
boolean
Whether the field is available in the 'add new' modal or not (both in the web and mobile app)

Defaulttrue
field_type
string
required
The type of the field

Value	Description
address	Address field
date	Date (format YYYY-MM-DD)
daterange	Date-range field (has a start date and end date value, both YYYY-MM-DD)
double	Numeric value
enum	Options field with a single possible chosen option
monetary	Monetary field (has a numeric value and a currency value)
org	Organization field (contains an organization ID which is stored on the same account)
people	Person field (contains a person ID which is stored on the same account)
phone	Phone field (up to 255 numbers and/or characters)
set	Options field with a possibility of having multiple chosen options
text	Long text (up to 65k characters)
time	Time field (format HH:MM:SS)
timerange	Time-range field (has a start time and end time value, both HH:MM:SS)
user	User field (contains a user ID of another Pipedrive user)
varchar	Text (up to 255 characters)
varchar_auto	Autocomplete text (up to 255 characters)
visible_to	System field that keeps item's visibility setting
Values

address

date

daterange

double

enum

monetary

org

people

phone

set

text

time

timerange

user

varchar

varchar_auto

visible_to

Response
200
OK


Collapse all

Copy code
"success":true
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
Update a person field
Copy link
Updates a person field. For more information, see the tutorial for updating custom fields' values.

API v1
Cost
10

Request
PUT/v1/personFields/{id}
Path parameters
id
integer
required
The ID of the field

Body parameters
application/json

name
string
The name of the field

options
array
When field_type is either set or enum, possible options must be supplied as a JSON-encoded sequential array of objects. All active items must be supplied and already existing items must have their ID supplied. New items only require a label. Example: [{"id":123,"label":"Existing Item"},{"label":"New Item"}]

add_visible_flag
boolean
Whether the field is available in 'add new' modal or not (both in web and mobile app)

Defaulttrue
Response
200
OK


Collapse all

Copy code
"success":true
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
Delete multiple person fields in bulk
Copy link
Marks multiple fields as deleted.

API v1
Cost
10

Request
DELETE/v1/personFields
Query parameters
ids
string
required
The comma-separated field IDs to delete

Response
200
OK


Collapse all

Copy code
"success":true
123
456
Delete a person field
Copy link
Marks a field as deleted. For more information, see the tutorial for deleting a custom field.

API v1
Cost
6

Request
DELETE/v1/personFields/{id}
Path parameters
id
integer
required
The ID of the field

Response
200
OK


Collapse all

Copy code
"success":true
"id":123