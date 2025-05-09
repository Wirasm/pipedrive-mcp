Pipedrive API v2 migration guide
Suggest Edits
Migration Guide
This document outlines the differences between Pipedrive API v1 and v2 of endpoints which are available on v2. Where available, please use API v2 for the best performance and developer experience.

General API Changes
All v2 endpoints now have significantly stricter input validation to improve data quality and prevent ambiguity.
Any boolean value fields which returned or accepted 1 or 0 now only return and accept true and false respectively.
Numeric fields no longer coerce string input to number and instead throw a validation error.
Related objects have been removed from API responses to prevent too eager fetching of unnecessary data. Use subsequent API calls to fetch them if you still need them.
All timestamps in the v2 API are now in RFC 3339 format (e.g. 2024-01-01T00:00:00Z or 2024-01-01T00:00:00.000Z) unless specified otherwise to ensure clarity regarding timezones.
Support for field selectors has been removed.
V1 endpoints, which were using HTTP PUT method have been switched to use HTTP PATCH method in v2 for compliance with REST best practices.
Only /api/v2/... prefix is supported. Previously both /api/v1/... and /v1/... could be used.
Custom Fields
Entity custom fields have been moved to a separate custom_fields object with clearer syntax.

Previously custom fields were on the root level of the entity object and had separate keys for their subfields. For example, a currency custom field in API v1 was presented as

JSON

"d4de1c1518b4531717c676029a45911c340390a6": 2300,
"d4de1c1518b4531717c676029a45911c340390a6_currency": "EUR"
The same field is now presented in API v2 as

JSON

"custom_fields": {
  ...,
  "d4de1c1518b4531717c676029a45911c340390a6": {
  "value": 2300,
  "currency": "EUR"
},
...
}
See subsections below for the exact changes for each custom field type.

Text, Large Text and Autocomplete Custom Fields Format Changes
API v1
JSON

"d4de1c1518b4531717c676029a45911c340390a6": "my text value"
API v2
JSON

"custom_fields": {
  ...,
  "d4de1c1518b4531717c676029a45911c340390a6": "my text value",
  ...
}
Numeric Custom Field Format Changes
API v1
JSON

"d4de1c1518b4531717c676029a45911c340390a6": 500
API v2
JSON

"custom_fields": {
  ...,
  "d4de1c1518b4531717c676029a45911c340390a6": 500,
  ...
}
Currency Custom Field Format Changes
API v1
JSON

"d4de1c1518b4531717c676029a45911c340390a6": 500,
"d4de1c1518b4531717c676029a45911c340390a6_currency": "USD"
API v2
JSON

"custom_fields": {
  ...,
  "d4de1c1518b4531717c676029a45911c340390a6": {
  "value": 500,
  "currency": "USD"
},
...
}
Address Custom Field Format Changes
API v1
JSON

"d4de1c1518b4531717c676029a45911c340390a6": "530 Fifth Avenue, New York, NY, USA",
"d4de1c1518b4531717c676029a45911c340390a6_route": "5th Avenue",
"d4de1c1518b4531717c676029a45911c340390a6_subpremise": null, // no longer included, was always null
"d4de1c1518b4531717c676029a45911c340390a6_country": "United States",
"d4de1c1518b4531717c676029a45911c340390a6_locality": "New York",
"d4de1c1518b4531717c676029a45911c340390a6_postal_code": "10036",
"d4de1c1518b4531717c676029a45911c340390a6_sublocality": "Manhattan",
"d4de1c1518b4531717c676029a45911c340390a6_street_number": "530",
"d4de1c1518b4531717c676029a45911c340390a6_admin_area_level_1": "New York",
"d4de1c1518b4531717c676029a45911c340390a6_admin_area_level_2": "New York County"
"d4de1c1518b4531717c676029a45911c340390a6_formatted_address": "530 5th Ave, New York, NY 10036, USA",
API v2
Only value subfield is required when setting an address value. All other subfields are optional and will be set to null if not provided for both POST and PATCH requests.

JSON

"custom_fields": {
  ...,
  "d4de1c1518b4531717c676029a45911c340390a6": {
  "route": "5th Avenue",
  "value": "530 Fifth Avenue, New York, NY, USA",
  "country": "United States",
  "locality": "New York",
  "postal_code": "10036",
  "sublocality": "Manhattan",
  "street_number": "530",
  "admin_area_level_1": "New York",
  "admin_area_level_2": "New York County",
  "formatted_address": "530 5th Ave, New York, NY 10036, USA"
},
...
}
Single Option Custom Field Format Changes
API v1
JSON

"d4de1c1518b4531717c676029a45911c340390a6": "123" // ID of the selected option. Can be mapped to user presented value via field endpoints.
API v2
JSON

"custom_fields": {
  ...,
  "d4de1c1518b4531717c676029a45911c340390a6": 123, // option ID is now a number
  ...
}
Multiple Option Custom Field Format Changes
API v1
JSON

"d4de1c1518b4531717c676029a45911c340390a6": "123,456" // concatenated IDs of the selected option. Can be mapped to user presented value via field endpoints.
API v2
JSON

"custom_fields": {
  ...,
  "d4de1c1518b4531717c676029a45911c340390a6": [123, 456], // option IDs are now in an array as numeric values.
  ...
}
User, Person, Organization Custom Fields Format Changes
API v1
JSON

"d4de1c1518b4531717c676029a45911c340390a6": 1234 // ID of the user/person/org
API v2
JSON

"custom_fields": {
  ...,
  "d4de1c1518b4531717c676029a45911c340390a6": 1234, // ID of the user/person/org
  ...
}
Date Custom Field Format Changes
API v1
JSON

"d4de1c1518b4531717c676029a45911c340390a6": "2024-01-01"
API v2
JSON

"custom_fields": {
  ...,
  "d4de1c1518b4531717c676029a45911c340390a6": "2024-01-01",
  ...
}
Date Range Custom Field Format Changes
API v1
JSON

"d4de1c1518b4531717c676029a45911c340390a6": "2024-01-01"
"d4de1c1518b4531717c676029a45911c340390a6_until": "2024-02-01"
API v2
JSON

"custom_fields": {
  ...,
  "d4de1c1518b4531717c676029a45911c340390a6": {
  "value": "2024-01-01",
  "until": "2024-02-01"
},
...
}
Time Custom Field Format Changes
API v1
JSON

"d4de1c1518b4531717c676029a45911c340390a6": "09:00:00"
API v2
JSON

"custom_fields": {
  ...,
  "d4de1c1518b4531717c676029a45911c340390a6": "09:00:00",
  ...
}
Time Range Custom Field Format Changes
API v1
JSON

"d4de1c1518b4531717c676029a45911c340390a6": "09:00:00"
"d4de1c1518b4531717c676029a45911c340390a6_until": "11:00:00"
API v2
JSON

"custom_fields": {
  ...,
  "d4de1c1518b4531717c676029a45911c340390a6": {
  "value": "09:00:00",
  "until": "11:00:00"
},
...
}
Pagination
Offset based pagination (start & limit) has been replaced with cursor based pagination (cursor & limit), which makes iterating over large collections significantly faster. See Pagination for more information.

Sorting
Endpoints, which support sorting, now have 2 optional parameters (sort_by and sort_direction) instead of 1 (sort).
- sort_by accepted values: id, add_time, update_time plus a few additional fields depending on the entity. Defaults to id.
- sort_direction accepted values: asc, desc. Defaults to asc.

A maximum of 1 field to sort by can be provided.

Products API
Product Object
Changes Summary
Please note that this section does not include the changes already covered in General API Changes section.

first_char and files_count fields are no longer included
visible_to field type has changed from string to integer. Old possible values were "1", "3", "5", "7". New possible values are 1, 3, 5, 7.
selectable field has been renamed to is_linkable for clarity. When set to true, the product is linkable to deals.
active_flag field has been replaced with is_deleted. It is the negation of the old value. When an entity has is_deleted set to true, the entity is considered soft deleted and will be fully deleted after 30 days of last activity.
product_variations has been removed to a separate Product Variations API described below.
Old v1 Product Object Example
JSON

{
    "id": 3,
    "name": "Name",
    "code": "Code",
    "description": "Description",
    "unit": "Unit",
    "tax": 20,
    "category": "262",
    "active_flag": true, // replaced with is_deleted flag. NB: is_deleted is the negated value of the old active_flag.
    "selectable": true, // replaced with is_linkable flag
    "first_char": "n", // no longer included
    "visible_to": "7", // is now an integer
    "owner_id": { // Replaced with only the numeric id of the owner user
        "id": 6192726,
        "name": "Owner Name",
        "email": "owner.name@email.com",
        "has_pic": 1,
        "pic_hash": "08bcf87d30a6662032680b65bfa1b509",
        "active_flag": true,
        "value": 6192726
    },
    "files_count": null, // no longer included
    "add_time": "2021-01-11 17:30:10",
    "update_time": "2024-01-09 09:31:15",
    "prices": [
        {
            "id": 5, // no longer included
            "product_id": 3,
            "price": 54,
            "currency": "EUR",
            "cost": 0,
            "overhead_cost": 0,
            "price_formatted": "54 €" // no longer included
        }
    ],
    "product_variations": [], // moved to a separate product variations API
    "53c2f18db6a1655d6af8bba77d9679565f975fd8": "Text Custom Field", // wrapped in custom_fields object
    "d4de1c1518b4531717c676029a45911c340390a6": 2300, // wrapped in custom_fields object
    "d4de1c1518b4531717c676029a45911c340390a6_currency": "EUR" // wrapped in custom_fields object
}
New v2 Product Object Example
JSON

{
    "id": 3,
    "name": "Name",
    "tax": 20,
    "add_time": "2021-01-11T17:30:10Z",
    "update_time": "2024-01-09T09:31:15Z",
    "description": "Description",
    "code": "Code",
    "unit": "Unit",
    "owner_id": 6192726, // is no longer a user object, just the id
    "category": "262",
    "visible_to": 7, // is now an integer
    "is_deleted": false, // Replaces old 'active_flag' field. NB: is_deleted is the negated value of the old active_flag.
    "is_linkable": true, // Replaces old 'selectable' field
    "prices": [
        {
            "product_id": 3,
            "price": 54,
            "currency": "EUR",
            "cost": 0,
            "direct_cost": 0
        }
    ],
    "custom_fields": { // custom fields are no longer flat root level fields
        "53c2f18db6a1655d6af8bba77d9679565f975fd8": "Text Custom Field",
        "d4de1c1518b4531717c676029a45911c340390a6": {
            "value": 2300,
            "currency": "EUR"
        }
    }
}
GET /api/v1/products/:id to GET /api/v2/products/:id
Please note that this section does not include the changes already covered in General API Changes section.

Returned product object has changed, see Product Object for details.

GET /api/v1/products to GET /api/v2/products
Please note that this section does not include the changes already covered in General API Changes section.

Returned product object has changed, see Product Object for details.

sorting is only supported by id, add_time, update_time or name
optional parameter user_id has been renamed to owner_id. It allows filtering products by specific owner user.
get_summary and first_char parameters have been removed
POST /api/v1/products to POST /api/v2/products
Please note that this section does not include the changes already covered in General API Changes section.

Only the name field is required. Everything else is optional and expected in the format described in Product Object section.

It is no longer possible to create an already deleted entity with POST.
PUT /api/v1/products/:id to PATCH /api/v2/products/:id
Please note that this section does not include the changes already covered in General API Changes section.

Any fields changed are expected to be in the format described in Product Object section.

It is no longer possible to use PATCH (former PUT) requests to delete an entity. Use corresponding DELETE endpoint instead.
When updating prices, the whole existing array will be replaced with the passed array.
DELETE /api/v1/products to DELETE /api/v2/products
No changes other than version change in the URL.

Deal Products API
Deal Product Object
Changes Summary
Please note that this section does not include the changes already covered in General API Changes section.

product, order_nr, quantity_formatted and sum_formatted fields are no longer included.
active_flag has been removed as it was always true.
comments field can not be null anymore. If it is not set, it will be an empty string "".
Old v1 Deal Product Object Example
JSON

{
    "id": 1,
    "deal_id": 1,
    "product_id": 1,
    "product_variation_id": null,
    "name": "Name",
    "order_nr": 1, // no longer included
    "item_price": 10,
    "quantity": 3,
    "duration": 1,
    "duration_unit": null,
    "sum": 30,
    "tax": 0,
    "tax_method": "inclusive",
    "currency": "EUR",
    "active_flag": true, // removed, was always true
    "enabled_flag": true, // renamed to is_enabled
    "add_time": "2020-11-12 12:10:45",
    "last_edit": "2022-11-12 12:10:45", // renamed to update_time
    "comments": null, // can not be null anymore. If not set, is an empty string instead.
    "quantity_formatted": "3", // no longer included
    "sum_formatted": "30 €", // no longer included
    "discount": 0,
    "discount_type": "percentage",
    "product": null // no longer included
}
New v2 Deal Product Object Example
JSON

{
    "id": 1,
    "deal_id": 1,
    "product_id": 1,
    "product_variation_id": null,
    "name": "Name",
    "item_price": 10,
    "quantity": 3,
    "sum": 30,
    "tax": 0,
    "tax_method": "inclusive",
    "currency": "EUR",
    "is_enabled": true, // renamed from enabled_flag
    "add_time": "2020-11-12T12:10:45Z",
    "update_time": "2022-11-12T12:10:45Z", // renamed from last_edit
    "comments": "", // can not be null anymore
    "discount": 0,
    "discount_type": "percentage"
}
GET /api/v1/deals/:id/products to GET /api/v2/deals/:id/products or GET /api/v2/deals/products?deal_ids=..,..
Please note that this section does not include the changes already covered in General API Changes section.

Returned product object has changed, see Deal Product Object for details.

New alternative endpoint is available to fetch multiple deals' products at once: GET /api/v2/deals/products. You can fetch up to 100 deals products at once by providing a comma separated list of deal IDs in deal_ids querystring parameter.
POST /api/v1/deals/:id/products to POST /api/v2/deals/:id/products
Please note that this section does not include the changes already covered in General API Changes section.

Keys are expected in the format described in Deal Product Object section.

It is no longer possible to create an already deleted entity with POST.
PUT /api/v1/deals/:id/products/:id to PATCH /api/v2/deals/:id/products/:id
Any fields changed are expected to be in the format described in Deal Product Object section.

It is no longer possible to use PATCH (former PUT) requests to delete an entity. Use the corresponding DELETE endpoint instead.
DELETE /api/v1/deals/:id/products to DELETE /api/v2/deals/:id/products
No changes other than version change in the URL.

Product Variations API
Product Variation Object
Changes Summary
Please note that this section does not include the changes already covered in General API Changes section.

Previously product variations were returned as part of the main products API. They have now been moved to a separate API with the following endpoints:

GET /api/v2/products/:id/variations
POST /api/v2/products/:id/variations
PATCH /api/v2/products/:id/variations/:id
DELETE /api/v2/products/:id/variations/:id
The prices object no longer includes the following fields: id, product_id, comment and price_formatted.

Old v1 Product Variation Object Example (within old v1/products API)
JSON

{
    "id": 1,
    "name": "Variation 1",
    "product_id": 1,
    "prices": [
        {
            "id": 1, // no longer included
            "product_id": 1, // no longer included within price object, use root level field instead
            "product_variation_id": 1,
            "price": 10,
            "currency": "EUR",
            "cost": 20,
            "comment": "", // no longer included
            "price_formatted": "10 €" // no longer included
        }
    ]
}
New v2 Product Variation Object Example
JSON

{
    "id": 1,
    "name": "Variation 1",
    "product_id": 1,
    "prices": [
        {
            "product_variation_id": 1,
            "price": 10,
            "currency": "EUR",
            "cost": 20
        }
    ]
}
Search API
GET /api/v1/deals/search to GET /api/v2/deals/search
GET /api/v1/persons/search to GET /api/v2/persons/search
GET /api/v1/organizations/search to GET /api/v2/organizations/search
GET /api/v1/leads/search to GET /api/v2/leads/search
GET /api/v1/products/search to GET /api/v2/products/search
GET /api/v1/itemSearch to GET /api/v2/itemSearch
Only change is a switch to cursor based pagination (cursor and limit instead of start and limit). See Pagination for more information.

GET /api/v1/itemSearch/field to GET /api/v2/itemSearch/field
The endpoint now uses cursor based pagination. See Pagination for more information.
field_key parameter has been renamed to field.
field_type parameter has been renamed to entity_type.
entity_type accepted values have been simplified to just deal, lead , person, organization, product, project from previous dealField, leadField etc.
return_item_ids parameter has been removed, the response always includes item ids now.
exact_match boolean parameter has been replaced with a string match parameter. Accepted values are
exact - fastest. Matches only if the field value is exactly the same as the term.
beginning - fast. Matches fields by beginning, e.g. finds my field value with my fie
middle - slowest. Old default behaviour. Matches fields by any substring, e.g. finds my field value with ld va. We recommend using other types of matching where possible for best experience.
Pipelines API
Pipeline Object
Changes Summary
Please note that this section does not include the changes already covered in General API Changes section.

url_title field is no longer included.
selected field has been renamed to is_selected for clarity. When set to true, the product is linkable to deals.
active_flag field has been replaced with is_deleted. It is the negation of the old value. When an entity has is_deleted set to true, the entity is considered soft deleted and will be fully deleted after 30 days of last activity.
order_nr is now read-only. When creating a new pipeline, it is placed at the end of existing Pipelines list. If user wants, they can reorder pipelines in the UI.
Old v1 Pipeline Object Example
JSON

{
    "id": 1,
    "name": "Sales Pipeline",
    "url_title": "Sales-Pipeline", //  removed
    "order_nr": 1,
    "active": true, // replaced with is_deleted. NB: Negation of the old value.
    "deal_probability": false, // replaced with is_deal_probability_enabled
    "add_time": "2018-09-03 17:05:08", 
    "update_time": "2018-09-04 12:46:03",
    "selected": true // renamed to is_selected
}
New v2 Pipeline Object Example
JSON

{
    "id": 1,
    "name": "Sales Pipeline",
    "order_nr": 1,
    "is_deleted": false, // replaces "active". NB: Negation of the old value.
    "is_deal_probability_enabled": false, // replaces "deal_probability"
    "add_time": "2018-09-03T17:05:08Z",
    "update_time": "2018-09-04T12:46:03Z",
    "is_selected": true // renamed from "selected"
}
GET /api/v1/pipelines/:id to GET /api/v2/pipelines/:id
Please note that this section does not include the changes already covered in General API Changes section.

Returned pipeline object has changed, see Pipeline Object for details.

GET /api/v1/pipelines to GET /api/v2/pipelines
Please note that this section does not include the changes already covered in General API Changes section.

Returned pipeline object has changed, see Pipeline Object for details.

POST /api/v1/pipelines to POST /api/v2/pipelines
Please note that this section does not include the changes already covered in General API Changes section.

Only the name field is required. Everything else is optional and expected in the format described in Pipeline Object section.

It is no longer possible to create an already deleted entity with POST.
PUT /api/v1/pipelines/:id to PATCH /api/v2/pipelines/:id
Please note that this section does not include the changes already covered in General API Changes section.

Any fields changed are expected to be in the format described in Pipeline Object section.

It is no longer possible to use PATCH (former PUT) requests to delete an entity. Use corresponding DELETE endpoint instead.
DELETE /api/v1/pipelines to DELETE /api/v2/pipelines
No changes other than version change in the URL.

Stages API
Stage Object
Changes Summary
Please note that this section does not include the changes already covered in General API Changes section.

pipeline_name and pipeline_deal_probability fields have been removed. Query the pipeline object if you need these.
rotten_flag has been replaced with is_deal_rot_enabled flag.
rotten_days has been replaced with days_to_rotten for clarity.
active_flag field has been replaced with is_deleted. It is the negation of the old value.
Old v1 Stage Object Example
JSON

{
    "id": 1,
    "order_nr": 1,
    "name": "Lead In",
    "active_flag": true, // replaced with is_deleted. NB: Negation of the old value.
    "deal_probability": 100,
    "pipeline_id": 1,
    "pipeline_name": "Sales Pipeline", // removed, query pipeline API instead
    "pipeline_deal_probability": false, // removed, query pipeline API instead
    "rotten_flag": false, // replaced with is_deal_rot_enabled
    "rotten_days": null, // replaced with days_to_rotten
    "add_time": "2018-09-04 06:24:59",
    "update_time": null
} 
New v2 Stage Object Example
JSON

{
    "id": 1,
    "order_nr": 1,
    "name": "Lead In",
    "is_deleted": false, // replaces "active_flag". NB: Negation of the old value.
    "deal_probability": 100,
    "pipeline_id": 1,
    "is_deal_rot_enabled": false, // replaces "rotten_flag"
    "days_to_rotten": null, // replaces "rotten_days"
    "add_time": "2018-09-04T06:24:59Z",
    "update_time": null
}
GET /api/v1/stages/:id to GET /api/v2/stages/:id
Please note that this section does not include the changes already covered in General API Changes section.

Returned stage object has changed, see Stage Object for details.

GET /api/v1/stages to GET /api/v2/stages
Please note that this section does not include the changes already covered in General API Changes section.

Returned stage object has changed, see Stage Object for details.

POST /api/v1/stages to POST /api/v2/stages
Please note that this section does not include the changes already covered in General API Changes section.

Only the name field is required. Everything else is optional and expected in the format described in Stage Object section.

It is no longer possible to create an already deleted entity with POST.
PUT /api/v1/stages/:id to PATCH /api/v2/stages/:id
Please note that this section does not include the changes already covered in General API Changes section.

Any fields changed are expected to be in the format described in Stage Object section.

It is no longer possible to use PATCH (former PUT) requests to delete an entity. Use corresponding DELETE endpoint instead.
DELETE /api/v1/stages to DELETE /api/v2/stages
No changes other than version change in the URL.

Deals API
Deal Object
Changes Summary
Please note that this section does not include the changes already covered in General API Changes section.

creator_user_id, user_id, person_id and org_idfields no longer contain an object but the relevant id.
user_id field has been renamed to owner_id for clarity and consistency with other entities.
deleted boolean field has been renamed to is_deleted. This is so all entities have a consistently named field for deleted status. When an entity has is_deleted set to true, the entity is considered soft deleted and will be fully deleted after 30 days of last activity.
The following fields are only included in the response when providing these field keys as comma separated string using the include_fields querystring parameter: next_activity_id, last_activity_id, first_won_time, products_count, files_count, notes_count, followers_count, email_messages_count, activities_count, done_activities_count, undone_activities_count , participants_count, last_incoming_mail_time, last_outgoing_mail_time.
label field has been replaced with label_ids field. Old field value was a comma concatenated string of label ids (e.g. "3,7", new value is an array of ids (e.g. [3, 7]).
visible_tofield type has changed from string to integer. Old possible values were"1", "3", "5", "7". New possible values are 1, 3, 5, 7.
active boolean field has been removed. It represented the condition status == 'open' which can be used directly instead.
weighted_value´has been removed. The value can be derived as value * probability/100.
next_activity_date, next_activity_time, next_activity_subject, next_activity_type, next_activity_duration, next_activity_note have been removed. They can be fetched via activities API using the optional field next_activity_id.
last_activity_date has been removed. It can be fetched via activities API using the optional field last_activity_id.
owner_name, person_name, org_name, org_hidden and person_hidden fields have been removed. They can be fetched via relevant APIs using the relevant id fields.
formatted_value, formatted_weighted_value, stage_order_nr fields have been removed.
Statistics fields average_time_to_won, average_stage_progress and stay_in_pipeline_stages have been removed.
acv_currency, arr_currency and mrr_currency fields have been removed. Their value was always equivalent to the value of currency.
Old v1 Deal Object Example
JSON

{
	"id": 1,
	"title": "Deal",
	"creator_user_id": { // Replaced with plain ID
	"id": 18,
	"name": "User Name",
	"email": "user@pipedrive.com",
	"has_pic": 0,
	"pic_hash": null,
	"active_flag": true,
	"value": 18
	},
	"user_id": { // Replaced with plain ID and renamed to `owner_id`
		"id": 18,
		"name": "User Name",
		"email": "user@pipedrive.com",
		"has_pic": 0,
		"pic_hash": null,
		"active_flag": true,
		"value": 18
	},
	"person_id": { // Replaced with plain ID
		"active_flag": true,
		"name": "Person",
		"email": [
		  {
		  "value": "",
		  "primary": true
		  }
		],
		"phone": [
		  {
		  "value": "",
		  "primary": true
		  }
		],
		"owner_id": 18,
		"value": 1
	},
	"org_id": { // Replaced with plain ID
		"name": "Org",
		"people_count": 0,
		"owner_id": 18,
		"address": null,
		"active_flag": true,
		"cc_email": "mycompany@mycompany.pipedrivemail.com",
		"label_ids": [],
		"owner_name": "User Name",
		"value": 1
	},
	"pipeline_id": 1,
	"stage_id": 2,
	"value": 0,
	"acv": 42,
	"acv_currency": "USD", // Removed,  use `currency` instead
	"mrr": 69,
	"mrr_currency": "USD", // Removed,  use `currency` instead
	"arr": 50,
	"arr_currency": "USD", // Removed,  use `currency` instead
	"currency": "USD",
	"add_time": "2024-07-01 05:46:33", // now in TZ format
	"update_time": "2024-07-01 11:29:32", // now in TZ format
	"stage_change_time": "2024-07-01 05:49:13", // now in TZ format
	"active": false, // Removed. active = true is equivalent to status = "open"
	"deleted": false, // Renamed to `is_deleted`
	"status": "won",
	"probability": null,
	"next_activity_id": null, // Included only when using `include_fields` parameter
	"next_activity_date": null, // Removed
	"next_activity_time": null, // Removed
	"next_activity_subject": null, // Removed
	"next_activity_type": null, // Removed
	"next_activity_duration": null, // Removed
	"next_activity_note": null, // Removed
	"last_activity_id": null, // Included only when using `include_fields` parameter
	"last_activity_date": null, // Removed
	"lost_reason": null,
	"visible_to": "3", // Is an integer now
	"close_time": "2024-07-01 05:50:19", // now in TZ format
	"won_time": "2024-07-01 05:50:19", // now in TZ format
	"first_won_time": "2024-07-01 05:50:19", // now in TZ format, included only when using `include_fields` parameter
	"expected_close_date": null,		
	"lost_time": null,
	"products_count": 0, // Included only when using `include_fields` parameter
	"files_count": 0, // Included only when using `include_fields` parameter
	"notes_count": 0, // Included only when using `include_fields` parameter
	"followers_count": 1, // Included only when using `include_fields` parameter
	"email_messages_count": 0, // Included only when using `include_fields` parameter
	"activities_count": 0, // Included only when using `include_fields` parameter
	"done_activities_count": 0, // Included only when using `include_fields` parameter
	"undone_activities_count": 0, // Included only when using `include_fields` parameter
	"participants_count": 1, // Included only when using `include_fields` parameter
	"last_incoming_mail_time": null, // Included only when using `include_fields` parameter
	"last_outgoing_mail_time": null, // Included only when using `include_fields` parameter
	"label": "2,3", // Replaced with `label_ids` array of IDs
	"local_won_date": "2024-07-01",
	"local_lost_date": null,
	"local_close_date": "2024-07-01",
	"origin": "ManuallyCreated",
	"origin_id": null,
	"channel": null,
	"channel_id": null,
	"stage_order_nr": 1, // removed
	"person_name": "Person", // removed
	"org_name": "Org", // removed
	"org_hidden": false, // removed
	"person_hidden": false, // removed
	"formatted_value": "$0", // removed
	"weighted_value": 0, // removed
	"formatted_weighted_value": "$0", // removed
	"weighted_value_currency": "USD", // removed
	"rotten_time": null,
	"owner_name": "User Name", // removed
	"cc_email": "mycompany+deal1@mycompany.pipedrivemail.com",
	"53c2f18db6a1655d6af8bba77d9679565f975fd8": "Text Custom Field", // wrapped in custom_fields object
	"d4de1c1518b4531717c676029a45911c340390a6": 2300, // wrapped in custom_fields object
	"d4de1c1518b4531717c676029a45911c340390a6_currency": "EUR" // wrapped in custom_fields object
}
New v2 Deal Object Example
JSON

{
      "id": 1,
      "title": "Deal",
      "value": 0.0,
      "creator_user_id": 18, // No longer an object
      "person_id": 1, // No longer an object
      "org_id": 1, // No longer an object
      "stage_id": 2,
      "pipeline_id": 1,
      "currency": "USD",
      "add_time": "2024-07-01T05:46:33Z", // In TZ format now
      "update_time": "2024-07-01T11:29:32Z", // In TZ format now
      "close_time": "2024-07-01T05:50:19Z", // In TZ format now
      "won_time": "2024-07-01T05:50:19Z", // In TZ format now
      "stage_change_time": "2024-07-01T05:49:13Z", // In TZ format now
      "status": "won",
      "probability": null,
      "lost_reason": null,
      "visible_to": 3, // No longer a string
      "lost_time": null,
      "local_won_date": "2024-07-01",
      "local_lost_date": null,
      "local_close_date": "2024-07-01",
      "expected_close_date": null,
      "owner_id": 18, // Renamed from `user_id`
      "label_ids": [], // Replaces `label` field.
      "is_deleted": false, // Renamed from `deleted`
      "acv": 42.0,
      "arr": 50.0,
      "mrr": 69.0,
      "custom_fields": { // custom fields are no longer flat root level fields
          "53c2f18db6a1655d6af8bba77d9679565f975fd8": "Text Custom Field",
          "d4de1c1518b4531717c676029a45911c340390a6": {
            "value": 2300,
            "currency": "EUR"
    			}
			}
GET /api/v1/deals/:id to GET /api/v2/deals/:id
Please note that this section does not include the changes already covered in General API Changes section.

Returned deal object has changed, see Deal Object for details.

custom_fields parameter has been added to optionally return only a subset of custom fields. Multiple custom field keys can be provided by separating them with commas. This can be used to reduce the response size and time.
include_fields parameter has been added to optionally include some values that are not part of the default response. Multiple fields can be included by separating them with commas. Supported optional fields are next_activity_id, last_activity_id, first_won_time, products_count, files_count, notes_count, followers_count, email_messages_count, activities_count, done_activities_count, undone_activities_count,participants_count, last_incoming_mail_time, last_outgoing_mail_time.
GET /api/v1/deals to GET /api/v2/deals
Note that GET /api/v2/deals also replaces the following v1 endpoints:

GET /api/v1/persons/:id/deals;
GET /api/v1/organizations/:id/deals;
GET /api/v1/pipelines/:id/deals;
GET /api/v1/stages/:id/deals.
Please note that this section does not include the changes already covered in General API Changes section.

Returned deal object has changed, see Deal Object for details.

custom_fields parameter has been added to optionally return only a subset of custom fields. Multiple custom field keys can be provided by separating them with commas. This can be used to reduce the response size and time.
optional parameter user_id has been renamed to owner_id. It allows filtering deals by specific owner user.
Additional quick filtering querystring parameters have been added: person_id, org_id, pipeline_id, stage_id.
include_fields parameter has been added to optionally include some values that are not part of the default response. Multiple fields can be included by separating them with commas. Supported optional fields are next_activity_id, last_activity_id, first_won_time, products_count, files_count, notes_count, followers_count, email_messages_count, activities_count, done_activities_count, undone_activities_count,participants_count, last_incoming_mail_time, last_outgoing_mail_time.
status querystring parameter only accepts values open, won, lost, deleted. Multiple statuses can be provided at once when separated with commas.
owned_by_you querystring parameter has been removed.
POST /api/v1/deals to POST /api/v2/deals
Please note that this section does not include the changes already covered in General API Changes section.

Only the title field is required. Everything else is optional and expected in the format described in Deal Object section.

It is no longer possible to create an already deleted entity with POST.
PUT /api/v1/deals/:id to PATCH /api/v2/deals/:id
Please note that this section does not include the changes already covered in General API Changes section.

Any fields changed are expected to be in the format described in Deal Object section.

It is no longer possible to use PATCH (former PUT) requests to delete an entity. Use corresponding DELETE endpoint instead.
DELETE /api/v1/deals to DELETE /api/v2/deals
No changes other than version change in the URL.


Persons API
Person Object
Changes Summary
Please note that this section does not include the changes already covered in General API Changes section.

picture_id, owner_id, and org_idfields no longer contain an object but the relevant id.
is_active boolean field has been renamed to is_deleted and the old value negated. This is so all entities have a consistently named field for deleted status. When an entity has is_deleted set to true, the entity is considered soft deleted and will be fully deleted after 30 days of last activity.
The following fields are only included in the response when providing these field keys as comma separated string using the include_fields querystring parameter: next_activity_id, last_activity_id, open_deals_count, related_open_deals_count, closed_deals_count, related_closed_deals_count, participant_open_deals_count, participant_closed_deals_count, email_messages_count, activities_count, done_activities_count, undone_activities_count , files_count, notes_count, followers_count, won_deals_count, related_won_deals_count, lost_deals_count, related_lost_deals_count, last_incoming_mail_time, last_outgoing_mail_time, marketing_status, doi_status.
label field has been replaced with label_ids field. Old field value was a comma concatenated string of label ids (e.g. "3,7", new value is an array of ids (e.g. [3, 7]).
visible_tofield type has changed from string to integer. Old possible values were"1", "3", "5", "7". New possible values are 1, 3, 5, 7.
next_activity_date and next_activity_time have been removed. They can be fetched via activities API using the optional field next_activity_id.
last_activity_date has been removed. It can be fetched via activities API using the optional field last_activity_id.
owner_name and org_name fields have been removed. They can be fetched via relevant APIs using the relevant id fields.
delete_time field has been removed. If the person has is_deleted: true, update_time is the delete_time.
company_id and first_char fields have been removed.
phone, email and im fields have been renamed to phones, emails and ims as they contain multiple elements.
Fields job_title, notes, birthday, postal_address and ims are only included if the company has contact sync feature enabled.
postal_address is now formatted as an object like an address type custom field instead of being spread across multiple fields. See General API Changes for more info.
Old v1 Person Object Example
JSON

{
  "id": 1,
  "company_id": 123, // Removed
  "name": "First Last",
  "first_name": "First",
  "last_name": "Last",
  "first_char": "f", // Removed
  "owner_id": { // Replaced with plain ID
    "id": 18,
    "name": "User Name",
    "email": "user@pipedrive.com",
    "has_pic": 0,
    "pic_hash": null,
    "active_flag": true,
    "value": 18
  },
  "org_id": { // Replaced with plain ID
    "name": "Org",
    "people_count": 0,
    "owner_id": 18,
    "address": null,
    "active_flag": true,
    "cc_email": "mycompany@mycompany.pipedrivemail.com",
    "label_ids": [],
    "owner_name": "User Name",
    "value": 1
  },
  "picture_id": { // Replaced with plain ID
    "item_type": "person",
    "item_id": 1,
    "active_flag": true,
    "add_time": "2024-08-12 12:14:32",
    "update_time": "0000-00-00 00:00:00",
    "added_by_user_id": 6192726,
    "file_size": 5445,
    "pictures": {
      "128": "https://....jpg",
      "512": "https://....jpg"
    },
    "value": 2
  },
  "add_time": "2024-07-01 05:46:33", // now in TZ format
  "update_time": "2024-07-01 11:29:32", // now in TZ format
  "active_flag": true, // Replaced with `is_deleted`, NB: It is negation of old value
  "next_activity_id": null, // Included only when using `include_fields` parameter
  "next_activity_date": null, // Removed
  "next_activity_time": null, // Removed
  "last_activity_id": null, // Included only when using `include_fields` parameter
  "last_activity_date": null, // Removed
  "visible_to": "3", // Is an integer now
  "open_deals_count": 1, // Included only when using `include_fields` parameter
  "related_open_deals_count": 0, // Included only when using `include_fields` parameter
  "closed_deals_count": 1, // Included only when using `include_fields` parameter
  "related_closed_deals_count": 0, // Included only when using `include_fields` parameter
  "participant_open_deals_count": 0, // Included only when using `include_fields` parameter
  "participant_closed_deals_count": 0, // Included only when using `include_fields` parameter
  "email_messages_count": 0, // Included only when using `include_fields` parameter
  "activities_count": 1, // Included only when using `include_fields` parameter
  "done_activities_count": 1, // Included only when using `include_fields` parameter
  "undone_activities_count": 0, // Included only when using `include_fields` parameter
  "files_count": 0, // Included only when using `include_fields` parameter
  "notes_count": 1, // Included only when using `include_fields` parameter
  "followers_count": 1, // Included only when using `include_fields` parameter
  "won_deals_count": 1, // Included only when using `include_fields` parameter
  "related_won_deals_count": 0, // Included only when using `include_fields` parameter
  "lost_deals_count": 0, // Included only when using `include_fields` parameter
  "related_lost_deals_count": 0, // Included only when using `include_fields` parameter
  "last_incoming_mail_time": null, // Included only when using `include_fields` parameter
  "last_outgoing_mail_time": null, // Included only when using `include_fields` parameter
  "label": "2,3", // Replaced with `label_ids` array of IDs
  "org_name": "Org", // removed
  "owner_name": "User Name", // removed
  "cc_email": "mycompany@mycompany.pipedrivemail.com",
  "phone": [ // Replaced with 'phones'
    {
      "label": "work",
      "value": "555-555-0172",
      "primary": true
    },
    {
      "label": "home",
      "value": "55123456",
      "primary": false
    },
  ],
  "email": [ // Replaced with 'emails'
    {
      "label": "work",
      "value": "main@email.com",
      "primary": true
    },
    {
      "label": "work",
      "value": "another@email.com",
      "primary": false
    }
  ],
  "53c2f18db6a1655d6af8bba77d9679565f975fd8": "Text Custom Field", // wrapped in custom_fields object
  "d4de1c1518b4531717c676029a45911c340390a6": 2300, // wrapped in custom_fields object
  "d4de1c1518b4531717c676029a45911c340390a6_currency": "EUR" // wrapped in custom_fields object
}
New v2 Person Object Example
JSON

{
  "id": 1,
  "name": "First Last",
  "first_name": "First",
  "last_name": "Last",
  "org_id": 1, // No longer an object
  "add_time": "2024-07-01T05:46:33Z", // In TZ format now
  "update_time": "2024-07-01T11:29:32Z", // In TZ format now
  "visible_to": 3, // No longer a string
  "owner_id": 18, // No longer an object
  "picture_id": 1, // No longer an object
  "label_ids": [], // Replaces `label` field.
  "is_deleted": false, // Replaces `active_flag` field. NB: Is negation of old value.
  "phones": [ // Renamed from `phone`
    {
      "label": "work",
      "value": "555-555-0172",
      "primary": true
    },
    {
      "label": "home",
      "value": "55123456",
      "primary": false
    },
  ],
  "emails": [ // Renamed from `email`
    {
      "label": "work",
      "value": "main@email.com",
      "primary": true
    },
    {
      "label": "work",
      "value": "another@email.com",
      "primary": false
    }
  ],
  "custom_fields": { // custom fields are no longer flat root level fields
      "53c2f18db6a1655d6af8bba77d9679565f975fd8": "Text Custom Field",
      "d4de1c1518b4531717c676029a45911c340390a6": {
    "value": 2300,
    "currency": "EUR"
      }
  }
}
GET /api/v1/persons/:id to GET /api/v2/persons/:id
Please note that this section does not include the changes already covered in General API Changes section.

Returned person object has changed, see Person Object for details.

custom_fields parameter has been added to optionally return only a subset of custom fields. Multiple custom field keys can be provided by separating them with commas. This can be used to reduce the response size and time.
include_fields parameter has been added to optionally include some values that are not part of the default response. Multiple fields can be included by separating them with commas. Supported optional fields are next_activity_id, last_activity_id, open_deals_count, related_open_deals_count, closed_deals_count, related_closed_deals_count, participant_open_deals_count, participant_closed_deals_count, email_messages_count, activities_count, done_activities_count, undone_activities_count , files_count, notes_count, followers_count, won_deals_count, related_won_deals_count, lost_deals_count, related_lost_deals_count, last_incoming_mail_time, last_outgoing_mail_time, marketing_status, doi_status.
marketing_status and doi_status can only be included if the company has marketing app access.
GET /api/v1/persons to GET /api/v2/persons
Note that GET /api/v2/persons also replaces GET /api/v1/organizations/:id/persons endpoint.

Please note that this section does not include the changes already covered in General API Changes section.

Returned person object has changed, see Person Object for details.

custom_fields parameter has been added to optionally return only a subset of custom fields. Multiple custom field keys can be provided by separating them with commas. This can be used to reduce the response size and time.
Additional quick filtering querystring parameter org_id has been added.
include_fields parameter has been added to optionally include some values that are not part of the default response. Multiple fields can be included by separating them with commas. Supported optional fields are next_activity_id, last_activity_id, open_deals_count, related_open_deals_count, closed_deals_count, related_closed_deals_count, participant_open_deals_count, participant_closed_deals_count, email_messages_count, activities_count, done_activities_count, undone_activities_count , files_count, notes_count, followers_count, won_deals_count, related_won_deals_count, lost_deals_count, related_lost_deals_count, last_incoming_mail_time, last_outgoing_mail_time, marketing_status, doi_status.
marketing_status and doi_status can only be included if the company has marketing app access.
POST /api/v1/persons to POST /api/v2/persons
Please note that this section does not include the changes already covered in General API Changes section.

Only the name field is required. Everything else is optional and expected in the format described in Person Object section.

It is no longer possible to create an already deleted entity with POST.
Either name or both first_name and last_name must be provided.
If name is provided, first_name and last_name are derived from splitting the name with the same logic as in v1 API.
If first_name and last_name are provided, name is created by concatenating these.
Empty strings are accepted for first_name and last_name, but both can not be empty strings at the same time.
Phones, emails and IMs can only be sent as an object. The expected format is

{
    "phones": [{"value": "55123456", "label": "anything", "primary": true }, ... {}],
    "emails": [{"value": "example@email.com", "label": "anything", "primary": true }, ... {}],
    "im": [{"value": "username", "label": "anything", "primary": true }, ... {}],
}
Only the value field is required.
label is optional and will default to work.
primary is optional and at most only 1 value for each field type can be marked as primary. If none are marked as primary, the first value is marked as primary.
PUT /api/v1/persons/:id to PATCH /api/v2/persons/:id
Please note that this section does not include the changes already covered in General API Changes section.

Any fields changed are expected to be in the format described in Person Object section.

It is no longer possible to use PATCH (former PUT) requests to delete an entity. Use corresponding DELETE endpoint instead.
When updating the person's name, either name or both first_name and last_name must be provided.
If name is provided, first_name and last_name are derived from splitting the name with the same logic as in v1 API.
If first_name and last_name are provided, name is created by concatenating these.
Empty strings are accepted for first_name and last_name, but both can not be empty strings at the same time.
Phones, emails and IMs can only be sent as an object. The expected format is

{
    "phones": [{"value": "55123456", "label": "anything", "primary": true }, ... {}],
    "emails": [{"value": "example@email.com", "label": "anything", "primary": true }, ... {}],
    "im": [{"value": "username", "label": "anything", "primary": true }, ... {}],
}
Only the value field is required.
label is optional and will default to work.
primary is optional and at most only 1 value for each field type can be marked as primary. If none are marked as primary, the first value is marked as primary.
DELETE /api/v1/persons to DELETE /api/v2/persons
No changes other than version change in the URL.

Organizations API
Organization Object
Changes Summary
Please note that this section does not include the changes already covered in General API Changes section.

owner_id field no longer contain an object but the relevant user id.
is_active boolean field has been renamed to is_deleted and the old value negated. This is so all entities have a consistently named field for deleted status. When an entity has is_deleted set to true, the entity is considered soft deleted and will be fully deleted after 30 days of last activity.
The following fields are only included in the response when providing these field keys as comma separated string using the include_fields querystring parameter: next_activity_id, last_activity_id, open_deals_count, related_open_deals_count, closed_deals_count, related_closed_deals_count, participant_open_deals_count, participant_closed_deals_count, email_messages_count, activities_count, done_activities_count, undone_activities_count , files_count, notes_count, followers_count, won_deals_count, related_won_deals_count, lost_deals_count, related_lost_deals_count, last_incoming_mail_time, last_outgoing_mail_time, marketing_status, doi_status.
label field has been replaced with label_ids field. Old field value was a comma concatenated string of label ids (e.g. "3,7", new value is an array of ids (e.g. [3, 7]).
visible_tofield type has changed from string to integer. Old possible values were"1", "3", "5", "7". New possible values are 1, 3, 5, 7.
next_activity_date and next_activity_time have been removed. They can be fetched via activities API using the optional field next_activity_id.
last_activity and next_activity objects have been removed.
last_activity_date has been removed. It can be fetched via activities API using the optional field last_activity_id.
owner_name field has been removed. It can be fetched via users API using owner_id field.
delete_time field has been removed. If the organization has is_deleted: true, update_time is the delete_time.
company_id, category_id, edit_name, country_code and first_char fields have been removed.
address is now formatted as an object like an address type custom field instead of being spread across multiple fields. See General API Changes for more info.
Old v1 Organization Object Example
JSON

{
  "id": 1,
  "company_id": 123, // Removed
  "name": "Organization Nname",
  "first_char": "o", // Removed
  "owner_id": { // Replaced with plain ID
    "id": 18,
    "name": "User Name",
    "email": "user@pipedrive.com",
    "has_pic": 0,
    "pic_hash": null,
    "active_flag": true,
    "value": 18
  },
  "add_time": "2024-07-01 05:46:33", // now in TZ format
  "update_time": "2024-07-01 11:29:32", // now in TZ format
  "active_flag": true, // Replaced with `is_deleted`, NB: It is negation of old value
  "next_activity_id": null, // Included only when using `include_fields` parameter
  "next_activity_date": null, // Removed
  "next_activity_time": null, // Removed
  "last_activity_id": null, // Included only when using `include_fields` parameter
  "last_activity_date": null, // Removed
  "visible_to": "3", // Is an integer now
  "next_activity_id": 1, // Included only when using `include_fields` parameter
  "last_activity_id": 1, // Included only when using `include_fields` parameter
  "open_deals_count": 0, // Included only when using `include_fields` parameter
  "related_open_deals_count": 0, // Included only when using `include_fields` parameter
  "closed_deals_count": 0, // Included only when using `include_fields` parameter
  "related_closed_deals_count": 0, // Included only when using `include_fields` parameter
  "email_messages_count": 0, // Included only when using `include_fields` parameter
  "people_count": 0, // Included only when using `include_fields` parameter
  "activities_count": 0, // Included only when using `include_fields` parameter
  "done_activities_count": 0, // Included only when using `include_fields` parameter
  "undone_activities_count": 0, // Included only when using `include_fields` parameter
  "files_count": 0, // Included only when using `include_fields` parameter
  "notes_count": 0, // Included only when using `include_fields` parameter
  "followers_count": 0, // Included only when using `include_fields` parameter
  "won_deals_count": 0, // Included only when using `include_fields` parameter
  "related_won_deals_count": 0, // Included only when using `include_fields` parameter
  "lost_deals_count": 0, // Included only when using `include_fields` parameter
  "related_lost_deals_count": 0, // Included only when using `include_fields` parameter
  "label": "2,3", // Replaced with `label_ids` array of IDs
  "last_activity": { ... }, // Removed
  "next_activity": { ... }, // Removed
  "owner_name": "User Name", // Removed
  "address": "Eiffel Tower, Avenue Gustave Eiffel, Paris, France", // Nested object now
  "address_subpremise": "",
  "address_street_number": "",
  "address_route": "Avenue Gustave Eiffel",
  "address_sublocality": "",
  "address_locality": "Paris",
  "address_admin_area_level_1": "Île-de-France",
  "address_admin_area_level_2": "Département de Paris",
  "address_country": "France",
  "address_postal_code": "75007",
  "address_formatted_address": "Av. Gustave Eiffel, 75007 Paris, France",
  "cc_email": "mycompany@mycompany.pipedrivemail.com",
  "53c2f18db6a1655d6af8bba77d9679565f975fd8": "Text Custom Field", // wrapped in custom_fields object
  "d4de1c1518b4531717c676029a45911c340390a6": 2300, // wrapped in custom_fields object
  "d4de1c1518b4531717c676029a45911c340390a6_currency": "EUR" // wrapped in custom_fields object
}
New v2 Organization Object Example
JSON

{
  "id": 1,
  "name": "Organization Name",
  "add_time": "2024-07-01T05:46:33Z", // In TZ format now
  "update_time": "2024-07-01T11:29:32Z", // In TZ format now
  "visible_to": 3, // No longer a string
  "owner_id": 18, // No longer an object
  "picture_id": 1, // No longer an object
  "label_ids": [], // Replaces `label` field.
  "is_deleted": false, // Replaces `active_flag` field. NB: Is negation of old value.
  "address": { // Is a nested object now
    "value": "Eiffel Tower, Avenue Gustave Eiffel, Paris, France",
    "street_number": "",
    "route": "Avenue Gustave Eiffel",
    "sublocality": "",
    "locality": "Paris",
    "admin_area_level_1": "Île-de-France",
    "admin_area_level_2": "Département de Paris",
    "country": "France",
    "postal_code": "75007",
    "formatted_address": "Av. Gustave Eiffel, 75007 Paris, France"
  },
  "custom_fields": { // custom fields are no longer flat root level fields
    "53c2f18db6a1655d6af8bba77d9679565f975fd8": "Text Custom Field",
    "d4de1c1518b4531717c676029a45911c340390a6": {
      "value": 2300,
      "currency": "EUR"
    }
  }
}
GET /api/v1/organizations/:id to GET /api/v2/organizations/:id
Please note that this section does not include the changes already covered in General API Changes section.

Returned organization object has changed, see Organization Object for details.

custom_fields parameter has been added to optionally return only a subset of custom fields. Multiple custom field keys can be provided by separating them with commas. This can be used to reduce the response size and time.
include_fields parameter has been added to optionally include some values that are not part of the default response. Multiple fields can be included by separating them with commas. Supported optional fields are next_activity_id, last_activity_id, open_deals_count, related_open_deals_count, closed_deals_count, related_closed_deals_count, participant_open_deals_count, participant_closed_deals_count, email_messages_count, activities_count, done_activities_count, undone_activities_count , files_count, notes_count, followers_count, won_deals_count, related_won_deals_count, lost_deals_count, related_lost_deals_count, last_incoming_mail_time, last_outgoing_mail_time, marketing_status, doi_status.
GET /api/v1/organizations to GET /api/v2/organizations
Note that GET /api/v2/persons also replaces GET /api/v1/organizations/:id/persons endpoint.

Please note that this section does not include the changes already covered in General API Changes section.

Returned organization object has changed, see Organization Object for details.

custom_fields parameter has been added to optionally return only a subset of custom fields. Multiple custom field keys can be provided by separating them with commas. This can be used to reduce the response size and time.
include_fields parameter has been added to optionally include some values that are not part of the default response. Multiple fields can be included by separating them with commas. Supported optional fields are next_activity_id, last_activity_id, open_deals_count, related_open_deals_count, closed_deals_count, related_closed_deals_count, participant_open_deals_count, participant_closed_deals_count, email_messages_count, activities_count, done_activities_count, undone_activities_count , files_count, notes_count, followers_count, won_deals_count, related_won_deals_count, lost_deals_count, related_lost_deals_count, last_incoming_mail_time, last_outgoing_mail_time, marketing_status, doi_status.
POST /api/v1/organizations to POST /api/v2/organizations
Please note that this section does not include the changes already covered in General API Changes section.

Only the name field is required. Everything else is optional and expected in the format described in Organization Object section.

It is no longer possible to create an already deleted entity with POST.
Only value subfield is required when setting an address. All other address subfields are optional and will default to null if not provided.
PUT /api/v1/organizations/:id to PATCH /api/v2/organizations/:id
Please note that this section does not include the changes already covered in General API Changes section.

Any fields changed are expected to be in the format described in Organization Object section.

It is no longer possible to use PATCH (former PUT) requests to delete an entity. Use corresponding DELETE endpoint instead.
Only value subfield is required when updating an address field. All other address subfields are optional and will default to null if not provided.
DELETE /api/v1/organizations to DELETE /api/v2/organizations
No changes other than version change in the URL.

Activities API
Activity Object
Changes Summary
Please note that this section does not include the changes already covered in General API Changes section.

is_active boolean field has been renamed to is_deleted and the old value negated. This is so all entities have a consistently named field for deleted status. When an entity has is_deleted set to true, the entity is considered soft deleted and will be fully deleted after 30 days of last activity.
The following fields are only included in the response when providing these field keys as comma separated string using the include_fields querystring parameter: attendees.
deal_title, lead_title, project_title, person_name, org_name, owner_name, type_name,person_dropbox_bcc, deal_dropbox_bcc fields have been removed. They can be fetched via relevant APIs using the relevant id fields.
busy_flag has been renamed to busy.
marked_as_done_time defaults to null instead of an empty string if the activity not marked as done.
delete_time field has been removed. If the person has is_deleted: true, update_time is the delete_time.
created_by_user_id field has been renamed to creator_user_id for consistency with other APIs.
assigned_to_user_id field has been removed. It always had the same value as user_id field (which has now been renamed to owner_id).
company_id, last_notification_time, last_notification_user_id, notification_language_id, calendar_sync_include_context , person_dropbox_bcc, deal_dropbox_bcc, type_name, reference_type, reference_id, conference_meeting_client, conference_meeting_url, conference_meeting_id, series, is_recurring, rec_rule, rec_rule_extension, rec_master_activity_id, original_start_time, source_timezone, update_user_id fields have been removed as they are for internal use only.
location is now formatted as an object like anaddress type custom field instead of being spread across multiple fields. See General API Changes for more info.
Old v1 Activity Object Example
JSON

{
  "id": 123,
  "subject": "Call",
  "user_id": 123, // Renamed to owner_id
  "done": false,
  "type": "call",
  "type_name": "Call", // Removed
  "lead": null, // Removed
  "conference_meeting_client": null,
  "conference_meeting_url": null,
  "conference_meeting_id": null,
  "company_id": 123, // Removed
  "reference_type": null, // Removed
  "reference_id": null, // Removed
  "last_notification_time": null, // Removed
  "last_notification_user_id": null, // Removed
  "notification_language_id": null, // Removed
  "calendar_sync_include_context": null, // Removed
  "series": null, // removed
  "is_recurring": null, // removed
  "rec_rule": null, // removed
  "rec_rule_extension": null, // removed
  "rec_master_activity_id": null, // removed
  "owner_name": "User Name", // Removed
  "person_dropbox_bcc": null, // Removed
  "deal_dropbox_bcc": null, // Removed
  "org_name": null,  // Removed
  "person_name": null, // Removed
  "deal_title": null, // Removed
  "lead_title": null, // Removed
  "project_title": null, // Removed
  "update_user_id": 123, // Removed
  "source_timezone": null, // Removed
  "original_start_time": null, // Removed
  "due_date": "1970-01-01",
  "due_time": "00:00",
  "duration": "01:20",
  "busy_flag": true, // Renamed to `busy`
  "add_time": "2024-11-05 10:56:51", // now in TZ format
  "update_time": "2024-11-26 11:32:36", // now in TZ format
  "marked_as_done_time": "",
  "public_description": "Public Description of the activity",
  "location": "Eiffel Tower, Avenue Gustave Eiffel, Paris, France", // Nested object now
  "location_subpremise": "",
  "location_street_number": "",
  "location_route": "Avenue Gustave Eiffel",
  "location_sublocality": "",
  "location_locality": "Paris",
  "location_admin_area_level_1": "Île-de-France",
  "location_admin_area_level_2": "Département de Paris",
  "location_country": "France",
  "location_postal_code": "75007",
  "location_formatted_location": "Av. Gustave Eiffel, 75007 Paris, France",
  "org_id": null,
  "person_id": null,
  "deal_id": null,
  "lead_id": null,
  "project_id": null,
  "private": false,
  "priority": 264,
  "note": "Activity's note",
  "created_by_user_id": 123, // Renamed to "creator_user_id"
  "assigned_to_user_id": 123, // Removed, always the same value as owner_id field (old user_id field)
  "attendees": [ // Included only when using `include_fields` parameter
    {
      "email_address": "some@attendee.com",
      "name": "Some Person",
      "status": "accepted",
      "is_organizer": 0,
      "person_id": null,
      "user_id": null
    }
  ],
  "participants": [
    {
      "person_id": 42,
      "primary_flag": true
    }
  ],
}
New v2 Activity Object Example
JSON

{
  "id": 123,
  "subject": "Call",
  "owner_id": 123, // Renamed from `user_id`
  "type": "call",
  "is_deleted": false, // Replacesd `active_flag`. NB: Negation of old value.
  "done": false,
  "conference_meeting_client": null,
  "conference_meeting_url": null,
  "conference_meeting_id": null,
  "due_date": "1970-01-01",
  "due_time": "00:00",
  "duration": "01:20",
  "busy": true, // Renamed from `busy_flag`
  "add_time": "2024-11-05T10:56:51Z", // now in TZ format
  "update_time": "2024-11-26T11:32:36Z", // now in TZ format
  "marked_as_done_time": null,
  "subject": "Call",
  "public_description": "Public Description of the activity",
  "location": { // Nested object now
    "value": "Eiffel Tower, Avenue Gustave Eiffel, Paris, France",
    "street_number": "",
    "route": "Avenue Gustave Eiffel",
    "sublocality": "",
    "locality": "Paris",
    "admin_area_level_1": "Île-de-France",
    "admin_area_level_2": "Département de Paris",
    "country": "France",
    "postal_code": "75007",
    "formatted_address": "Av. Gustave Eiffel, 75007 Paris, France"
  },
  "org_id": null,
  "person_id": null,
  "deal_id": null,
  "lead_id": null,
  "project_id": null,
  "private": false,
  "priority": 264,
  "note": "Activity's note",
  "creator_user_id": 123, // Renamed from  "created_by_user_id"
  "attendees": [ // Included only when using `include_fields` parameter
    {
      "email_address": "some@attendee.com",
      "name": "Some Person",
      "status": "accepted",
      "is_organizer": 0,
      "person_id": null,
      "user_id": null
    }
  ],
  "participants": [
    {
      "person_id": 42,
      "primary_flag": true
    }
  ],
}
GET /api/v1/activities/:id to GET /api/v2/activities/:id
Please note that this section does not include the changes already covered in General API Changes section.

Returned activity object has changed, see Activity Object for details.

include_fields parameter has been added to optionally include some values that are not part of the default response. Multiple fields can be included by separating them with commas. Supported optional fields are attendees.
GET /api/v1/activities to GET /api/v2/activities
Please note that this section does not include the changes already covered in General API Changes section.

Returned activity object has changed, see Activity Object for details.

include_fields parameter has been added to optionally include some values that are not part of the default response. Multiple fields can be included by separating them with commas. Supported optional fields are attendees.
POST /api/v1/activities to POST /api/v2/activities
Please note that this section does not include the changes already covered in General API Changes section.

Only the name field is required. Everything else is optional and expected in the format described in Person Object section.

It is no longer possible to create an already deleted entity with POST.
person_id field is now read-only. It is set indirectly by adding a primary participant. The simplest way to set it is to use "participants": \[ [ "person_id": 1, "primary": true ] ]\.
PUT /api/v1/activities/:id to PATCH /api/v2/activities/:id
Please note that this section does not include the changes already covered in General API Changes section.

Any fields changed are expected to be in the format described in Activity Object section.

It is no longer possible to use PATCH (former PUT) requests to delete an entity. Use corresponding DELETE endpoint instead.
person_id field is now read-only. It is set indirectly by adding a primary participant. The simplest way to set it is to use "participants": \[ [ "person_id": 1, "primary": true ] ]\.
DELETE /api/v1/activities to DELETE /api/v2/activities
No changes other than version change in the URL.

Deal Followers, Person Followers, Organization Followers, Product Followers, User Followers API
Follower Object
Changes Summary
Please note that this section does not include the changes already covered in General API Changes section.

Follower object now only contains the add_time of the following relation and the user_id representing the user following the entity.
id field was removed from all Follower objects as it is for internal use only.
deal_id field was removed from Deal Follower object
person_id field was removed from Person Follower object
org_id was removed from Organization Follower object
product_id was removed from Product Follower object
User Followers now return a standardized Follower object instead of followed user ids only.
Old v1 Follower Object Example
JSON

{
  "id": 123, // Removed
  "user_id": 456,
  "add_time": "2025-01-01 10:56:51", // now in TZ format
  "deal_id": 123, // Removed, was only present for deal followers
  "person_id": 123, // Removed, was only present for person followers
  "org_id": 123, // Removed, was only present for organization followers
  "product_id": 123 // Removed, was only present for product followers
}
New v2 Follower Object Example
JSON

{
  "user_id": 456,
  "add_time": "2025-01-01T10:56:51Z", // now in TZ format
}
GET /api/v1/deals/:id/followers to GET /api/v2/deals/:id/followers
GET /api/v1/persons/:id/followers to GET /api/v2/persons/:id/followers
GET /api/v1/organizations/:id/followers to GET /api/v2/organizations/:id/followers
GET /api/v1/products/:id/followers to GET /api/v2/products/:id/followers
GET /api/v1/users/:id/followers to GET /api/v2/users/:id/followers
Please note that this section does not include the changes already covered in General API Changes section.

Returned follower object has changed, see Follower Object for details.

POST /api/v1/deals/:id/followers to POST /api/v2/deals/:id/followers
POST /api/v1/persons/:id/followers to POST /api/v2/persons/:id/followers
POST /api/v1/organizations/:id/followers to POST /api/v2/organizations/:id/followers
POST /api/v1/products/:id/followers to POST /api/v2/products/:id/followers
Please note that this section does not include the changes already covered in General API Changes section.

Returned follower object has changed, see Follower Object for details.

Trying to add a user as a follower who is already a follower will return 400 Bad Request now. Previously it succeeded with 200 Success.
DELETE /api/v1/deals/:id/followers/:id to DELETE /api/v2/deals/:id/followers/:id
DELETE /api/v1/persons/:id/followers/:id to DELETE /api/v2/persons/:id/followers/:id
DELETE /api/v1/organizations/:id/followers/:id to DELETE /api/v2/organizations/:id/followers/:id
DELETE /api/v1/products/:id/followers/:id to DELETE /api/v2/products/:id/followers/:id
Please note that this section does not include the changes already covered in General API Changes section.

Returned follower object has changed, see Follower Object for details.

The follower ID in the request is no longer the arbitrary id of the old Follower object, but the user id of the following user who should be removed as a follower.
