# OpenAPI Governance Specification

Version: 1.0

Status: Approved Target Architecture

Document Type: API Documentation & Governance Specification

Owner: Platform Engineering

Audience:

* Backend Engineers
* Frontend Engineers
* QA Engineers
* Platform Architects
* DevOps Engineers
* API Governance Reviewers

---

# 1. Purpose

This document defines the OpenAPI governance standards for the ATS platform.

The objective is to ensure:

* Consistent API documentation
* Predictable API evolution
* Enterprise-grade API discoverability
* Stable SDK generation
* Contract-first development
* Governance compliance

This specification applies to all public and internal APIs.

---

# 2. Governance Principles

The platform follows:

```text
Contract First
Documentation Driven
Schema Driven
Version Controlled
Backward Compatible
```

OpenAPI documentation is considered:

```text
Source Of Truth
```

not a by-product of implementation.

---

# 3. OpenAPI Ownership

Every API endpoint must have:

| Responsibility        | Owner                |
| --------------------- | -------------------- |
| Business Contract     | Platform Engineering |
| Request Schema        | Backend Team         |
| Response Schema       | Backend Team         |
| OpenAPI Documentation | Backend Team         |
| Contract Review       | Governance Reviewers |

---

# 4. Required API Metadata

The API must define:

```yaml
title
description
version
contact
license
termsOfService
```

Example:

```yaml
title: ATS Platform API
description: Enterprise Applicant Tracking System API
version: 1.0.0
contact:
  name: Platform Engineering
```

---

# 5. API Versioning Standard

All business APIs must be versioned.

Format:

```text
/api/v1
```

Examples:

```text
/api/v1/resume/upload
/api/v1/jobs
/api/v1/analytics
```

Forbidden:

```text
/resume/upload
/jobs
/analytics
```

---

# 6. Endpoint Naming Standards

Endpoints must use:

```text
Plural Resources
Noun-Based Paths
Consistent Naming
```

Preferred:

```text
/api/v1/jobs
/api/v1/users
/api/v1/resumes
```

Avoid:

```text
/api/v1/createJob
/api/v1/getRanking
/api/v1/uploadResume
```

---

# 7. HTTP Method Standards

| Method  | Purpose              |
| ------- | -------------------- |
| GET     | Retrieve             |
| POST    | Create               |
| PUT     | Full Update          |
| PATCH   | Partial Update       |
| DELETE  | Remove               |
| HEAD    | Metadata             |
| OPTIONS | Capability Discovery |

---

# 8. Endpoint Documentation Requirements

Every endpoint must define:

```python
summary
description
response_model
tags
responses
```

Example:

```python
@router.get(
    "/jobs/{job_id}",
    summary="Get Job",
    description="Retrieve job details.",
    response_model=JobResponse
)
```

---

# 9. Required OpenAPI Sections

Every endpoint must document:

```text
Summary
Description
Authentication
Authorization
Request Schema
Response Schema
Error Responses
Examples
```

---

# 10. Tag Governance

All endpoints must belong to a domain tag.

Approved Tags:

```text
Authentication
Resume
Jobs
Matching
Ranking
Analytics
Administration
Health
```

Example:

```python
tags=["Jobs"]
```

---

# 11. Schema Governance

Every request and response must use explicit schemas.

Required:

```python
JobCreateRequest
JobResponse
ResumeResponse
```

Forbidden:

```python
dict
Any
object
```

without justification.

---

# 12. Schema Naming Standards

Requests:

```text
<Resource>CreateRequest
<Resource>UpdateRequest
<Resource>FilterRequest
```

Examples:

```text
JobCreateRequest
ResumeUploadRequest
UserUpdateRequest
```

---

Responses:

```text
<Resource>Response
<Resource>CollectionResponse
```

Examples:

```text
JobResponse
ResumeResponse
RankingResponse
```

---

# 13. Example Requirements

Every endpoint must contain examples.

Request Example:

```json
{
  "title": "Senior Backend Engineer",
  "description": "..."
}
```

Response Example:

```json
{
  "data": {
    "job_id": 1
  }
}
```

---

# 14. Error Documentation Requirements

Every endpoint must document:

| HTTP Status |
| ----------- |
| 400         |
| 401         |
| 403         |
| 404         |
| 422         |
| 500         |

where applicable.

Error responses must reference:

```text
05_Error_Contract_Specification.md
```

---

# 15. Security Documentation Standards

Every protected endpoint must declare:

```yaml
security:
  - BearerAuth: []
```

Documentation must clearly indicate:

```text
Authentication Required
Authorized Roles
Ownership Constraints
```

---

# 16. Authorization Documentation Standards

Every protected endpoint must document:

```text
Allowed Roles
Resource Ownership Rules
Assignment Rules
```

Example:

```text
Allowed Roles:
Recruiter
Admin

Ownership:
Admin Owned Job

Assignment:
Assigned Recruiters May Modify
```

---

# 17. Pagination Documentation Standards

Collection endpoints must document:

Query Parameters:

```text
limit
offset
```

Response Structure:

```json
{
  "items": [],
  "pagination": {}
}
```

---

# 18. Response Documentation Standards

Responses must follow:

```text
06_API_Response_Standardization_Specification.md
```

OpenAPI examples must reflect:

```text
Production Responses
```

not implementation shortcuts.

---

# 19. Deprecated Endpoint Governance

Deprecated endpoints must contain:

```yaml
deprecated: true
```

Documentation must include:

```text
Reason
Replacement Endpoint
Removal Timeline
```

Example:

```text
Deprecated Since:
v2.1

Replacement:
GET /api/v2/jobs
```

---

# 20. Backward Compatibility Rules

Minor Releases May:

```text
Add Optional Fields
Add Endpoints
Add Metadata
```

Minor Releases Must Not:

```text
Remove Fields
Rename Fields
Change Field Types
Change Meanings
```

---

# 21. Breaking Change Governance

Breaking changes require:

```text
New API Version
Migration Guide
Approval Review
```

Examples:

```text
Field Removal
Field Rename
Response Structure Changes
Authentication Changes
```

---

# 22. OpenAPI Generation Standards

OpenAPI documentation must be generated from:

```text
Typed Schemas
Typed Responses
Typed Requests
```

OpenAPI must never rely on:

```text
Dynamic Dictionaries
Untyped Objects
Runtime Guessing
```

---

# 23. Documentation Review Checklist

Every endpoint review must verify:

```text
Summary Exists
Description Exists
Schema Exists
Examples Exist
Error Responses Exist
Security Defined
Tags Defined
Versioned Path
```

All checks must pass before release.

---

# 24. SDK Compatibility Requirements

OpenAPI documents must support generation of:

```text
Python SDK
TypeScript SDK
Java SDK
Go SDK
```

Documentation must avoid constructs that break code generation.

---

# 25. Change Management Process

Any API contract modification requires:

```text
Contract Proposal
Review
Approval
Implementation
Documentation Update
Release
```

Documentation updates are mandatory.

---

# 26. OpenAPI CI/CD Requirements

Build pipelines must validate:

```text
Schema Integrity
OpenAPI Generation
Example Validity
Reference Resolution
Contract Consistency
```

Builds must fail if validation fails.

---

# 27. Governance Rules

No endpoint may be released without:

```text
Versioned Route
Schema Definitions
Examples
Error Documentation
Security Documentation
```

No undocumented endpoint may exist in production.

---

# 28. Compliance Matrix

| Requirement         | Mandatory |
| ------------------- | --------- |
| Versioned Path      | Yes       |
| Request Schema      | Yes       |
| Response Schema     | Yes       |
| Examples            | Yes       |
| Error Documentation | Yes       |
| Security Definition | Yes       |
| OpenAPI Validation  | Yes       |
| Contract Review     | Yes       |

---

# 29. Success Criteria

The OpenAPI Governance Program is complete when:

```text
Every Endpoint Is Versioned
Every Endpoint Is Documented
Every Endpoint Has Examples
Every Endpoint Uses Typed Schemas
All Errors Are Documented
Authentication Is Documented
Authorization Is Documented
SDK Generation Works Reliably
Governance Reviews Are Enforced
```
