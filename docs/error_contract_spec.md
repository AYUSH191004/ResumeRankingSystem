# Error Contract Specification

Version: 1.0

Status: Approved Target Architecture

Document Type: Platform Error Governance Specification

Owner: Platform Engineering

Audience:

* Backend Engineers
* Frontend Engineers
* QA Engineers
* DevOps Engineers
* Security Engineers
* Platform Governance Reviewers

---

# 1. Purpose

This document defines the enterprise-wide error handling contract for the ATS platform.

The Error Contract establishes:

* Standard Error Response Format
* Error Categories
* Error Codes
* HTTP Status Mapping
* Validation Error Standards
* Authentication Error Standards
* Authorization Error Standards
* Business Rule Error Standards
* Logging Requirements
* Observability Requirements

This specification applies to all APIs.

---

# 2. Design Principles

The error system must satisfy:

```text
Consistency
Predictability
Debuggability
Security
Observability
Client Compatibility
```

Every API must return errors using a unified schema.

Clients must never need endpoint-specific error handling.

---

# 3. Standard Error Envelope

All API failures must return:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Job not found",
    "details": {},
    "request_id": "e4e4a9cb-0f98-4e4c-a6a3-6f8e4ef6c5f2",
    "timestamp": "2026-06-02T12:00:00Z"
  }
}
```

---

# 4. Error Object Definition

## code

Machine-readable identifier.

Purpose:

```text
Frontend logic
Automation
Monitoring
Alerting
```

Example:

```text
RESOURCE_NOT_FOUND
```

---

## message

Human-readable message.

Purpose:

```text
User Display
Developer Understanding
```

Example:

```text
Job not found
```

---

## details

Structured contextual information.

Example:

```json
{
  "job_id": 15
}
```

Optional.

May be empty.

---

## request_id

Unique request identifier.

Purpose:

```text
Tracing
Support Investigation
Log Correlation
```

Required.

---

## timestamp

UTC timestamp of error generation.

Required.

Format:

```text
ISO-8601 UTC
```

---

# 5. Error Categories

The platform supports the following error categories.

| Category       | Description                   |
| -------------- | ----------------------------- |
| VALIDATION     | Invalid input                 |
| AUTHENTICATION | Identity failure              |
| AUTHORIZATION  | Permission failure            |
| RESOURCE       | Resource missing              |
| BUSINESS_RULE  | Business constraint violation |
| CONFLICT       | State conflict                |
| RATE_LIMIT     | Usage limits                  |
| INFRASTRUCTURE | System dependency failure     |
| INTERNAL       | Unexpected failure            |

---

# 6. HTTP Status Mapping

| HTTP Status | Category       |
| ----------- | -------------- |
| 400         | VALIDATION     |
| 401         | AUTHENTICATION |
| 403         | AUTHORIZATION  |
| 404         | RESOURCE       |
| 409         | CONFLICT       |
| 422         | BUSINESS_RULE  |
| 429         | RATE_LIMIT     |
| 500         | INTERNAL       |
| 502         | INFRASTRUCTURE |
| 503         | INFRASTRUCTURE |

---

# 7. Validation Error Contract

Used when request data fails validation.

HTTP Status:

```text
400 Bad Request
```

Error Code:

```text
VALIDATION_ERROR
```

Example:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "field": "title",
      "reason": "minimum length is 3"
    },
    "request_id": "req_123",
    "timestamp": "2026-06-02T12:00:00Z"
  }
}
```

---

# 8. Authentication Errors

Authentication failures occur before authorization.

---

## Invalid Token

HTTP:

```text
401 Unauthorized
```

Code:

```text
AUTH_INVALID_TOKEN
```

Example:

```json
{
  "error": {
    "code": "AUTH_INVALID_TOKEN",
    "message": "Token is invalid"
  }
}
```

---

## Expired Token

HTTP:

```text
401 Unauthorized
```

Code:

```text
AUTH_TOKEN_EXPIRED
```

Example:

```json
{
  "error": {
    "code": "AUTH_TOKEN_EXPIRED",
    "message": "Token has expired"
  }
}
```

---

## Missing Token

HTTP:

```text
401 Unauthorized
```

Code:

```text
AUTH_TOKEN_MISSING
```

---

## Inactive Account

HTTP:

```text
401 Unauthorized
```

Code:

```text
AUTH_USER_INACTIVE
```

---

# 9. Authorization Errors

Authorization failures occur after identity is resolved.

---

## Permission Denied

HTTP:

```text
403 Forbidden
```

Code:

```text
AUTHORIZATION_DENIED
```

Example:

```json
{
  "error": {
    "code": "AUTHORIZATION_DENIED",
    "message": "Insufficient permissions"
  }
}
```

---

## Resource Access Denied

HTTP:

```text
403 Forbidden
```

Code:

```text
RESOURCE_ACCESS_DENIED
```

Example:

```json
{
  "error": {
    "code": "RESOURCE_ACCESS_DENIED",
    "message": "Access to resource denied"
  }
}
```

---

# 10. Resource Errors

---

## Job Not Found

HTTP:

```text
404 Not Found
```

Code:

```text
JOB_NOT_FOUND
```

Example:

```json
{
  "error": {
    "code": "JOB_NOT_FOUND",
    "message": "Job does not exist"
  }
}
```

---

## Resume Not Found

HTTP:

```text
404 Not Found
```

Code:

```text
RESUME_NOT_FOUND
```

---

## User Not Found

HTTP:

```text
404 Not Found
```

Code:

```text
USER_NOT_FOUND
```

---

## Match Not Found

HTTP:

```text
404 Not Found
```

Code:

```text
MATCH_NOT_FOUND
```

---

# 11. Business Rule Errors

Business rule errors represent valid requests that violate platform policies.

---

## Resume Parsing Failed

HTTP:

```text
422 Unprocessable Entity
```

Code:

```text
RESUME_PARSE_FAILED
```

Example:

```json
{
  "error": {
    "code": "RESUME_PARSE_FAILED",
    "message": "Unable to parse uploaded resume"
  }
}
```

---

## Embedding Generation Failed

HTTP:

```text
422 Unprocessable Entity
```

Code:

```text
EMBEDDING_GENERATION_FAILED
```

---

## Matching Failed

HTTP:

```text
422 Unprocessable Entity
```

Code:

```text
MATCHING_FAILED
```

---

## Recruiter Assignment Invalid

HTTP:

```text
422 Unprocessable Entity
```

Code:

```text
INVALID_RECRUITER_ASSIGNMENT
```

---

# 12. Conflict Errors

Used when current state prevents requested action.

---

## Duplicate Resource

HTTP:

```text
409 Conflict
```

Code:

```text
RESOURCE_ALREADY_EXISTS
```

---

## Job Already Archived

HTTP:

```text
409 Conflict
```

Code:

```text
JOB_ALREADY_ARCHIVED
```

---

## Assignment Conflict

HTTP:

```text
409 Conflict
```

Code:

```text
ASSIGNMENT_CONFLICT
```

---

# 13. Rate Limit Errors

HTTP:

```text
429 Too Many Requests
```

Code:

```text
RATE_LIMIT_EXCEEDED
```

Example:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded"
  }
}
```

---

# 14. Infrastructure Errors

Generated when dependencies fail.

---

## Database Failure

HTTP:

```text
503 Service Unavailable
```

Code:

```text
DATABASE_UNAVAILABLE
```

---

## Cache Failure

HTTP:

```text
503 Service Unavailable
```

Code:

```text
CACHE_UNAVAILABLE
```

---

## Queue Failure

HTTP:

```text
503 Service Unavailable
```

Code:

```text
QUEUE_UNAVAILABLE
```

---

## Model Service Failure

HTTP:

```text
503 Service Unavailable
```

Code:

```text
MODEL_SERVICE_UNAVAILABLE
```

---

# 15. Internal Errors

Unexpected failures.

HTTP:

```text
500 Internal Server Error
```

Code:

```text
INTERNAL_SERVER_ERROR
```

Response:

```json
{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected error occurred"
  }
}
```

---

# 16. Security Rules

The platform must never expose:

```text
Stack Traces
Database Queries
Connection Strings
JWT Secrets
Internal File Paths
Embedding Vectors
Infrastructure Details
```

Forbidden Example:

```json
{
  "detail": "sqlalchemy.exc.IntegrityError..."
}
```

---

# 17. Logging Requirements

Every error must generate a log entry.

Required Fields:

```text
request_id
user_id
role
endpoint
http_method
error_code
http_status
timestamp
```

---

# 18. Observability Requirements

All errors must be measurable.

Metrics:

```text
error_count
error_rate
error_by_endpoint
error_by_code
authentication_failures
authorization_failures
infrastructure_failures
```

---

# 19. OpenAPI Requirements

Every endpoint must document:

```text
Success Responses
Validation Errors
Authentication Errors
Authorization Errors
Business Errors
Internal Errors
```

Example:

```text
200
400
401
403
404
422
500
```

must be explicitly documented.

---

# 20. Governance Rules

All APIs must:

```text
Return Standard Error Envelope
Use Approved Error Codes
Include Request ID
Include Timestamp
Log Error Event
Avoid Internal Information Disclosure
```

No endpoint may return:

```text
detail
traceback
raw exception strings
framework-generated error payloads
```

directly to clients.

---

# 21. Success Criteria

The Error Contract is considered complete when:

```text
Every API Returns Standard Error Responses
Every Error Has A Stable Code
All HTTP Status Codes Are Standardized
Authentication Errors Are Consistent
Authorization Errors Are Consistent
Business Errors Are Consistent
Logs Correlate With API Errors
Frontend Can Reliably Handle Failures
OpenAPI Documents All Failure Modes
```
