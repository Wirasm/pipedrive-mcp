# Pipedrive API Edge Cases

This document outlines known edge cases and quirks in the Pipedrive API that require special handling in our implementation.

## General API Behavior

### Pagination

- When using cursor-based pagination, always handle the case where the `next_cursor` is `null`, indicating the end of results
- Maximum limit for pagination is 500 items per request
- Always use the v2 API endpoints which use cursor-based pagination when possible

### Error Handling

- Success flag in responses: Always check the `success` flag in responses, even for 200 OK responses
- Error responses might have different structures depending on the endpoint
- Rate limiting: Handle 429 responses with exponential backoff

## Person API Edge Cases

### Person Creation

- **Names**: Can't be empty, but can be just whitespace (which Pipedrive trims)
- **Email/Phone Format**: 
  - Pipedrive doesn't strictly validate email formats
  - Phone numbers aren't validated for format
  - Both need to be provided as arrays of objects with `value`, `label`, and `primary` fields
  - To clear emails/phones, send an empty array (`[]`), not `null`

### Person Updates

- **Partial Updates**: Only fields included in the PATCH request are updated
- **Organization Association**: When changing `org_id` to null, the person is dissociated from any organization
- **Custom Fields**: Custom fields need to be updated using their hash key, which looks like `9dc80c50d78a15643bfc4ca79d76156a73a1ca0e`

### Person Deletion

- Deletion is soft (marked as deleted) rather than permanent
- Deleted persons can still be retrieved within 30 days using filters
- After 30 days, they're permanently removed

## ID Handling

- All IDs from Pipedrive are integers
- Our tools accept string IDs and convert them to integers
- Always validate IDs before sending to the API
- IDs of 0 are invalid

## Visibility Settings

Visibility settings (`visible_to`) have specific integer values:
- `1`: Owner only
- `3`: Entire company
- `5`: Owner's visibility group
- Sending invalid visibility values results in API errors

## Date and Time Formats

- Dates should be in ISO 8601 format (YYYY-MM-DD)
- Timestamps should be in RFC3339 format (e.g., 2025-01-01T10:20:00Z)
- All times in the API are in UTC timezone

## Custom Fields

- Custom field keys are 40-character hash strings
- Custom field values need to match the expected type (e.g., monetary, date, enum)
- When updating custom fields, include the field key directly in the payload, not nested in a custom_fields object

## Empty vs. Null Values

- For most fields, `null` means "remove this value"
- For arrays (like emails, phones), empty array (`[]`) means "remove all values"
- For strings, empty string (`""`) is usually treated as a valid value, not removal

## Implementation Recommendations

1. Always implement proper validation before sending data to the API
2. Use Pydantic models to enforce correct data structures
3. Include specific error handling for known edge cases
4. Add retry logic with backoff for rate limiting
5. Always check the success flag in responses
6. Use the `convert_id_string` utility for all ID conversions