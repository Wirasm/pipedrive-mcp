About the Pipedrive API
Suggest Edits
📘
An application programming interface (API) is a set of functionalities that a service owner provides so people can use its features and/or build software applications. An API details how a user makes requests and the responses they receive in return.

Pipedrive is a sales CRM with an intuitive RESTful API, webhooks, app extensions and API clients to help you build an app for the Pipedrive Marketplace.

Pipedrive RESTful API
Our Pipedrive RESTful API Reference can be accessed via https://developers.pipedrive.com/docs/api/v1/, where you will find a list of endpoints and their descriptions.

Calls to our API are validated against an API token or an access_token when using OAuth 2.0. Our API supports UTF-8 for character encoding. Learn how to find and use the api_token here.

3687
Pipedrive Entity Relationship Diagram (ERD)

Webhooks
Webhooks enable you to obtain real-time, programmatic notifications from Pipedrive regarding changes to your data as they happen. Instead of pulling information via our API, webhooks will push information to your endpoint.

You can create webhooks via the web app and our API. You can create a webhook programmatically by making a POST request to the webhook’s endpoint. Pipedrive will then send a notification when an event is triggered (e.g., a new lead is added) as an HTTP post with a JSON body to the endpoint(s) you have specified. Find out more about webhooks here.

App extensions
App extensions enable apps built for the Pipedrive Marketplace to give additional value to their users. With app extensions, the app’s functionality will be available directly inside the Pipedrive platform’s UI and users will be able to interact with and see the custom functionality of your app.

This also helps to increase your app's visibility and brand awareness, as the app icon will be displayed inside Pipedrive after a user has installed it. Find out more about app extensions here.

API clients
Pipedrive API clients are available on GitHub. Some of the most popular repositories include:

Client-nodejs (official)
Client-php (official)
Pipedrive (community built)
Python-pipedrive (community built)
Pipedrive-dotnet (community built)
Pipedrive.rb (community built)

How Pipedrive API works
📘
Do take note that entity/entities may be called “item/items” or “type of item/items” for the end user in the Pipedrive web and mobile app.

At the base of your Pipedrive account is a customer relationship management (CRM) database of your sales pipeline, processes and relationships. As organizing sales data is essential for sales activities, Pipedrive helps to organize and link your data together for better visibility through the core and adjacent entities.

Core entities
Within the Pipedrive API, we have core entities that consist of multiple endpoints. These core entities represent a larger area inside Pipedrive and can be found in the left-hand side menu in the Pipedrive web app. Tied to them are adjacent entities that contain supplementary information relevant to the core entities.

2041
Pipedrive core entities ERD

The ERD above shows how core entities are connected within Pipedrive.

As leads can be converted to deals, they are sometimes used in place of each other. For example, in the case of activities, an activity can be associated with either a lead or a deal. This goes the same for products.
Persons and organizations are considered contacts and are often grouped together.
Mailbox, found in the Mail tab of the Pipedrive web app, is the email control hub inside Pipedrive that stores all the emails a user decides to keep a record of. Mail is tracked and associated with persons and deals through Pipedrive’s email sync and Smart Bcc features.

[Entity] Fields endpoints allow you to obtain the near-complete schema of the respective core entities. You can add, update and delete main and custom fields through these adjacent entities.

Read on to discover how leads, deals, persons and organizations (contacts), activities, products and users are further connected to other core and adjacent entities.


Leads
1847
Leads ERD

Leads are prequalified, potential deals that are kept in a separate inbox called the Leads Inbox. Leads can subsequently be converted to deals via the Pipedrive web app and added to a pipeline.

Leads can have activities, emails (mailbox) and notes attached to them. They can also have multiple LeadLabels to categorize them and be linked with one LeadSource to indicate where the lead came from.

Key aspects of leads:

Leads must always have one person (contacts) or organization (contacts) linked with them
Leads can only have one source (LeadSource). Leads created through the API have a set source “API”.
Leads can only have the same custom fields (DealFields) as deals
Leads can only be converted to deals via the Pipedrive web app

Deals
2443
Deals ERD

Deals are ongoing transactions pursued with a person or an organization. It’s tracked and processed through the Stages of a pipeline until it’s won or lost. Deals can be converted from leads via the Pipedrive web app.

In Pipedrive, deals contain all actions taken towards closing a sale, for example, activities, emails (mailbox), notes and files, and have their own custom fields (DealFields). Products and subscriptions can also be attached to deals.

A deal can be linked with either a person or organization (contacts) but it must always have one contact linked with them. As a deal is associated with a contact, it will pull all information from the linked contact and, likewise, associate all actions performed on the deal with the linked contact.


Persons & organizations (contacts)
2073
Persons & organizations (contacts) ERD

Persons (or people) are the specific customers of the sales process, while organizations are the companies that the persons work at. Persons and organizations are considered contacts and they rest in one centralized hub in the Pipedrive web app. The ERD above depicts how different core and adjacent entities can either relate to contacts as a whole or persons/organizations specifically.

Both persons and organizations can have activities, notes and files attached to them and their respective main fields and custom fields (PersonFields and OrganizationFields). Emails (Mailbox) and products can only be linked to persons while OrganizationRelationships can only be linked to organizations.

Key aspects of Persons and organizations (contacts):

A person can only be linked to one organization
A lead or a deal must always have a person or an organization linked to it
Both persons and organizations can have multiple deals open for them at the same time

Activities
2043
Activities ERD

Activities are any actions a user does towards the closing of a sale. There are different types of activities (ActivityTypes) that can be performed, e.g. a phone call (CallLogs), a meeting or a task. You can have custom activity types and custom fields (ActivityFields) for activities. Users can schedule activities in relation to a person, an organization or a lead/deal.

Key aspects of activities:

Associating an activity with a deal will also associate the activity with the person and/or organization linked to the deal
Currently, Files can only be added to activities via the API
CallLogs
CallLogs for calls made via the Pipedrive mobile app are also considered activities, which means they can be associated with a deal, a person and/or an organization. Do note that CallLogs differ from other activities as they only receive the information needed to describe the phone call.


Projects

Projects represents projects and task management entities to assist sales processes from an after-sales activities perspective. Each project has an owner and must be placed in a phase. Projects can be attached to an organization, person or deal. Projects can also be connected with Tasks and ProjectTemplates.

Products
1401
Products ERD

Products are goods and/or services that your company deals with. Products can have their own custom fields (ProductFields) and be attached to deals. Persons (contacts) can be added as participants and users can be added as followers for a product. Files can also be added to products.


Users
1598
Users ERD

A Company within pipedrive comprises Users who may be grouped into teams. The ERD above depicts how different core and adjacent entities can relate to a company as a whole or users/teams specifically.

Goals may be related to a company, a team and/or a user. Users and teams can have their own specific PermissionSets and Roles, which are a part of the visibility groups’ feature. Users can also have their own UserSettings and UserConnections.

2 main types of webhooks can be created: webhooks related to a company and webhooks for apps. When querying webhooks, a user can obtain the webhooks they’ve created, while apps can only see and delete webhooks that have the type set as type= 'application'.


REQUESTS

Requests
Suggest Edits
📘
All requests to the Pipedrive API must be made over SSL (https, not http).

We recommend using JSON body format when performing API requests. To do a proper JSON-formatted request, ensure you provide Content-Type: application/json in HTTP request headers. Our API supports UTF-8 for character encoding.

For the POST method, regular form-encoded body format is also supported but you may experience quirks related to a lack of data types. Our API uses the HTTP verbs for each action:

Method	Description
GET	Used for retrieving resources
POST	Used for creating resources
PUT	Used for replacing resources or collections
PATCH	Used for updating some parts of a resource
DELETE	Used for deleting resources

URL naming
Our API uses a straightforward URL naming convention.

Each request must be made to the API endpoint https://{COMPANYDOMAIN}.pipedrive.com/api/v1, followed by the type of object in a plural form, for example, https://{COMPANYDOMAIN}.pipedrive.com/api/v1/deals
When one item is being asked, and such a method exists, the ID of the item must be appended to the URL, for example https://{COMPANYDOMAIN}.pipedrive.com/api/v1/deals/2
When asking for sub-objects of an object, append that to the ID of the master object, for example, https://{COMPANYDOMAIN}.pipedrive.com/api/v1/deals/2/activities
We advise everyone to use {COMPANYDOMAIN}.pipedrive.com for faster requests as it helps us to better determine which data center your request should go to.


Field selector
When asking for a collection/list of objects, you can pass in a field selector to indicate which fields you would like to fetch per each object. Most endpoints in our API reference support this, but not all.

The field selector is supported in requests done with OAuth and requests done with the api_token. For example, you may only want to fetch a deal's ID, title, value, and currency when asking the deals list – this can be done by using the following syntax:

URL

GET https://{COMPANYDOMAIN}.pipedrive.com/api/v1/deals:(id,title,value,currency)
You can also see the field selector being used in our updating custom fields' values tutorial.



RESPONSES

Responses
Suggest Edits
All data is sent and received as JSON.

Each response sent from the API contains a success parameter, which is of boolean type, indicating whether the request was successful. Upon success being false, an optional error parameter (string) may be given. In case of success is true, the response is always contained within a data parameter, and additional metadata may be carried inside an additional_data parameter.

Success response
All success responses follow the same schema:

JSON

{
    success: true, //boolean, shows if operation succeeded (similar to HTTP status)
    data: null, //object in other cases
    additional_data: {
        pagination: { //for endpoints that list data
            start: 0,
            limit: 100,
            more_items_in_collection: false
        }
    }
}
Error response
All error responses follow the same schema:

JSON

{
    success: false,
    error: "Requested service is not available", //main error message
    error_info: "Please check developers.pipedrive.com",
    data: null,
    additional_data: null
}
Error response in the scenario when a customer's account hits a limit for either Deal, custom field, Role or Team creation with the HTTP error code 403:

JSON

{
    "success": false,
    "error": "Couldn't add the deal. Open deals limit reached.",
    "error_info": "Please check developers.pipedrive.com for more information about Pipedrive API.",
    "data": null,
    "additional_data": null,
    "code": "feature_capping_deals_limit"
}


Rate limiting
Suggest Edits
📘
To maintain high performance standards and ensure fair resource access across all users, token-based rate limits will be introduced for API usage. This change will affect new and existing customers according to the following schedule:

New Customers: Starting on December 2nd, 2024, all new signups will operate under the token-based rate limiting system from the outset.
Existing Customers: For current accounts, rate limits will be gradually rolled out beginning March 1st, 2025, with the process scheduled to complete by May 31st, 2025. This phased rollout is designed to provide time for any necessary adjustments.
Rate limiting is a system used to control the number of requests an application can make to an API within a specific timeframe. It ensures fair resource usage across all users and protects the platform from being overwhelmed by high-volume requests. By setting usage limits, rate limiting helps maintain stable performance, reduce server load, and prevent any single application from monopolizing resources at the expense of others.

Token-Based Rate Limiting
With token-based rate limiting, each request consumes a certain number of tokens from a set daily allowance, or “budget.” Once this budget is exhausted, further requests will be temporarily blocked until the budget resets at the start of the next day.

Unlike traditional request-based rate limiting, which restricts the sheer number of requests regardless of their complexity, token-based rate limiting offers a more flexible and efficient approach. This method allows lightweight requests to consume fewer tokens, while more resource-intensive API calls are assigned a higher token cost. By adapting the “charge” based on the complexity of each request, token-based rate limiting provides greater freedom to execute frequent, low-impact operations without hitting limits prematurely, while still protecting the platform from heavy resource usage.

📘
You can view the token costs for each API endpoint in our API Reference.

Token-based rate limiting is widely used across the industry as a fair and scalable approach to managing API usage. It ensures that both lightweight and complex API interactions are accommodated efficiently, balancing performance and access.

Tokens Daily Budget
Each company account is allocated a daily API token budget, which is shared among all users within that account. This budget is exclusively for API traffic authenticated by API tokens or OAuth tokens, and it does not impact actions performed directly within the Pipedrive user interface.

The daily token budget is calculated using the following formula:

30,000 base tokens × subscription plan multiplier × number of seats

Plan	Plan multiplier
Essential	1
Advanced	2
Professional	3
Power	5
Enterprise	7
📘
Tokens budget resets at midnight at server’s timezone which may not be aligned with timezone of customer location.

API Requests
Each API request consumes a specific number of tokens, with each API endpoint assigned cost in tokens based on the complexity and resource demand of the endpoint. When a request is made, the corresponding token cost is deducted from the company’s daily API budget. Lightweight endpoints consume fewer tokens, while more complex or data-intensive endpoints require a higher token cost.

📘
You can view the token costs for each API endpoint in our API Reference.

Costs for some of the API operations are listed below:

API Endpoint type	Cost in tokens
Get single entity	2
Get list of entities	20
Update single entity	10
Delete single entity	6
Delete list of entities	10
Search for entities	40
📘
Available API v2 endpoints are performance-optimized, resulting in lower token costs compared to the original v1 endpoints. Learn more here.

Exceeding the tokens budget
When the daily API token budget is close to being fully consumed, automated notifications will be sent to the company administrators to provide visibility and allow for any necessary adjustments.

📘
75% Notification: When usage reaches 75% of the daily budget, an automated email will be sent to the company administrators. This notification is intended as an early warning, giving time to review API usage or adjust integrations if needed.
100% Notification: Upon reaching 100% of the daily token budget, a second email notification will be sent to inform the administrator that the budget has been exhausted.
Once the daily budget is fully depleted, all further API requests will be rejected with a 429 (Too Many Requests) status code. These requests will remain blocked until the budget resets the following day, at the designated reset time based on the server’s timezone

📘
Tokens budget resets at midnight at server’s timezone which may not be aligned with timezone of customer location.

To avoid interruptions, administrators may wish to monitor API usage closely and consider adjusting their usage patterns or increasing their budget allocation by upgrading to a higher plan or adding more seats. The company’s API usage statistics can be found in the API Usage Dashboard within Company Settings.

Burst limits
In addition to the daily token-based rate limits, burst rate limits are in place to prevent a large number of tokens from being consumed in a short period. These burst limits are designed to protect against rapid, high-volume API calls that could deplete the entire daily budget too quickly, potentially locking a company out from API access until the next daily reset.

How do Burst Limits Work?
Burst rate limits apply at the individual user level within each company account, operating on a rolling 2-second window. This means that each user has a maximum allowable number of requests within any 2-second timeframe, based on the company’s subscription plan. These limits prevent sudden spikes in usage, helping to maintain consistent access to the API throughout the day.

Limits
📘
Burst rate limiting of the Pipedrive API is considered per token, not per company.

Plan	API token limits	OAuth apps limits
Essential	20 requests per 2 seconds	80 requests per 2 seconds
Advanced	40 requests per 2 seconds	160 requests per 2 seconds
Professional	80 requests per 2 seconds	320 requests per 2 seconds
Power	100 requests per 2 seconds	400 requests per 2 seconds
Enterprise	120 requests per 2 seconds	480 requests per 2 seconds
The Search API has unique burst limits that are consistent across all authentication types and subscription plans:

Plan	API limit
Essential	10 requests per 2 seconds
Advanced	10 requests per 2 seconds
Professional	10 requests per 2 seconds
Power	10 requests per 2 seconds
Enterprise	10 requests per 2 seconds
HTTP headers and response codes
Pipedrive burst limits have the following response headers:

Header	Description
x-ratelimit-limit	The maximum number of requests current access_token or api_token can perform per 2-second window.
x-ratelimit-remaining	The number of requests left for the 2-second window.
x-ratelimit-reset	The remaining window before the rate limit resets.
x-daily-requests-left	Indicates how many requests you can still make to POST/PUT endpoints during the ongoing day (calculated in UTC). Applicable only to api_token requests.
Limiting high volume traffic
🚧
Only the high volume traffic coming from api_token integrations will be blocked.

In order to protect ourselves from online attacks caused by misconfigured API integrations, users abusing our system by not respecting our rate limits and keeping up the high volume of traffic despite getting the 429 response code, will also get the 403 response code. When getting the 403 response code, the answer will be an HTML error page with the message "This error is produced by Cloudflare. See troubleshooting guide here.", informing the user that one’s access has been denied:



Please note that this improvement will not impact the vast majority of users, even if our API is heavily used. If this impacts you, please review your integration and remove any misconfiguration that might lead you to be blocked.

How to avoid being rate limited
If you're reaching the rate limit, options to improve performance include restructuring the integration architecture, using Webhooks, and/or upgrading to a higher plan. Learn more about optimizing API usage here.



Date format
Suggest Edits
All dates and times received by the API will be in ISO 8601 format 2019-01-22 08:55:59 (would be the same as 2019-01-22T08:55:59).

🚧
All times received by the API will be in UTC timezone.

The times that are sent to the API should also be converted to the UTC timezone before being sent.

Updated about 2 months ago

Pagination
Suggest Edits
Pipedrive offers pagination for most of our API’s list and item collection endpoints.

Cursor pagination
As the name suggests, cursor-based pagination uses cursors to page through the endpoint’s results. Performance-wise, it is the most efficient and stable pagination method for traversing through large amounts of entities. Inside the Pipedrive API, we support cursor-based pagination for the following endpoints:

All v2 API list endpoints
GET /v1/activities/collection
GET /v1/deals/collection
GET /v1/organizations/collection
GET /v1/persons/collection
GET /v1/deals/{id}/participantsChangelog
GET /v1/deals/{id}/changelog
GET /v1/persons/{id}/changelog
GET /v1/organizations/{id}/changelog
GET /v1/projects endpoints with pagination
GET /v1/projectTemplates
GET /v1/tasks
Cursor-based endpoints accept the cursor and limit query parameters. A cursor is a marker indicating the next page’s first item. By specifying the limit, you can control the number of entities returned per page. The maximum limit value is 500.

cursor (string)	A marker (an opaque string value) representing the first item on the next page
limit (integer)	For pagination, the limit of entries to be returned. If not provided, 100 items will be returned.
Example request for the GET /v1/activities/collection endpoint:

JSON

GET https://{COMPANYDOMAIN}.pipedrive.com/api/v1/activities/collection?cursor=eyJhY3Rpdml0eSI6NDJ9&limit=100
Within the response’s additional_data object, the next_cursor field will be returned, indicating the first item on the next page. The value of the next_cursor field will be null if you have reached the end of the dataset and there are no more pages to be returned.

Example response:

JSON

{
    "success": true,
    "data": [
        {
           … // returned activities’ data
        }
    ],
    "additional_data": {
        "next_cursor": "eyJhY3Rpdml0aWVzIjoyN30"
    }
}

Offset pagination
With the rest of our GET endpoints, we offer offset-based pagination. The parameters that control this type of pagination are start and limit, indicating the desired offset and the number of items to be returned per page.

start (integer)	Pagination start.
If omitted, the default value is 0.
limit (integer)	The number of items shown per page. If not provided, 100 items will be returned.
Example request for the GET /v1/activities endpoint:

JSON

GET https://{COMPANYDOMAIN}.pipedrive.com/api/v1/activities?start=0&limit=100
Within the response’s additional_data object, a pagination object will be returned. The additional_data.pagination object will contain the given start and limit values, as well as the more_items_in_collection flag, indicating whether more items can be fetched after the current batch.

If more items can be fetched, the next_start field, which can be used for specifying the next offset pointer, will also be returned.

The maximum limit value is 500.

Example response:

JSON

{
    "success": true,
    "data": [
        {
           … // returned activities’ data
        }
    ],
    "additional_data": {
        "pagination": {
            "start": 0,
            "limit": 10,
            "more_items_in_collection": true,
            "next_start": 10
        }
    }
}
Updated about 2 months ago

HTTP status codes
Suggest Edits
Here's a list of the status codes used in Pipedrive:

Status Code	Name	Description
200	OK	Request fulfilled
201	Created	New resource created
400	Bad Request	Request not understood
401	Unauthorized	Invalid API token
402	Payment Required	Company account is not open (possible reason: trial expired, payment details not entered)
403	Forbidden	Request not allowed.
User account has reached a limit for an entity.
404	Not Found	Resource unavailable
405	Method not allowed	Incorrect request method
410	Gone	Old resource permanently unavailable
415	Unsupported Media Type	Feature is not enabled
422	Unprocessable Entity	Webhooks limit reached
429	Too Many Requests	Rate limit has been exceeded
500	Internal Server Error	Generic server error
501	Not Implemented	Non-existent functionality
503	Service Unavailable	Scheduled maintenance


Custom fields
Suggest Edits
Custom fields allow you to add additional data to your Pipedrive account that isn't included by default. Each deal, organization, person, and product item can contain custom fields. We have 16 different field types available, each with its own uses.


Creating a custom field
See our creating a new custom field tutorial to add a custom field programmatically.

Method	URL	Useful for
POST	/dealFields	Adding a new deal field.
NB! Leads inherit all deals’ custom fields.
POST	/organizationFields	Adding a new organization field
POST	/personFields	Adding a new person field
POST	/productFields	Adding a new product field
📘
Note that custom fields cannot be duplicated to multiple different Pipedrive accounts. You can add the custom fields with the same name and field type to different accounts but they'll have different values for key parameters referenced in our API.


Naming a custom field
All custom fields are referenced as randomly generated 40-character hashes in the dataset, for example, dcf558aac1ae4e8c4f849ba5e668430d8df9be12 - it may look like our office cat walked across the laptop, but this actually is a key for a custom field in our API dataset.

🚧
These 40-character custom fields (for example, dcf558aac1ae4e8c4f849ba5e668430d8df9be12) are not shown in our API Reference as they differ for each Pipedrive account, but they can be seen in the API requests and responses as well as used in the requests when adding new items or updating existing ones.

You can’t rename the reference of the custom field (the field API key), but you can rename the name of a custom field that’s visible to the User.

Inside Pipedrive, you can find the API key of a field by going to Settings > Data fields and choosing the entity (deal/person/organization/product). When you hover over the row of a custom field, a three-dot menu appears on the right-hand side. From there, choose Copy API key.

Finding the API key of a custom field
Finding the API key of a custom field


Referencing a custom field
Here’s how you use an example key for a custom field in an example POST request to /deals (make sure you replace the example key with yours before making the request):

PHP

<?php
$api_token = 'Your API token goes here';
 
$deal = array (
    'title' => 'New deal with a custom field',
    'value' => '500',
    'currency' => 'USD',
    'dcf558aac1ae4e8c4f849ba5e668430d8df9be12' => 'A new field value for an existing example custom field key'
);
 
$url = 'https://companydomain.pipedrive.com/api/v1/deals';
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $deal);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['x-api-token: ' . $api_token]);

$output = curl_exec($ch);
curl_close($ch);
 
$result = json_decode($output, true); // Check if an ID came back, if did print it out
 
if (!empty($result['data']['id'])) { echo 'Deal was added successfully!' . PHP_EOL; }
Each custom field type corresponds to a specific data format. To determine in which format you need to submit data into a custom field, make a GET request for the same kind of object and check the format of the value of that field. You can find the list of field_type in the table below.


Updating a custom field
See our updating custom fields’ values tutorial to update a custom field programmatically.

Method	URL	Useful for
PUT	/dealFields/{id}	Updating a Deal field.
NB! Leads inherit all deal's custom fields.
PUT	/organizationFields/{id}	Updating an organization field
PUT	/personFields/{id}	Updating a person field
PUT	/productFields/{id}	Updating a product field

Deleting a custom field
🚧
We don't recommend deleting a custom field, because it might permanently remove all data. In case you do delete by mistake, there's a chance that you can get it back by contacting our awesome support people.

See our deleting a custom field tutorial to delete a custom field programmatically.

Method	URL	Useful for
DELETE	/dealFields/{id}	Marking a deal field as deleted.
NB! Leads inherit all deals' custom fields.
DELETE	/organizationFields/{id}	Marking an organization field as deleted
DELETE	/personFields/{id}	Marking a person field as deleted
DELETE	/productFields/{id}	Marking a product field as deleted
After a custom field is deleted, it will no longer appear in API responses. All POST requests mentioning a custom field will ignore it.


Types of custom fields
See below the 16 different types of custom fields available:

Type	field_type	Description	Useful for	Additional info
Text	varchar	The text field is used to store texts up to 255 characters	Billing addresses, (short) comments, email addresses	
Autocomplete	varchar_auto	The text field is used to store texts up to 255 characters and can autocomplete from the text previously inserted into this field	Custom options (e.g., tagging), email addresses	
Large text	text	The large text field is used to store texts longer than usual	Comments, descriptions	
Numerical	double	The numeric field is used to store data such as the amount of commission or other custom numerical data	Commission, priority level	The value should be numeric with a maximum precision (decimal places) of 16.

If a number exceeds the maximum precision, it will stay without the full precision.
Monetary	monetary	The monetary field is used to store data such as the amount of commission	Commission, amounts	The currency of the field will match the user’s default currency setting unless specified otherwise in the request.

The format of the field is determined by the user’s locale.
Multiple options	set	The multiple options field lets you predefine a list of values to choose from.

Multiple option fields can have a max of 10,000 options per field.	Industry type, competitors, region	
Single option	enum	The single option field lets you predefine a list of values out of which one can be selected.

Single option fields can have a max of 10,000 options per field.	Lead type, category, industry	
User	user	The user field can contain one user amongst users of your Pipedrive account*	Tech contacts, previous deal owners	
Organization	org	The organization field can contain one organization out of all the organizations stored on your Pipedrive account*	Related parties, partner organizations	
Person	people	The person field can contain one person out of all the people stored on your Pipedrive account*	Related parties, tech contacts	
Phone	phone	A phone number field can contain a phone number (naturally) or a Skype Name with a click-to-call functionality	Skype names, phone numbers	No auto-formatting unless enabled from the User Interface (supports only the US phone format)
Time	time	The time field is used to store times, picked from a handy inline time picker	Delivery times, lunchtime	
Time range	timerange	The time range field is used to store time ranges picked from a handy inline time picker	Office hours, the best time to contact	
Date	date	Date field is used to store dates picked from a handy inline calendar	Delivery dates, deadlines	The format of the field is determined by the user’s locale
Date range	daterange	The date range field is used to store date ranges picked from a handy inline calendar	Event dates, completion estimates	
Address	address	Address field is used to store addresses	Event places, office locations (when separate from business address)	The address field can hold all parts of address components – including City, tate, Zip Code, and Country – so there’s no need to create separate address fields for each address component.

You can use Google Maps autocomplete textfield to enter addresses and visualize them on a map. You’ll also be able to filter items based on specific address criteria.
* Doesn’t link the item with the user, person, or organization for statistics or any other form of ownership or relation, but can be used for filtering.


How to find out if a field is a custom field
The edit_flag parameter in the response body of an entity’s fields can be used to identify if the field is a custom field:

true – a custom field
false – Pipedrive default field
JSON

{
  id: 12499,
  key: '123456789',
  name: 'Date',
  order_nr: 47,
  field_type: 'date',
  json_column_flag: true,
  add_time: '2023-03-02 02:14:54',
  update_time: '2023-03-02 02:14:54',
  last_updated_by_user_id: 13053568,
  edit_flag: true,
  details_visible_flag: true,
  add_visible_flag: false,
  important_flag: true,
  bulk_edit_allowed: true,
  filtering_allowed: true,
  sortable_flag: true,
  mandatory_flag: false,
  active_flag: true,
  projects_detail_visible_flag: false,
  index_visible_flag: true,
  searchable_flag: false
},

Custom fields created by Contact Sync
When a user first sets up Contact Sync, five new custom fields (Instant messenger, Postal address, Notes, Birthday, Job title) are created for the entire company. These fields are similar to the default Pipedrive fields as they have a field API key that follows the syntax of all default Pipedrive API keys (field name, with an underscore replacing each space), unlike user-generated custom fields.

Here are the five custom fields created by Contact Sync:

Field name	Type	Show in Add new dialog	Show in detail view	Field API key	Additional info
Instant messenger	Varchar	by default: No	by default: No	im	Although this is a text field, it accepts an array of objects. (See example below)
Postal address	Address	by default: No	by default: No	postal_address	
Notes	Large Text	by default: No	by default: No	notes	
Birthday	Date	by default: No	by default: No	birthday	
Job title	Text	by default: No	by default: No	job_title	
You can also see these fields in the Pipedrive web app by going to Settings > (Company) > Data fields > Person. It’s not possible to add any other fields to Contact Sync.

Contact Sync and custom fields duplication
Contact Sync directly affects these five fields, as the data for these fields is updated every time the Contact Sync source is updated. As such, when using these fields, please note that they may be duplicated by users who create custom fields with the same name. This can cause issues where the field names match, but the API keys do not because one has a Pipedrive API key and the other has a 40-character hashed API key. Therefore, a user may have two fields with different information in them.

Instant messenger field and labels
The instant messenger field (field key im) is a text field that accepts an array of objects. Do note that multiple labels are available for the different instant messengers, for example, Google, AIM, Yahoo, Skype, etc.

Here is an example of what an array for this field could look like:

JSON

[
  {
    "label": "google",
    "value": "person1@companyname.com",
    "primary": true
  },
  {
    "label": "aim",
    "value": "person1@companyname.com",
    "primary": false
  }
]