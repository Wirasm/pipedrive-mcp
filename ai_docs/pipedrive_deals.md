Deals

Run in Postman
Deals represent ongoing, lost or won sales to an organization or to a person. Each deal has a monetary value and must be placed in a stage. Deals can be owned by a user, and followed by one or many users. Each deal consists of standard data fields but can also contain a number of custom fields. The custom fields can be recognized by long hashes as keys. These hashes can be mapped against DealField.key. The corresponding label for each such custom field can be obtained from DealField.name.

Get all deals
Copy link
Returns all deals. For more information, see the tutorial for getting all deals.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
10

Request
GET/api/v2/deals
Query parameters
filter_id
integer
If supplied, only deals matching the specified filter are returned

ids
string
Optional comma separated string array of up to 100 entity ids to fetch. If filter_id is provided, this is ignored. If any of the requested entities do not exist or are not visible, they are not included in the response.

owner_id
integer
If supplied, only deals owned by the specified user are returned. If filter_id is provided, this is ignored.

person_id
integer
If supplied, only deals linked to the specified person are returned. If filter_id is provided, this is ignored.

org_id
integer
If supplied, only deals linked to the specified organization are returned. If filter_id is provided, this is ignored.

pipeline_id
integer
If supplied, only deals in the specified pipeline are returned. If filter_id is provided, this is ignored.

stage_id
integer
If supplied, only deals in the specified stage are returned. If filter_id is provided, this is ignored.

status
string
Only fetch deals with a specific status. If omitted, all not deleted deals are returned. If set to deleted, deals that have been deleted up to 30 days ago will be included. Multiple statuses can be included as a comma separated array. If filter_id is provided, this is ignored.

Values

open

won

lost

deleted

updated_since
string
If set, only deals with an update_time later than or equal to this time are returned. In RFC3339 format, e.g. 2025-01-01T10:20:00Z.

updated_until
string
If set, only deals with an update_time earlier than this time are returned. In RFC3339 format, e.g. 2025-01-01T10:20:00Z.

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

first_won_time

products_count

files_count

notes_count

followers_count

email_messages_count

activities_count

done_activities_count

undone_activities_count

participants_count

last_incoming_mail_time

last_outgoing_mail_time

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
"title":"Deal Title"
"creator_user_id":1
"owner_id":1
"value":200
"person_id":1
"org_id":1
"stage_id":1
"pipeline_id":1
"currency":"USD"
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"stage_change_time":"2021-01-01T00:00:00Z"
"status":"open"
"is_deleted":false
"probability":90
"lost_reason":"Lost Reason"
"visible_to":7
"close_time":"2021-01-01T00:00:00Z"
"won_time":"2021-01-01T00:00:00Z"
"lost_time":"2021-01-01T00:00:00Z"
"local_won_date":"2021-01-01"
"local_lost_date":"2021-01-01"
"local_close_date":"2021-01-01"
"expected_close_date":"2021-01-01"
1
2
3
"origin":"ManuallyCreated"
"origin_id":null
"channel":52
"channel_id":"Jun23 Billboards"
"acv":120
"arr":120
"mrr":10
"custom_fields":
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
Get all deals (BETA)
Copy link
Returns all deals. This is a cursor-paginated endpoint that is currently in BETA. For more information, please refer to our documentation on pagination. Please note that only global admins (those with global permissions) can access these endpoints. Users with regular permissions will receive a 403 response. Read more about global permissions here.

API v1
Cost
10

Request
GET/v1/deals/collection
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
If supplied, only deals matching the given user will be returned

stage_id
integer
If supplied, only deals within the given stage will be returned

status
string
Only fetch deals with a specific status. If omitted, all not deleted deals are returned. If set to deleted, deals that have been deleted up to 30 days ago will be included.

Values

open

won

lost

deleted

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"creator_user_id":8877
"person_id":1101
"org_id":5
"stage_id":2
"title":"Deal One"
"value":5000
"currency":"EUR"
"add_time":"2019-05-29 04:21:51"
"update_time":"2019-11-28 16:19:50"
"status":"open"
"probability":null
"lost_reason":null
"visible_to":"1"
"close_time":null
"pipeline_id":1
"won_time":"2019-11-27 11:40:36"
"lost_time":"2019-11-27 11:40:36"
"expected_close_date":"2019-06-29"
"label":"11"
"next_cursor":"eyJhY3Rpdml0aWVzIjoyN30"
Search deals
Copy link
Searches all deals by title, notes and/or custom fields. This endpoint is a wrapper of /v1/itemSearch with a narrower OAuth scope. Found deals can be filtered by the person ID and the organization ID.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
20

Request
GET/api/v2/deals/search
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

notes

title

exact_match
boolean
When enabled, only full exact matches against the given term are returned. It is not case sensitive.

person_id
integer
Will filter deals by the provided person ID. The upper limit of found deals associated with the person is 2000.

organization_id
integer
Will filter deals by the provided organization ID. The upper limit of found deals associated with the organization is 2000.

status
string
Will filter deals by the provided specific status. open = Open, won = Won, lost = Lost. The upper limit of found deals associated with the status is 2000.

Values

open

won

lost

include_fields
string
Supports including optional fields in the results which are not provided by default

Values

deal.cc_email

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
"result_score":1.22
"id":1
"type":"deal"
"title":"Jane Doe deal"
"value":100
"currency":"USD"
"status":"open"
"visible_to":3
"id":1
"id":1
"name":"Lead In"
"id":1
"name":"Jane Doe"
"organization":null
"custom_fields":
"notes":
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
Get deals summary
Copy link
Returns a summary of all the deals.

API v1
Cost
40

Request
GET/v1/deals/summary
Query parameters
status
string
Only fetch deals with a specific status. open = Open, won = Won, lost = Lost.

Values

open

won

lost

filter_id
integer
user_id will not be considered. Only deals matching the given filter will be returned.

user_id
integer
Only deals matching the given user will be returned. user_id will not be considered if you use filter_id.

pipeline_id
integer
Only deals within the given pipeline will be returned

stage_id
integer
Only deals within the given stage will be returned

Response
200
OK


Collapse all

Copy code
"success":true
"value":10
"count":2
"value_converted":11.1
"value_formatted":"€10"
"value_converted_formatted":"US$11.10"
"value":30
"count":3
"value_converted":30
"value_formatted":"US$30"
"value_converted_formatted":"US$3"
"value":10
"count":2
"value_formatted":"€10"
"value":30
"count":3
"value_formatted":"US$30"
"total_count":5
"total_currency_converted_value":41.1
"total_weighted_currency_converted_value":41.1
"total_currency_converted_value_formatted":"US$41.1"
"total_weighted_currency_converted_value_formatted":"US$41.1"
Get deals timeline
Copy link
Returns open and won deals, grouped by a defined interval of time set in a date-type dealField (field_key) — e.g. when month is the chosen interval, and 3 months are asked starting from January 1st, 2012, deals are returned grouped into 3 groups — January, February and March — based on the value of the given field_key.

API v1
Cost
20

Request
GET/v1/deals/timeline
Query parameters
start_date
string
required
The date when the first interval starts. Format: YYYY-MM-DD.

Formatdate
interval
string
required
The type of the interval

Value	Description
day	Day
week	A full week (7 days) starting from start_date
month	A full month (depending on the number of days in given month) starting from start_date
quarter	A full quarter (3 months) starting from start_date
Values

day

week

month

quarter

amount
integer
required
The number of given intervals, starting from start_date, to fetch. E.g. 3 (months).

field_key
string
required
The date field key which deals will be retrieved from

user_id
integer
If supplied, only deals matching the given user will be returned

pipeline_id
integer
If supplied, only deals matching the given pipeline will be returned

filter_id
integer
If supplied, only deals matching the given filter will be returned

exclude_deals
number
Whether to exclude deals list (1) or not (0). Note that when deals are excluded, the timeline summary (counts and values) is still returned.

Values

0

1

totals_convert_currency
string
The 3-letter currency code of any of the supported currencies. When supplied, totals_converted is returned per each interval which contains the currency-converted total amounts in the given currency. You may also set this parameter to default_currency in which case the user's default currency is used.

Response
200
OK


Collapse all

Copy code
"success":true
"period_start":"2019-12-01 00:00:00"
"period_end":"2019-12-31 23:59:59"
"id":1
"creator_user_id":8877
"user_id":8877
"person_id":1101
"org_id":5
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
"lost_time":""
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
"mrr":null
"acv_currency":null
"arr_currency":null
"mrr_currency":null
"count":2
"EUR":100
"USD":220
"EUR":100
"USD":2200
"open_count":1
"EUR":100
"EUR":100
"won_count":1
"USD":2200
Get details of a deal
Copy link
Returns the details of a specific deal. Note that this also returns some additional fields which are not present when asking for all deals – such as deal age and stay in pipeline stages. Also note that custom fields appear as long hashes in the resulting data. These hashes can be mapped against the key value of dealFields. For more information, see the tutorial for getting details of a deal.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
1

Request
GET/api/v2/deals/{id}
Path parameters
id
integer
required
The ID of the deal

Query parameters
include_fields
string
Optional comma separated string array of additional fields to include

Values

next_activity_id

last_activity_id

first_won_time

products_count

files_count

notes_count

followers_count

email_messages_count

activities_count

done_activities_count

undone_activities_count

participants_count

last_incoming_mail_time

last_outgoing_mail_time

custom_fields
string
Optional comma separated string array of custom fields keys to include. If you are only interested in a particular set of custom fields, please use this parameter for faster results and smaller response.
A maximum of 15 keys is allowed.

Response
200
OK


Expand all

Copy code
"success":true
List activities associated with a deal
Copy link
Lists activities associated with a deal.

API v1
Cost
20

Request
GET/v1/deals/{id}/activities
Path parameters
id
integer
required
The ID of the deal

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


Expand all

Copy code
"success":true
List updates about deal field values
Copy link
Lists updates about field values of a deal.

API v1
Cost
20

Request
GET/v1/deals/{id}/changelog
Path parameters
id
integer
required
The ID of the deal

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
"field_key":"title"
"old_value":"My Deel"
"new_value":"My Deal"
"actor_user_id":26
"time":"2024-02-12 09:14:35"
"change_source":"app"
"change_source_user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
"is_bulk_update_flag":false
"field_key":"value"
"old_value":"0"
"new_value":"100"
"actor_user_id":26
"time":"2024-02-12 09:10:12"
"change_source":"app"
"change_source_user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
"is_bulk_update_flag":false
"next_cursor":"aWQ6NTQ0"
List files attached to a deal
Copy link
Lists files associated with a deal.

API v1
Cost
20

Request
GET/v1/deals/{id}/files
Path parameters
id
integer
required
The ID of the deal

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
List updates about a deal
Copy link
Lists updates about a deal.

API v1
Cost
40

Request
GET/v1/deals/{id}/flow
Path parameters
id
integer
required
The ID of the deal

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


Collapse all

Copy code
"success":true
"object":"dealChange"
"timestamp":"2020-09-25 09:21:55"
"id":1300
"item_id":120
"user_id":8877
"field_key":"value"
"old_value":50
"new_value":100
"is_bulk_update_flag":null
"log_time":"2020-09-25 09:21:55"
"change_source":"app"
"change_source_user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML like Gecko) Chrome/84.0.4147.135 Safari/537.36"
"additional_data":
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
"object":"mailMessage"
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
"id":123
"name":"Jane Doe"
"email":"jane@pipedrive.com"
"has_pic":1
"pic_hash":"2611ace8ac6a3afe2f69ed56f9e08c6b"
"active_flag":true
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
"id":1
"name":"Org Name"
"people_count":1
"owner_id":123
"address":"Mustamäe tee 3a, 10615 Tallinn"
"active_flag":true
"cc_email":"org@pipedrivemail.com"
"id":123
"title":"Deal title"
"status":"open"
"value":600
"currency":"EUR"
"stage_id":2
"pipeline_id":1
List updates about participants of a deal
Copy link
List updates about participants of a deal. This is a cursor-paginated endpoint. For more information, please refer to our documentation on pagination.

API v1
Cost
10

Request
GET/v1/deals/{id}/participantsChangelog
Path parameters
id
integer
required
The ID of the deal

Query parameters
limit
integer
Items shown per page

cursor
string
For pagination, the marker (an opaque string value) representing the first item on the next page

Response
200
OK


Collapse all

Copy code
"success":true
"actor_user_id":18
"person_id":10
"action":"added"
"time":"2024-01-10 11:47:23"
"next_cursor":"eyJkZWFsIjo0fQ"
List followers of a deal
Copy link
Lists the followers of a deal.

API v1
Cost
20

Request
GET/v1/deals/{id}/followers
Path parameters
id
integer
required
The ID of the deal

Response
200
OK


Collapse all

Copy code
"success":true
"user_id":123
"id":456
"deal_id":789
"add_time":"2020-09-09 11:36:23"
"start":0
"limit":100
"more_items_in_collection":true
List mail messages associated with a deal
Copy link
Lists mail messages associated with a deal.

API v1
Cost
20

Request
GET/v1/deals/{id}/mailMessages
Path parameters
id
integer
required
The ID of the deal

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
List participants of a deal
Copy link
Lists the participants associated with a deal.
If a company uses the Campaigns product, then this endpoint will also return the data.marketing_status field.

API v1
Cost
10

Request
GET/v1/deals/{id}/participants
Path parameters
id
integer
required
The ID of the deal

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
"id":1092
"active_flag":true
"name":"Peter Pan"
"label":"work"
"value":"john.smith@pipedrive.com"
"primary":true
"label":"work"
"value":"736174198"
"primary":true
"value":1598
"add_time":"2020-07-07 10:29:47"
"active_flag":true
"deal_id":1078
"title":"Neverland deal"
"id":1598
"company_id":4657212
"id":6900896
"name":"Foo Bar"
"email":"foo.bar@pipedrive.com"
"has_pic":0
"pic_hash":null
"active_flag":true
"value":6900896
"name":"Neverland"
"people_count":1
"owner_id":6900896
"address":null
"active_flag":true
"cc_email":null
"value":314
"name":"Peter Pan"
"first_name":"Peter"
"last_name":"Pan"
"open_deals_count":0
"related_open_deals_count":0
"closed_deals_count":0
"related_closed_deals_count":0
"participant_open_deals_count":0
"participant_closed_deals_count":0
"email_messages_count":0
"activities_count":4
"done_activities_count":1
"undone_activities_count":3
"files_count":1
"notes_count":12
"followers_count":1
"won_deals_count":0
"related_won_deals_count":0
"lost_deals_count":0
"related_lost_deals_count":0
"active_flag":true
"label":"work"
"value":"736174198"
"primary":true
"label":"work"
"value":"john.smith@pipedrive.com"
"primary":true
"first_char":"p"
"update_time":"2020-08-31 14:25:11"
"add_time":"2020-07-07 10:29:47"
"visible_to":"3"
"picture_id":null
"sync_needed":false
"next_activity_date":"2020-07-01"
"next_activity_time":null
"next_activity_id":2448
"last_activity_id":2450
"last_activity_date":"2020-07-02"
"last_incoming_mail_time":null
"last_outgoing_mail_time":null
"label":"5, 6"
"org_name":"Neverland"
"owner_name":"Foo Bar"
"cc_email":null
"id":6900896
"name":"Foo Bar"
"email":"foo.bar@pipedrive.com"
"has_pic":0
"pic_hash":null
"active_flag":true
"value":6900896
"related_item_type":"deal"
"related_item_id":1078
"start":0
"limit":100
"more_items_in_collection":false
"id":6900896
"name":"Foo Bar"
"email":"foo.bar@pipedrive.com"
"has_pic":0
"pic_hash":null
"active_flag":true
"active_flag":true
"id":1598
"name":"Peter Pan"
"label":"work"
"value":"john.smith@pipedrive.com"
"primary":true
"label":"work"
"value":"736174198"
"primary":true
"owner_id":8877
"id":314
"name":"Neverland"
"people_count":1
"owner_id":6900896
"address":null
"active_flag":true
"cc_email":null
List permitted users
Copy link
Lists the users permitted to access a deal.

API v1
Cost
10

Request
GET/v1/deals/{id}/permittedUsers
Path parameters
id
integer
required
The ID of the deal

Response
200
OK


Collapse all

Copy code
"success":true
123
456
List all persons associated with a deal
Copy link
Lists all persons associated with a deal, regardless of whether the person is the primary contact of the deal, or added as a participant.
If a company uses the Campaigns product, then this endpoint will also return the data.marketing_status field.

API v1
Cost
20

Request
GET/v1/deals/{id}/persons
Path parameters
id
integer
required
The ID of the deal

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
List products attached to a deal
Copy link
Lists products attached to a deal.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
10

Request
GET/api/v2/deals/{id}/products
Path parameters
id
integer
required
The ID of the deal

Query parameters
cursor
string
For pagination, the marker (an opaque string value) representing the first item on the next page

limit
integer
For pagination, the limit of entries to be returned. If not provided, 100 items will be returned. Please note that a maximum value of 500 is allowed.

sort_by
string
The field to sort by. Supported fields: id, add_time, update_time.

Defaultid
Values

id

add_time

update_time

sort_direction
string
The sorting direction. Supported values: asc, desc.

Defaultasc
Values

asc

desc

Response
200
OK


Collapse all

Copy code
"success":true
"id":3
"sum":90
"tax":0
"deal_id":1
"name":"Mechanical Pencil"
"product_id":1
"product_variation_id":null
"add_time":"2019-12-19T11:36:49Z"
"update_time":"2019-12-19T11:36:49Z"
"comments":""
"currency":"USD"
"discount":0
"quantity":1
"item_price":90
"tax_method":"inclusive"
"discount_type":"percentage"
"is_enabled":true
"billing_frequency":"one-time"
"billing_frequency_cycles":null
"billing_start_date":"2019-12-19"
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
Get deal products of several deals
Copy link
Returns data about products attached to deals

API v2
Cost
10

Request
GET/api/v2/deals/products
Query parameters
deal_ids
array
required
An array of integers with the IDs of the deals for which the attached products will be returned. A maximum of 100 deal IDs can be provided.

cursor
string
For pagination, the marker (an opaque string value) representing the first item on the next page

limit
integer
For pagination, the limit of entries to be returned. If not provided, 100 items will be returned. Please note that a maximum value of 500 is allowed.

sort_by
string
The field to sort by. Supported fields: id, deal_id, add_time, update_time.

Defaultid
Values

id

deal_id

add_time

update_time

sort_direction
string
The sorting direction. Supported values: asc, desc.

Defaultasc
Values

asc

desc

Response
200
OK


Collapse all

Copy code
"success":true
"id":3
"sum":90
"tax":0
"deal_id":1
"name":"Mechanical Pencil"
"product_id":1
"product_variation_id":null
"add_time":"2019-12-19T11:36:49Z"
"update_time":"2019-12-19T11:36:49Z"
"comments":""
"currency":"USD"
"discount":0
"quantity":1
"item_price":90
"tax_method":"inclusive"
"discount_type":"percentage"
"is_enabled":true
"billing_frequency":"one-time"
"billing_frequency_cycles":null
"billing_start_date":"2019-12-19"
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
List discounts added to a deal
Copy link
Lists discounts attached to a deal.

API v2
Cost
10

Request
GET/api/v2/deals/{id}/discounts
Path parameters
id
integer
required
The ID of the deal

Response
200
OK


Collapse all

Copy code
"success":true
"id":"30195b0e-7577-4f52-a5cf-f3ee39b9d1e0"
"description":"10%"
"amount":10
"type":"percentage"
"deal_id":1
"created_at":"2024-03-12T10:30:05Z"
"created_by":1
"updated_at":"2024-03-12T10:30:05Z"
"updated_by":1
List installments added to a list of deals
Copy link
Lists installments attached to a list of deals.

Only available in Advanced and above plans.

API v2
Endpoint is in beta

Cost
10

Request
GET/api/v2/deals/installments
Query parameters
deal_ids
array
required
An array of integers with the IDs of the deals for which the attached installments will be returned. A maximum of 100 deal IDs can be provided.

cursor
string
For pagination, the marker (an opaque string value) representing the first item on the next page

limit
integer
For pagination, the limit of entries to be returned. If not provided, 100 items will be returned. Please note that a maximum value of 500 is allowed.

sort_by
string
The field to sort by. Supported fields: id, billing_date, deal_id.

Defaultid
Values

id

billing_date

deal_id

sort_direction
string
The sorting direction. Supported values: asc, desc.

Defaultasc
Values

asc

desc

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"amount":10
"billing_date":"2025-03-10"
"deal_id":1
"description":"Delivery Fee"
Add a deal
Copy link
Adds a new deal. All deals created through the Pipedrive API will have a origin set to API. Note that you can supply additional custom fields along with the request that are not described here. These custom fields are different for each Pipedrive account and can be recognized by long hashes as keys. To determine which custom fields exists, fetch the dealFields and look for key values. For more information, see the tutorial for adding a deal.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
5

Request
POST/api/v2/deals
Body parameters
application/json

title
string
required
The title of the deal

owner_id
integer
The ID of the user who owns the deal

person_id
integer
The ID of the person linked to the deal

org_id
integer
The ID of the organization linked to the deal

pipeline_id
integer
The ID of the pipeline associated with the deal

stage_id
integer
The ID of the deal stage

value
number
The value of the deal

currency
string
The currency associated with the deal

add_time
string
The creation date and time of the deal

update_time
string
The last updated date and time of the deal

stage_change_time
string
The last updated date and time of the deal stage

is_deleted
boolean
Whether the deal is deleted or not

status
string
The status of the deal

probability
number
The success probability percentage of the deal

lost_reason
string
The reason for losing the deal. Can only be set if deal status is lost.

visible_to
integer
The visibility of the deal

close_time
string
The date and time of closing the deal. Can only be set if deal status is won or lost.

won_time
string
The date and time of changing the deal status as won. Can only be set if deal status is won.

lost_time
string
The date and time of changing the deal status as lost. Can only be set if deal status is lost.

expected_close_date
string
The expected close date of the deal

Formatdate
label_ids
array
The IDs of labels assigned to the deal

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"title":"Deal Title"
"creator_user_id":1
"owner_id":1
"value":200
"person_id":1
"org_id":1
"stage_id":1
"pipeline_id":1
"currency":"USD"
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"stage_change_time":"2021-01-01T00:00:00Z"
"status":"open"
"is_deleted":false
"probability":90
"lost_reason":"Lost Reason"
"visible_to":7
"close_time":"2021-01-01T00:00:00Z"
"won_time":"2021-01-01T00:00:00Z"
"lost_time":"2021-01-01T00:00:00Z"
"local_won_date":"2021-01-01"
"local_lost_date":"2021-01-01"
"local_close_date":"2021-01-01"
"expected_close_date":"2021-01-01"
1
2
3
"origin":"ManuallyCreated"
"origin_id":null
"channel":52
"channel_id":"Jun23 Billboards"
"acv":120
"arr":120
"mrr":10
"custom_fields":
Duplicate deal
Copy link
Duplicates a deal.

API v1
Cost
10

Request
POST/v1/deals/{id}/duplicate
Path parameters
id
integer
required
The ID of the deal

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"creator_user_id":123
"user_id":456
"person_id":1
"org_id":2
"stage_id":2
"title":"Deal One"
"value":5000
"currency":"EUR"
"add_time":"2019-05-29 04:21:51"
"update_time":"2019-05-29 04:21:51"
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
"lost_time":""
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
"origin":"ManuallyCreated"
"origin_id":null
"channel":52
"channel_id":"Jun23 Billboards"
"stage_order_nr":2
"mrr":null
"acv_currency":null
"arr_currency":null
"mrr_currency":null
Add a follower to a deal
Copy link
Adds a follower to a deal.

API v1
Cost
10

Request
POST/v1/deals/{id}/followers
Path parameters
id
integer
required
The ID of the deal

Body parameters
application/json

user_id
integer
required
The ID of the user

Response
200
OK


Collapse all

Copy code
"success":true
"user_id":1
"id":2
"deal_id":3
"add_time":"2018-04-11 12:54:43"
Add a participant to a deal
Copy link
Adds a participant to a deal.

API v1
Cost
10

Request
POST/v1/deals/{id}/participants
Path parameters
id
integer
required
The ID of the deal

Body parameters
application/json

person_id
integer
required
The ID of the person

Response
200
OK


Collapse all

Copy code
"success":true
"id":2146
"active_flag":true
"name":"Bortoloni"
"label":"work"
"value":"namna.nanaaa@pipedrive.com"
"primary":true
"value":""
"primary":true
"value":1131
"add_time":"2020-09-14 05:34:59"
"active_flag":true
"deal_id":1078
"title":"Neverland deal"
"id":1131
"company_id":4657212
"id":9126687
"name":"Moo moo"
"email":"moo.moo@pipedrive.com"
"has_pic":0
"pic_hash":null
"active_flag":true
"value":9126687
"org_id":null
"name":"Bortoloni"
"first_name":"Bortoloni"
"last_name":null
"open_deals_count":0
"related_open_deals_count":0
"closed_deals_count":0
"related_closed_deals_count":0
"participant_open_deals_count":0
"participant_closed_deals_count":0
"email_messages_count":0
"activities_count":0
"done_activities_count":0
"undone_activities_count":0
"files_count":0
"notes_count":0
"followers_count":1
"won_deals_count":0
"related_won_deals_count":0
"lost_deals_count":0
"related_lost_deals_count":0
"active_flag":true
"value":""
"primary":true
"label":"work"
"value":"namna.nanaaa@pipedrive.com"
"primary":true
"first_char":"b"
"update_time":"2020-07-09 07:44:51"
"add_time":"2020-02-03 10:14:03"
"visible_to":"3"
"picture_id":null
"sync_needed":false
"next_activity_date":null
"next_activity_time":null
"next_activity_id":null
"last_activity_id":null
"last_activity_date":null
"last_incoming_mail_time":null
"last_outgoing_mail_time":null
"label":"5, 6"
"org_name":null
"owner_name":"Gabriel"
"cc_email":null
"id":927097
"name":"Heheh Nono"
"email":"heheh.nono@pipedrive.com"
"has_pic":0
"pic_hash":null
"active_flag":true
"value":927097
"related_item_type":"deal"
"related_item_id":1078
"id":927097
"name":"Heheh Nono"
"email":"heheh.nono@pipedrive.com"
"has_pic":0
"pic_hash":null
"active_flag":true
"id":9126687
"name":"Gabriel"
"email":"gogoog.yayay@pipedrive.com"
"has_pic":1
"pic_hash":"4db4fc64638d7d3d9e16e64599ccaff6"
"active_flag":true
"active_flag":true
"id":1131
"name":"Bortoloni"
"label":"work"
"value":"namna.nanaaa@pipedrive.com"
"primary":true
"value":""
"primary":true
"owner_id":8877
Add a product to a deal
Copy link
Adds a product to a deal, creating a new item called a deal-product.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
5

Request
POST/api/v2/deals/{id}/products
Path parameters
id
integer
required
The ID of the deal

Body parameters
application/json

product_id
integer
required
The ID of the product

item_price
number
required
The price value of the product

quantity
number
required
The quantity of the product

tax
number
The product tax

Default0
comments
string
The comments of the product

discount
number
The value of the discount. The discount_type field can be used to specify whether the value is an amount or a percentage

Default0
is_enabled
boolean
Whether this product is enabled for the deal

Not possible to disable the product if the deal has installments associated and the product is the last one enabled

Not possible to enable the product if the deal has installments associated and the product is recurring

Defaulttrue
tax_method
string
The tax option to be applied to the products. When using inclusive, the tax percentage will already be included in the price. When using exclusive, the tax will not be included in the price. When using none, no tax will be added. Use the tax field for defining the tax percentage amount. By default, the user setting value for tax options will be used. Changing this in one product affects the rest of the products attached to the deal

Values

exclusive

inclusive

none

discount_type
string
The value of the discount. The discount_type field can be used to specify whether the value is an amount or a percentage

Defaultpercentage
Values

percentage

amount

product_variation_id
integer
The ID of the product variation

billing_frequency
string
Only available in Advanced and above plans

How often a customer is billed for access to a service or product

To set billing_frequency different than one-time, the deal must not have installments associated

A deal can have up to 20 products attached with billing_frequency different than one-time

Defaultone-time
Values

one-time

annually

semi-annually

quarterly

monthly

weekly

billing_frequency_cycles
integer
Only available in Advanced and above plans

The number of times the billing frequency repeats for a product in a deal

When billing_frequency is set to one-time, this field must be null

When billing_frequency is set to weekly, this field cannot be null

For all the other values of billing_frequency, null represents a product billed indefinitely

Must be a positive integer less or equal to 208

billing_start_date
string
Only available in Advanced and above plans

The billing start date. Must be between 10 years in the past and 10 years in the future

FormatYYYY-MM-DD
Response
201
Created


Collapse all

Copy code
"success":true
"id":3
"sum":90
"tax":0
"deal_id":1
"name":"Mechanical Pencil"
"product_id":1
"product_variation_id":null
"add_time":"2019-12-19T11:36:49Z"
"update_time":"2019-12-19T11:36:49Z"
"comments":""
"currency":"USD"
"discount":0
"quantity":1
"item_price":90
"tax_method":"inclusive"
"discount_type":"percentage"
"is_enabled":true
"billing_frequency":"one-time"
"billing_frequency_cycles":null
"billing_start_date":"2019-12-19"
Add a discount to a deal
Copy link
Adds a discount to a deal changing, the deal value if the deal has one-time products attached.

API v2
Cost
5

Request
POST/api/v2/deals/{id}/discounts
Path parameters
id
integer
required
The ID of the deal

Body parameters
application/json

description
string
required
The name of the discount.

amount
number
required
The discount amount. Must be a positive number (excluding 0).

type
string
required
Determines whether the discount is applied as a percentage or a fixed amount.

Values

percentage

amount

Response
201
Created


Collapse all

Copy code
"success":true
"id":"30195b0e-7577-4f52-a5cf-f3ee39b9d1e0"
"description":"10%"
"amount":10
"type":"percentage"
"deal_id":1
"created_at":"2024-03-12T10:30:05Z"
"created_by":1
"updated_at":"2024-03-12T10:30:05Z"
"updated_by":1
Add an installment to a deal
Copy link
Adds an installment to a deal.

An installment can only be added if the deal includes at least one one-time product. If the deal contains at least one recurring product, adding installments is not allowed.

Only available in Advanced and above plans.

API v2
Endpoint is in beta

Cost
5

Request
POST/api/v2/deals/{id}/installments
Path parameters
id
integer
required
The ID of the deal

Body parameters
application/json

description
string
required
The name of the installment.

amount
number
required
The installment amount. Must be a positive number (excluding 0).

billing_date
string
required
The date which the installment will be charged. Must be in the format YYYY-MM-DD.

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"amount":10
"billing_date":"2025-03-10"
"deal_id":1
"description":"Delivery Fee"
Update a deal
Copy link
Updates the properties of a deal. For more information, see the tutorial for updating a deal.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
5

Request
PATCH/api/v2/deals/{id}
Path parameters
id
integer
required
The ID of the deal

Body parameters
application/json

title
string
The title of the deal

owner_id
integer
The ID of the user who owns the deal

person_id
integer
The ID of the person linked to the deal

org_id
integer
The ID of the organization linked to the deal

pipeline_id
integer
The ID of the pipeline associated with the deal

stage_id
integer
The ID of the deal stage

value
number
The value of the deal

currency
string
The currency associated with the deal

add_time
string
The creation date and time of the deal

update_time
string
The last updated date and time of the deal

stage_change_time
string
The last updated date and time of the deal stage

is_deleted
boolean
Whether the deal is deleted or not

status
string
The status of the deal

probability
number
The success probability percentage of the deal

lost_reason
string
The reason for losing the deal. Can only be set if deal status is lost.

visible_to
integer
The visibility of the deal

close_time
string
The date and time of closing the deal. Can only be set if deal status is won or lost.

won_time
string
The date and time of changing the deal status as won. Can only be set if deal status is won.

lost_time
string
The date and time of changing the deal status as lost. Can only be set if deal status is lost.

expected_close_date
string
The expected close date of the deal

Formatdate
label_ids
array
The IDs of labels assigned to the deal

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"title":"Deal Title"
"creator_user_id":1
"owner_id":1
"value":200
"person_id":1
"org_id":1
"stage_id":1
"pipeline_id":1
"currency":"USD"
"add_time":"2021-01-01T00:00:00Z"
"update_time":"2021-01-01T00:00:00Z"
"stage_change_time":"2021-01-01T00:00:00Z"
"status":"open"
"is_deleted":false
"probability":90
"lost_reason":"Lost Reason"
"visible_to":7
"close_time":"2021-01-01T00:00:00Z"
"won_time":"2021-01-01T00:00:00Z"
"lost_time":"2021-01-01T00:00:00Z"
"local_won_date":"2021-01-01"
"local_lost_date":"2021-01-01"
"local_close_date":"2021-01-01"
"expected_close_date":"2021-01-01"
1
2
3
"origin":"ManuallyCreated"
"origin_id":null
"channel":52
"channel_id":"Jun23 Billboards"
"acv":120
"arr":120
"mrr":10
"custom_fields":
Merge two deals
Copy link
Merges a deal with another deal. For more information, see the tutorial for merging two deals.

API v1
Cost
40

Request
PUT/v1/deals/{id}/merge
Path parameters
id
integer
required
The ID of the deal

Body parameters
application/json

merge_with_id
integer
required
The ID of the deal that the deal will be merged with

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"creator_user_id":123
"user_id":456
"person_id":1
"org_id":2
"stage_id":2
"title":"Deal One"
"value":5000
"currency":"EUR"
"add_time":"2019-05-29 04:21:51"
"update_time":"2019-06-29 05:20:31"
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
"lost_time":""
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
"origin":"ManuallyCreated"
"origin_id":null
"channel":52
"channel_id":"Jun23 Billboards"
"stage_order_nr":2
"mrr":null
"acv_currency":null
"arr_currency":null
"mrr_currency":null
Update the product attached to a deal
Copy link
Updates the details of the product that has been attached to a deal.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
5

Request
PATCH/api/v2/deals/{id}/products/{product_attachment_id}
Path parameters
id
integer
required
The ID of the deal

product_attachment_id
integer
required
The ID of the deal-product (the ID of the product attached to the deal)

Body parameters
application/json

product_id
integer
The ID of the product

item_price
number
The price value of the product

quantity
number
The quantity of the product

tax
number
The product tax

Default0
comments
string
The comments of the product

discount
number
The value of the discount. The discount_type field can be used to specify whether the value is an amount or a percentage

Default0
is_enabled
boolean
Whether this product is enabled for the deal

Not possible to disable the product if the deal has installments associated and the product is the last one enabled

Not possible to enable the product if the deal has installments associated and the product is recurring

Defaulttrue
tax_method
string
The tax option to be applied to the products. When using inclusive, the tax percentage will already be included in the price. When using exclusive, the tax will not be included in the price. When using none, no tax will be added. Use the tax field for defining the tax percentage amount. By default, the user setting value for tax options will be used. Changing this in one product affects the rest of the products attached to the deal

Values

exclusive

inclusive

none

discount_type
string
The value of the discount. The discount_type field can be used to specify whether the value is an amount or a percentage

Defaultpercentage
Values

percentage

amount

product_variation_id
integer
The ID of the product variation

billing_frequency
string
Only available in Advanced and above plans

How often a customer is billed for access to a service or product

To set billing_frequency different than one-time, the deal must not have installments associated

A deal can have up to 20 products attached with billing_frequency different than one-time

Values

one-time

annually

semi-annually

quarterly

monthly

weekly

billing_frequency_cycles
integer
Only available in Advanced and above plans

The number of times the billing frequency repeats for a product in a deal

When billing_frequency is set to one-time, this field must be null

When billing_frequency is set to weekly, this field cannot be null

For all the other values of billing_frequency, null represents a product billed indefinitely

Must be a positive integer less or equal to 208

billing_start_date
string
Only available in Advanced and above plans

The billing start date. Must be between 10 years in the past and 10 years in the future

FormatYYYY-MM-DD
Response
200
OK


Collapse all

Copy code
"success":true
"id":3
"sum":90
"tax":0
"deal_id":1
"name":"Mechanical Pencil"
"product_id":1
"product_variation_id":null
"add_time":"2019-12-19T11:36:49Z"
"update_time":"2019-12-19T11:36:49Z"
"comments":""
"currency":"USD"
"discount":0
"quantity":1
"item_price":90
"tax_method":"inclusive"
"discount_type":"percentage"
"is_enabled":true
"billing_frequency":"one-time"
"billing_frequency_cycles":null
"billing_start_date":"2019-12-19"
Update a discount added to a deal
Copy link
Edits a discount added to a deal, changing the deal value if the deal has one-time products attached.

API v2
Cost
5

Request
PATCH/api/v2/deals/{id}/discounts/{discount_id}
Path parameters
id
integer
required
The ID of the deal

discount_id
integer
required
The ID of the discount

Body parameters
application/json

description
string
The name of the discount.

amount
number
The discount amount. Must be a positive number (excluding 0).

type
string
Determines whether the discount is applied as a percentage or a fixed amount.

Values

percentage

amount

Response
200
OK


Collapse all

Copy code
"success":true
"id":"30195b0e-7577-4f52-a5cf-f3ee39b9d1e0"
"description":"10%"
"amount":10
"type":"percentage"
"deal_id":1
"created_at":"2024-03-12T10:30:05Z"
"created_by":1
"updated_at":"2024-03-12T10:30:05Z"
"updated_by":1
Update an installment added to a deal
Copy link
Edits an installment added to a deal.

Only available in Advanced and above plans.

API v2
Endpoint is in beta

Cost
5

Request
PATCH/api/v2/deals/{id}/installments/{installment_id}
Path parameters
id
integer
required
The ID of the deal

installment_id
integer
required
The ID of the installment

Body parameters
application/json

description
string
The name of the installment.

amount
number
The installment amount. Must be a positive number (excluding 0).

billing_date
string
The date which the installment will be charged. Must be in the format YYYY-MM-DD.

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
"amount":10
"billing_date":"2025-03-10"
"deal_id":1
"description":"Delivery Fee"
Delete multiple deals in bulk
Copy link
Marks multiple deals as deleted. After 30 days, the deals will be permanently deleted.

API v1
Cost
10

Request
DELETE/v1/deals
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
Delete a deal
Copy link
Marks a deal as deleted. After 30 days, the deal will be permanently deleted.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
3

Request
DELETE/api/v2/deals/{id}
Path parameters
id
integer
required
The ID of the deal

Response
200
OK


Collapse all

Copy code
"success":true
"id":1
Delete a follower from a deal
Copy link
Deletes a follower from a deal.

API v1
Cost
6

Request
DELETE/v1/deals/{id}/followers/{follower_id}
Path parameters
id
integer
required
The ID of the deal

follower_id
integer
required
The ID of the follower

Response
200
OK


Collapse all

Copy code
"success":true
"id":123
Delete a participant from a deal
Copy link
Deletes a participant from a deal.

API v1
Cost
6

Request
DELETE/v1/deals/{id}/participants/{deal_participant_id}
Path parameters
id
integer
required
The ID of the deal

deal_participant_id
integer
required
The ID of the participant of the deal

Response
200
OK


Collapse all

Copy code
"success":true
"id":123
Delete an attached product from a deal
Copy link
Deletes a product attachment from a deal, using the product_attachment_id

Not possible to delete the attached product if the deal has installments associated and the product is the last one enabled

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
3

Request
DELETE/api/v2/deals/{id}/products/{product_attachment_id}
Path parameters
id
integer
required
The ID of the deal

product_attachment_id
integer
required
The product attachment ID

Response
200
OK


Collapse all

Copy code
"success":true
"id":123
Delete a discount from a deal
Copy link
Removes a discount from a deal, changing the deal value if the deal has one-time products attached.

API v2
Cost
3

Request
DELETE/api/v2/deals/{id}/discounts/{discount_id}
Path parameters
id
integer
required
The ID of the deal

discount_id
integer
required
The ID of the discount

Response
200
OK


Collapse all

Copy code
"success":true
"id":123
Delete an installment from a deal
Copy link
Removes an installment from a deal.

Only available in Advanced and above plans.

API v2
Endpoint is in beta

Cost
3

Request
DELETE/api/v2/deals/{id}/installments/{installment_id}
Path parameters
id
integer
required
The ID of the deal

installment_id
integer
required
The ID of the installment

Response
200
OK


Expand all

Copy code
"success":true


DealFields

Run in Postman
Deal fields represent the near-complete schema for a deal in the context of the company of the authorized user. Each company can have a different schema for their deals, with various custom fields. In the context of using deal fields as a schema for defining the data fields of a deal, it must be kept in mind that some types of custom fields can have additional data fields which are not separate deal fields per se. Such is the case with monetary, daterange and timerange fields – each of these fields will have one additional data field in addition to the one presented in the context of deal fields. For example, if there is a monetary field with the key ffk9s9 stored on the account, ffk9s9 would hold the numeric value of the field, and ffk9s9_currency would hold the ISO currency code that goes along with the numeric value. To find out which data fields are available, fetch one deal and list its keys.

Get all deal fields
Copy link
Returns data about all deal fields.

API v1
Cost
20

Request
GET/v1/dealFields
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
Get one deal field
Copy link
Returns data about a specific deal field.

API v1
Cost
2

Request
GET/v1/dealFields/{id}
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
Add a new deal field
Copy link
Adds a new deal field. For more information, see the tutorial for adding a new custom field.

API v1
Cost
10

Request
POST/v1/dealFields
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
Update a deal field
Copy link
Updates a deal field. For more information, see the tutorial for updating custom fields' values.

API v1
Cost
10

Request
PUT/v1/dealFields/{id}
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
Delete multiple deal fields in bulk
Copy link
Marks multiple deal fields as deleted.

API v1
Cost
10

Request
DELETE/v1/dealFields
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
Delete a deal field
Copy link
Marks a field as deleted. For more information, see the tutorial for deleting a custom field.

API v1
Cost
6

Request
DELETE/v1/dealFields/{id}
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