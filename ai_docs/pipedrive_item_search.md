ItemSearch

Run in Postman
Ordered reference objects, pointing to either deals, persons, organizations, leads, products, files or mail attachments.

Perform a search from multiple item types
Copy link
Performs a search from your choice of item types and fields.




API v2
Cost
20

Request
GET/api/v2/itemSearch
Query parameters
term
string
required
The search term to look for. Minimum 2 characters (or 1 if using exact_match). Please note that the search term has to be URL encoded.

item_types
string
A comma-separated string array. The type of items to perform the search from. Defaults to all.

Values

deal

person

organization

product

lead

file

mail_attachment

project

fields
string
A comma-separated string array. The fields to perform the search from. Defaults to all. Relevant for each item type are:

Item type	Field
Deal	custom_fields, notes, title
Person	custom_fields, email, name, notes, phone
Organization	address, custom_fields, name, notes
Product	code, custom_fields, name
Lead	custom_fields, notes, email, organization_name, person_name, phone, title
File	name
Mail attachment	name
Project	custom_fields, notes, title, description

Only the following custom field types are searchable: address, varchar, text, varchar_auto, double, monetary and phone. Read more about searching by custom fields here.
When searching for leads, the email, organization_name, person_name, and phone fields will return results only for leads not linked to contacts. For searching leads by person or organization values, please use search_for_related_items.
Values

address

code

custom_fields

email

name

notes

organization_name

person_name

phone

title

description

search_for_related_items
boolean
When enabled, the response will include up to 100 newest related leads and 100 newest related deals for each found person and organization and up to 100 newest related persons for each found organization

exact_match
boolean
When enabled, only full exact matches against the given term are returned. It is not case sensitive.

include_fields
string
A comma-separated string array. Supports including optional fields in the results which are not provided by default.

Values

deal.cc_email

person.picture

product.price

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
"result_score":1.22724
"id":42
"type":"deal"
"title":"Sample Deal"
"value":53883
"currency":"USD"
"status":"open"
"visible_to":3
"id":69
"id":3
"name":"Demo Scheduled"
"id":6
"name":"Sample Person"
"id":9
"name":"Sample Organization"
"address":"Dabas, Hungary"
"Sample text"
"Sample note"
"result_score":0.31335002
"id":9
"type":"organization"
"name":"Sample Organization"
"address":"Dabas, Hungary"
"visible_to":3
"id":69
"custom_fields":
"notes":
"result_score":0.29955
"id":6
"type":"person"
"name":"Sample Person"
"555123123"
"+372 (55) 123468"
"0231632772"
"primary@email.com"
"secondary@email.com"
"visible_to":1
"id":69
"id":9
"name":"Sample Organization"
"address":"Dabas, Hungary"
"Custom Field Text"
"Person note"
"result_score":0.0093
"id":4
"type":"mail_attachment"
"name":"Sample mail attachment.txt"
"url":"/files/4/download"
"result_score":0.0093
"id":3
"type":"file"
"name":"Sample file attachment.txt"
"url":"/files/3/download"
"id":42
"title":"Sample Deal"
"id":6
"name":"Sample Person"
"id":9
"name":"Sample Organization"
"address":"Dabas, Hungary"
"result_score":0.0011999999
"id":1
"type":"product"
"name":"Sample Product"
"code":"product-code"
"visible_to":3
"id":69
"custom_fields":
"result_score":0
"id":2
"type":"deal"
"title":"Other deal"
"value":100
"currency":"USD"
"status":"open"
"visible_to":3
"id":1
"id":1
"name":"Lead In"
"id":1
"name":"Sample Person"
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
Perform a search using a specific field from an item type
Copy link
Performs a search from the values of a specific field. Results can either be the distinct values of the field (useful for searching autocomplete field values), or the IDs of actual items (deals, leads, persons, organizations or products).

View quick guide: /v1 to /v2 migration

API v1
API v2
Cost
20

Request
GET/api/v2/itemSearch/field
Query parameters
term
string
required
The search term to look for. Minimum 2 characters (or 1 if match is exact). Please note that the search term has to be URL encoded.

entity_type
string
required
The type of the field to perform the search from

Values

deal

lead

person

organization

product

project

match
string
The type of match used against the term. The search is case sensitive.

E.g. in case of searching for a value monkey,

with exact match, you will only find it if term is monkey
with beginning match, you will only find it if the term matches the beginning or the whole string, e.g. monk and monkey
with middle match, you will find the it if the term matches any substring of the value, e.g. onk and ke
.
Defaultexact
Values

exact

beginning

middle

field
string
required
The key of the field to search from. The field key can be obtained by fetching the list of the fields using any of the fields' API GET methods (dealFields, personFields, etc.). Only the following custom field types are searchable: address, varchar, text, varchar_auto, double, monetary and phone. Read more about searching by custom fields here.

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
"name":"Jane Doe"
"id":2
"name":"John Doe"
"next_cursor":"eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"