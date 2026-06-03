# API Response Standardization Specification

Version: 1.0

Status: Approved Target Architecture

Document Type: API Response Governance Specification

Owner: Platform Engineering

Audience:

* Backend Engineers
* Frontend Engineers
* QA Engineers
* API Governance Reviewers
* DevOps Engineers

---

# 1. Purpose

This document defines the standard response contract for all ATS platform APIs.

The objective is to ensure:

* Consistent API responses
* Predictable frontend integrations
* Simplified SDK development
* Stable OpenAPI generation
* Uniform pagination
* Consistent metadata handling

This specification applies to all successful API responses.

Error responses are governed by:

```text
05_Error_Contract_Specification.md
```

---

# 2. Design Principles

All APIs must satisfy:

```text
Consistency
Predictability
Extensibility
Backward Compatibility
Observability
```

Clients should never need endpoint-specific parsing strategies.

---

# 3. Response Categories

The platform supports four response categories:

```text
Resource Response
Collection Response
Action Response
Health Response
```

---

# 4. Resource Response Contract

Used when returning a single business resource.

Examples:

```text
Resume
Job
MatchResult
Analytics Summary
```

Format:

```json
{
  "data": {
    ...
  }
}
```

Example:

```json
{
  "data": {
    "id": 1,
    "title": "Backend Engineer"
  }
}
```

---

# 5. Collection Response Contract

Used when returning multiple resources.

Examples:

```text
Rankings
Candidate Lists
Jobs
Users
```

Format:

```json
{
  "items": [],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "total": 250
  }
}
```

---

# 6. Action Response Contract

Used when an operation performs work.

Examples:

```text
Resume Upload
Job Creation
Recruiter Assignment
```

Format:

```json
{
  "data": {
    ...
  },
  "meta": {
    "action": "resume_uploaded"
  }
}
```

---

# 7. Health Response Contract

Used only for health endpoints.

Format:

```json
{
  "status": "healthy",
  "service": "ats-api",
  "version": "1.0.0"
}
```

---

# 8. Metadata Contract

Metadata contains information about the response, not the business resource.

Format:

```json
{
  "meta": {
    "request_id": "req_123",
    "timestamp": "2026-06-02T12:00:00Z"
  }
}
```

---

## Required Metadata Fields

| Field      | Required |
| ---------- | -------- |
| request_id | Yes      |
| timestamp  | Yes      |

---

# 9. Pagination Contract

All collection endpoints must support:

```text
limit
offset
```

Default values:

```text
limit = 10
offset = 0
```

---

## Pagination Response

```json
{
  "items": [],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "total": 500
  }
}
```

---

# 10. Resource Naming Rules

Responses must use domain names.

Preferred:

```json
{
  "resume_id": 1
}
```

Avoid:

```json
{
  "id": 1
}
```

when resource context is ambiguous.

---

# 11. Collection Naming Rules

Use:

```text
items
```

for collections.

Allowed:

```json
{
  "items": [...]
}
```

Forbidden:

```json
{
  "data": [...]
}
```

```json
{
  "results": [...]
}
```

```json
{
  "records": [...]
}
```

---

# 12. Timestamp Rules

All timestamps must:

```text
Use UTC
Use ISO-8601
Include timezone information
```

Example:

```text
2026-06-02T12:00:00Z
```

---

# 13. Null Handling Rules

Allowed:

```json
{
  "contact": null
}
```

Forbidden:

```json
{}
```

when a field exists in schema.

Responses must be explicit.

---

# 14. Boolean Rules

Booleans must never be encoded as:

```text
0 / 1
yes / no
true_string / false_string
```

Use:

```json
{
  "is_active": true
}
```

---

# 15. Numeric Precision Rules

Scores:

```text
4 Decimal Places Maximum
```

Example:

```json
{
  "final_score": 0.8725
}
```

Avoid:

```json
{
  "final_score": 0.87253423824
}
```

---

# 16. Ranking Response Contract

Ranking responses must use:

```json
{
  "items": [
    {
      "resume_id": 1,
      "scores": {
        "final": 0.92,
        "semantic": 0.88,
        "skills": 0.94,
        "experience": 0.86
      }
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "total": 100
  }
}
```

---

# 17. Analytics Response Contract

Analytics endpoints return:

```json
{
  "data": {
    "total_candidates": 100,
    "average_score": 0.74,
    "top_score": 0.95,
    "lowest_score": 0.12,
    "pool_quality": "strong applicants"
  }
}
```

---

# 18. Resume Upload Response Contract

```json
{
  "data": {
    "resume_id": 10,
    "parse_status": "success",
    "skills_found": 25,
    "experience_years": 7
  },
  "meta": {
    "action": "resume_uploaded"
  }
}
```

---

# 19. Job Creation Response Contract

```json
{
  "data": {
    "job_id": 20,
    "title": "Senior Backend Engineer"
  },
  "meta": {
    "action": "job_created"
  }
}
```

---

# 20. Version Compatibility Rules

Future versions may:

```text
Add Optional Fields
Add Metadata Fields
Add Collection Metadata
```

Future versions must not:

```text
Rename Existing Fields
Remove Existing Fields
Change Field Types
```

without API version increment.

---

# 21. OpenAPI Requirements

Every response must:

```text
Use Explicit Pydantic Schemas
Avoid Generic Dict Types
Avoid Untyped Objects
Document Examples
```

Example:

Preferred:

```python
scores: CandidateScores
```

Forbidden:

```python
scores: dict
```

---

# 22. Governance Rules

Business APIs must never return:

```text
ORM Models
Database Rows
Internal IDs
Embedding Vectors
File Paths
Stack Traces
```

All responses must pass through:

```text
Response Schemas
Serialization Layer
```

---

# 23. Success Criteria

The Response Standardization Contract is complete when:

```text
Every Endpoint Uses Standard Response Structures
Every Collection Uses Pagination Contract
Every Resource Uses Resource Contract
Every Action Uses Action Contract
All Responses Are Schema Driven
Frontend Parsing Logic Is Consistent
OpenAPI Generation Is Predictable
Future Versioning Is Safe
```
