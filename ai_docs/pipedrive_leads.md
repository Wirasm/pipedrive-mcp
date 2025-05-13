Leads

Leads are potential deals stored in Leads Inbox before they are archived or converted to a deal. Each lead needs to be named (using the title field) and be linked to a person or an organization. In addition to that, a lead can contain most of the fields a deal can (such as value or expected_close_date).

Get all leads

Returns multiple leads. Leads are sorted by the time they were created, from oldest to newest. Pagination can be controlled using limit and start query parameters. If a lead contains custom fields, the fields' values will be included in the response in the same format as with the Deals endpoints. If a custom field's value hasn't been set for the lead, it won't appear in the response. Please note that leads do not have a separate set of custom fields, instead they inherit the custom fields' structure from deals.

API v1
Cost
20

Request
GET/v1/leads
Query parameters
limit
integer
For pagination, the limit of entries to be returned. If not provided, 100 items will be returned.

start
integer
For pagination, the position that represents the first result for the page

archived_status
string
Filtering based on the archived status of a lead. If not provided, All is used.

Values

archived

not_archived

all

owner_id
integer
If supplied, only leads matching the given user will be returned. However, filter_id takes precedence over owner_id when supplied.

person_id
integer
If supplied, only leads matching the given person will be returned. However, filter_id takes precedence over person_id when supplied.

organization_id
integer
If supplied, only leads matching the given organization will be returned. However, filter_id takes precedence over organization_id when supplied.

filter_id
integer
The ID of the filter to use

sort
string
The field names and sorting mode separated by a comma (field_name_1 ASC, field_name_2 DESC). Only first-level field keys are supported (no nested keys).

Values

id

title

owner_id

creator_id

was_seen

expected_close_date

next_activity_id

add_time

update_time

Response
200
OK


Collapse all

Copy code
"success":true
"id":"adf21080-0e10-11eb-879b-05d71fb426ec"
"title":"Jane Doe Lead"
"owner_id":1
"creator_id":1
"f08b42a0-4e75-11ea-9643-03698ef1cfd6"
"f08b42a1-4e75-11ea-9643-03698ef1cfd6"
"person_id":1092
"organization_id":null
"source_name":"API"
"origin":"API"
"origin_id":null
"channel":52
"channel_id":"Jun23 Billboards"
"is_archived":false
"was_seen":false
"amount":999
"currency":"USD"
"expected_close_date":null
"next_activity_id":1
"add_time":"2020-10-14T11:30:36.551Z"
"update_time":"2020-10-14T11:30:36.551Z"
"visible_to":"3"
"cc_email":"company+1+leadntPaYKA5QRxXkh6WMNHiGh@dev.pipedrivemail.com"
Get one lead
Copy link
Returns details of a specific lead. If a lead contains custom fields, the fields' values will be included in the response in the same format as with the Deals endpoints. If a custom field's value hasn't been set for the lead, it won't appear in the response. Please note that leads do not have a separate set of custom fields, instead they inherit the custom fields’ structure from deals.

API v1
Cost
2

Request
GET/v1/leads/{id}
Path parameters
id
string
required
The ID of the lead

Formatuuid
Response
200
OK


Collapse all

Copy code
"success":true
"id":"adf21080-0e10-11eb-879b-05d71fb426ec"
"title":"Jane Doe Lead"
"owner_id":1
"creator_id":1
"f08b42a0-4e75-11ea-9643-03698ef1cfd6"
"f08b42a1-4e75-11ea-9643-03698ef1cfd6"
"person_id":1092
"organization_id":null
"source_name":"API"
"origin":"API"
"origin_id":null
"channel":52
"channel_id":"Jun23 Billboards"
"is_archived":false
"was_seen":false
"amount":999
"currency":"USD"
"expected_close_date":null
"next_activity_id":1
"add_time":"2020-10-14T11:30:36.551Z"
"update_time":"2020-10-14T11:30:36.551Z"
"visible_to":"3"
"cc_email":"company+1+leadntPaYKA5QRxXkh6WMNHiGh@dev.pipedrivemail.com"
List permitted users
Copy link
Lists the users permitted to access a lead.

API v1
Cost
10

Request
GET/v1/leads/{id}/permittedUsers
Path parameters
id
string
required
The ID of the lead

Response
200
OK


Collapse all

Copy code
"success":true
10100010
22302444
33511023
Search leads
Copy link
Searches all leads by title, notes and/or custom fields. This endpoint is a wrapper of /v1/itemSearch with a narrower OAuth scope. Found leads can be filtered by the person ID and the organization ID.

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
20

Request
GET/api/v2/leads/search
Query parameters
term
string
required
The search term to look for. Minimum 2 characters (or 1 if using exact_match). Please note that the search term has to be URL encoded.

fields
string
A comma-separated string array. The fields to perform the search from. Defaults to all of them.

Values

custom_fields

notes

title

exact_match
boolean
When enabled, only full exact matches against the given term are returned. It is not case sensitive.

person_id
integer
Will filter leads by the provided person ID. The upper limit of found leads associated with the person is 2000.

organization_id
integer
Will filter leads by the provided organization ID. The upper limit of found leads associated with the organization is 2000.

include_fields
string
Supports including optional fields in the results which are not provided by default

Values

lead.was_seen

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
"result_score":0.29
"id":"39c433f0-8a4c-11ec-8728-09968f0a1ca0"
"type":"lead"
"title":"John Doe lead"
"id":1
"id":1
"name":"John Doe"
"id":1
"name":"John company"
"phones":
"john@doe.com"
"custom_fields":
"notes":
"value":100
"currency":"USD"
"visible_to":3
"is_archived":false
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
Add a lead
Copy link
Creates a lead. A lead always has to be linked to a person or an organization or both. All leads created through the Pipedrive API will have a lead source and origin set to API. Here's the tutorial for adding a lead. If a lead contains custom fields, the fields' values will be included in the response in the same format as with the Deals endpoints. If a custom field's value hasn't been set for the lead, it won't appear in the response. Please note that leads do not have a separate set of custom fields, instead they inherit the custom fields' structure from deals. See an example given in the updating custom fields' values tutorial.

API v1
Cost
10

Request
POST/v1/leads
Body parameters
application/json

title
string
required
The name of the lead

owner_id
integer
The ID of the user which will be the owner of the created lead. If not provided, the user making the request will be used.

label_ids
array
The IDs of the lead labels which will be associated with the lead

person_id
integer
The ID of a person which this lead will be linked to. If the person does not exist yet, it needs to be created first. This property is required unless organization_id is specified.

organization_id
integer
The ID of an organization which this lead will be linked to. If the organization does not exist yet, it needs to be created first. This property is required unless person_id is specified.

value
object
The potential value of the lead represented by a JSON object: { "amount": 200, "currency": "EUR" }. Both amount and currency are required.

expected_close_date
string
The date of when the deal which will be created from the lead is expected to be closed. In ISO 8601 format: YYYY-MM-DD.

Formatdate
visible_to
string
The visibility of the lead. If omitted, the visibility will be set to the default visibility setting of this item type for the authorized user. Read more about visibility groups here.

Essential / Advanced plan
Value	Description
1	Owner & followers
3	Entire company
Professional / Enterprise plan
Value	Description
1	Owner only
3	Owner's visibility group
5	Owner's visibility group and sub-groups
7	Entire company
Values

1

3

5

7

was_seen
boolean
A flag indicating whether the lead was seen by someone in the Pipedrive UI

origin_id
string
The optional ID to further distinguish the origin of the lead - e.g. Which API integration created this lead. If omitted, origin_id will be set to null.

channel
integer
The ID of Marketing channel this lead was created from. Provided value must be one of the channels configured for your company. You can fetch allowed values with GET /v1/dealFields. If omitted, channel will be set to null.

channel_id
string
The optional ID to further distinguish the Marketing channel. If omitted, channel_id will be set to null.

Response
201
Created


Collapse all

Copy code
"success":true
"id":"adf21080-0e10-11eb-879b-05d71fb426ec"
"title":"Jane Doe Lead"
"owner_id":1
"creator_id":1
"f08b42a0-4e75-11ea-9643-03698ef1cfd6"
"f08b42a1-4e75-11ea-9643-03698ef1cfd6"
"person_id":1092
"organization_id":null
"source_name":"API"
"origin":"API"
"origin_id":null
"channel":52
"channel_id":"Jun23 Billboards"
"is_archived":false
"was_seen":false
"amount":999
"currency":"USD"
"expected_close_date":null
"next_activity_id":1
"add_time":"2020-10-14T11:30:36.551Z"
"update_time":"2020-10-14T11:30:36.551Z"
"visible_to":"3"
"cc_email":"company+1+leadntPaYKA5QRxXkh6WMNHiGh@dev.pipedrivemail.com"
Update a lead
Copy link
Updates one or more properties of a lead. Only properties included in the request will be updated. Send null to unset a property (applicable for example for value, person_id or organization_id). If a lead contains custom fields, the fields' values will be included in the response in the same format as with the Deals endpoints. If a custom field's value hasn't been set for the lead, it won't appear in the response. Please note that leads do not have a separate set of custom fields, instead they inherit the custom fields’ structure from deals. See an example given in the updating custom fields’ values tutorial.

API v1
Cost
10

Request
PATCH/v1/leads/{id}
Path parameters
id
string
required
The ID of the lead

Formatuuid
Body parameters
application/json

title
string
The name of the lead

owner_id
integer
The ID of the user which will be the owner of the created lead. If not provided, the user making the request will be used.

label_ids
array
The IDs of the lead labels which will be associated with the lead

person_id
integer
The ID of a person which this lead will be linked to. If the person does not exist yet, it needs to be created first. A lead always has to be linked to a person or organization or both.

organization_id
integer
The ID of an organization which this lead will be linked to. If the organization does not exist yet, it needs to be created first. A lead always has to be linked to a person or organization or both.

is_archived
boolean
A flag indicating whether the lead is archived or not

value
object
The potential value of the lead represented by a JSON object: { "amount": 200, "currency": "EUR" }. Both amount and currency are required.

expected_close_date
string
The date of when the deal which will be created from the lead is expected to be closed. In ISO 8601 format: YYYY-MM-DD.

Formatdate
visible_to
string
The visibility of the lead. If omitted, the visibility will be set to the default visibility setting of this item type for the authorized user. Read more about visibility groups here.

Essential / Advanced plan
Value	Description
1	Owner & followers
3	Entire company
Professional / Enterprise plan
Value	Description
1	Owner only
3	Owner's visibility group
5	Owner's visibility group and sub-groups
7	Entire company
Values

1

3

5

7

was_seen
boolean
A flag indicating whether the lead was seen by someone in the Pipedrive UI

channel
integer
The ID of Marketing channel this lead was created from. Provided value must be one of the channels configured for your company which you can fetch with GET /v1/dealFields.

channel_id
string
The optional ID to further distinguish the Marketing channel.

Response
200
OK


Collapse all

Copy code
"success":true
"id":"adf21080-0e10-11eb-879b-05d71fb426ec"
"title":"Jane Doe Lead"
"owner_id":1
"creator_id":1
"f08b42a0-4e75-11ea-9643-03698ef1cfd6"
"f08b42a1-4e75-11ea-9643-03698ef1cfd6"
"person_id":1092
"organization_id":null
"source_name":"API"
"origin":"API"
"origin_id":null
"channel":52
"channel_id":"Jun23 Billboards"
"is_archived":false
"was_seen":false
"amount":999
"currency":"USD"
"expected_close_date":null
"next_activity_id":1
"add_time":"2020-10-14T11:30:36.551Z"
"update_time":"2020-10-14T11:30:36.551Z"
"visible_to":"3"
"cc_email":"company+1+leadntPaYKA5QRxXkh6WMNHiGh@dev.pipedrivemail.com"
Delete a lead
Copy link
Deletes a specific lead.

API v1
Cost
6

Request
DELETE/v1/leads/{id}
Path parameters
id
string
required
The ID of the lead

Formatuuid
Response
200
OK


Collapse all

Copy code
"success":true
"id":"adf21080-0e10-11eb-879b-05d71fb426ec"

LeadLabels

Run in Postman
Lead labels allow you to visually categorize your leads. There are three default lead labels: hot, cold, and warm, but you can add as many new custom labels as you want.

Get all lead labels
Copy link
Returns details of all lead labels. This endpoint does not support pagination and all labels are always returned.

API v1
Cost
10

Request
GET/v1/leadLabels
Response
200
OK


Collapse all

Copy code
"success":true
"id":"f08b42a0-4e75-11ea-9643-03698ef1cfd6"
"name":"Hot"
"color":"red"
"add_time":"2020-02-13T15:31:44.000Z"
"update_time":"2020-02-13T15:31:44.000Z"
"id":"f08b42a1-4e75-11ea-9643-03698ef1cfd6"
"name":"Cold"
"color":"blue"
"add_time":"2020-02-13T15:31:44.000Z"
"update_time":"2020-02-13T15:31:44.000Z"
"id":"f08b69b0-4e75-11ea-9643-03698ef1cfd6"
"name":"Warm"
"color":"yellow"
"add_time":"2020-02-13T15:31:44.000Z"
"update_time":"2020-02-13T15:31:44.000Z"
Add a lead label
Copy link
Creates a lead label.

API v1
Cost
10

Request
POST/v1/leadLabels
Body parameters
application/json

name
string
required
The name of the lead label

color
string
required
The color of the label. Only a subset of colors can be used.

Values

blue

brown

dark-gray

gray

green

orange

pink

purple

red

yellow

Response
200
OK


Expand all

Copy code
"success":true
Update a lead label
Copy link
Updates one or more properties of a lead label. Only properties included in the request will be updated.

API v1
Cost
10

Request
PATCH/v1/leadLabels/{id}
Path parameters
id
string
required
The ID of the lead label

Formatuuid
Body parameters
application/json

name
string
The name of the lead label

color
string
The color of the label. Only a subset of colors can be used.

Values

blue

brown

dark-gray

gray

green

orange

pink

purple

red

yellow

Response
200
OK


Collapse all

Copy code
"success":true
"id":"f08b42a0-4e75-11ea-9643-03698ef1cfd6"
"name":"Hot"
"color":"red"
"add_time":"2020-02-13T15:31:44.000Z"
"update_time":"2020-10-14T13:11:36.000Z"
Delete a lead label
Copy link
Deletes a specific lead label.

API v1
Cost
6

Request
DELETE/v1/leadLabels/{id}
Path parameters
id
string
required
The ID of the lead label

Formatuuid
Response
200
OK


Collapse all

Copy code
"success":true
"id":"adf21080-0e10-11eb-879b-05d71fb426ec"

LeadSources

Run in Postman
A lead source indicates where your lead came from. Currently, these are the possible lead sources: Manually created, Deal, Web forms, Prospector, Leadbooster, Live chat, Import, Website visitors, Workflow automation, and API. Lead sources are pre-defined and cannot be edited. Please note that leads sourced from the Chatbot feature are assigned the value Leadbooster. Please also note that this list is not final and new sources may be added as needed.

Get all lead sources
Copy link
Returns all lead sources. Please note that the list of lead sources is fixed, it cannot be modified. All leads created through the Pipedrive API will have a lead source API assigned.

API v1
Cost
2

Request
GET/v1/leadSources
Response
200
OK


Collapse all

Copy code
"success":true
"name":"Manually created"
"name":"Deal"
"name":"Web forms"
"name":"Prospector"
"name":"Leadbooster"
"name":"Live chat"
"name":"Import"
"name":"Website visitors"
"name":"Workflow automation"
"name":"API"


LeadLabels

Run in Postman
Lead labels allow you to visually categorize your leads. There are three default lead labels: hot, cold, and warm, but you can add as many new custom labels as you want.

Get all lead labels
Copy link
Returns details of all lead labels. This endpoint does not support pagination and all labels are always returned.

API v1
Cost
10

Request
GET/v1/leadLabels
Response
200
OK


Collapse all

Copy code
"success":true
"id":"f08b42a0-4e75-11ea-9643-03698ef1cfd6"
"name":"Hot"
"color":"red"
"add_time":"2020-02-13T15:31:44.000Z"
"update_time":"2020-02-13T15:31:44.000Z"
"id":"f08b42a1-4e75-11ea-9643-03698ef1cfd6"
"name":"Cold"
"color":"blue"
"add_time":"2020-02-13T15:31:44.000Z"
"update_time":"2020-02-13T15:31:44.000Z"
"id":"f08b69b0-4e75-11ea-9643-03698ef1cfd6"
"name":"Warm"
"color":"yellow"
"add_time":"2020-02-13T15:31:44.000Z"
"update_time":"2020-02-13T15:31:44.000Z"
Add a lead label
Copy link
Creates a lead label.

API v1
Cost
10

Request
POST/v1/leadLabels
Body parameters
application/json

name
string
required
The name of the lead label

color
string
required
The color of the label. Only a subset of colors can be used.

Values

blue

brown

dark-gray

gray

green

orange

pink

purple

red

yellow

Response
200
OK


Collapse all

Copy code
"success":true
"id":"f08b42a0-4e75-11ea-9643-03698ef1cfd6"
"name":"Hot"
"color":"red"
"add_time":"2020-02-13T15:31:44.000Z"
"update_time":"2020-10-14T13:11:36.000Z"
Update a lead label
Copy link
Updates one or more properties of a lead label. Only properties included in the request will be updated.

API v1
Cost
10

Request
PATCH/v1/leadLabels/{id}
Path parameters
id
string
required
The ID of the lead label

Formatuuid
Body parameters
application/json

name
string
The name of the lead label

color
string
The color of the label. Only a subset of colors can be used.

Values

blue

brown

dark-gray

gray

green

orange

pink

purple

red

yellow

Response
200
OK


Collapse all

Copy code
"success":true
"id":"f08b42a0-4e75-11ea-9643-03698ef1cfd6"
"name":"Hot"
"color":"red"
"add_time":"2020-02-13T15:31:44.000Z"
"update_time":"2020-10-14T13:11:36.000Z"
Delete a lead label
Copy link
Deletes a specific lead label.

API v1
Cost
6

Request
DELETE/v1/leadLabels/{id}
Path parameters
id
string
required
The ID of the lead label

Formatuuid
Response
200
OK


Collapse all

Copy code
"success":true
"id":"adf21080-0e10-11eb-879b-05d71fb426ec"