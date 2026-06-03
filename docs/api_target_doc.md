# ATS Platform API Inventory Specification

Version: 1.0

Status: Target Contract Baseline

Audience:

* Backend Engineering
* Frontend Engineering
* QA Engineering
* Platform Governance
* DevOps
* Product Engineering

---

# 1. Purpose

This document defines the authoritative API inventory for the ATS platform.

The purpose of this inventory is to establish:

* API boundaries
* Resource ownership
* Request contracts
* Response contracts
* Error contracts
* Authentication boundaries
* Authorization boundaries
* OpenAPI requirements

This document intentionally focuses on API contracts and excludes implementation details.

---

# 2. Domain Overview

The ATS platform consists of five primary business domains.

```text
User
│
├── Resume
│
├── Job
│
├── Match
│
├── Ranking
│
└── Analytics
```

Data flow:

```text
Resume
      │
      ▼
Embedding

Job
      │
      ▼
Embedding

Resume + Job
      │
      ▼
Matching Engine
      │
      ▼
MatchResult
      │
 ┌────┴────┐
 │         │
 ▼         ▼
Ranking Analytics
```

---

# 3. API Domains

## Resume Domain

Purpose:

Candidate profile ingestion and resume processing.

Ownership:

User-owned resource.

Primary Resource:

Resume

---

## Job Domain

Purpose:

Job creation and management.

Ownership:

Recruiter-owned resource.

Primary Resource:

Job

---

## Match Domain

Purpose:

Matching resumes against jobs.

Ownership:

System-generated resource.

Primary Resource:

MatchResult

---

## Ranking Domain

Purpose:

Candidate ranking and recruiter shortlist generation.

Ownership:

Derived resource.

Primary Resource:

RankedCandidate

---

## Analytics Domain

Purpose:

Recruiter insights and hiring intelligence.

Ownership:

Derived resource.

Primary Resource:

JobAnalytics

---

# 4. Resource Inventory

## Resume

Description:

Represents a candidate resume uploaded into the ATS.

### Public Fields

| Field            | Type    |
| ---------------- | ------- |
| id               | integer |
| parse_status     | string  |
| skills_found     | integer |
| contact          | object  |
| experience_years | integer |
| text_snippet     | string  |

### Internal Fields

Not exposed externally.

| Field            |
| ---------------- |
| file_path        |
| parsed_data      |
| embedding_vector |

---

## Job

Description:

Represents an active recruiting position.

### Public Fields

| Field           | Type          |
| --------------- | ------------- |
| id              | integer       |
| title           | string        |
| description     | string        |
| required_skills | array[string] |
| min_experience  | integer       |
| status          | string        |
| created_at      | datetime      |

### Internal Fields

| Field            |
| ---------------- |
| recruiter_id     |
| embedding_vector |
| updated_at       |

---

## MatchResult

Description:

Persisted matching outcome between a Resume and a Job.

### Public Fields

| Field            | Type    |
| ---------------- | ------- |
| resume_id        | integer |
| job_id           | integer |
| semantic_score   | float   |
| skill_score      | float   |
| experience_score | float   |
| final_score      | float   |
| explanation      | object  |

### Internal Fields

| Field      |
| ---------- |
| created_at |
| updated_at |

---

## RankedCandidate

Description:

Read-optimized candidate ranking projection.

### Public Fields

| Field             | Type    |
| ----------------- | ------- |
| resume_id         | integer |
| scores.final      | float   |
| scores.semantic   | float   |
| scores.skills     | float   |
| scores.experience | float   |

---

## JobAnalytics

Description:

Aggregate recruiter-facing hiring insights.

### Fields

| Field            | Type    |
| ---------------- | ------- |
| total_candidates | integer |
| average_score    | float   |
| top_score        | float   |
| lowest_score     | float   |
| pool_quality     | string  |

---

# 5. Endpoint Inventory

## Resume APIs

### Upload Resume

Method:

```http
POST
```

Path:

```http
/resume/upload
```

Purpose:

Upload and process candidate resume.

Request Type:

```text
multipart/form-data
```

Response:

```text
ResumeResponse
```

---

## Job APIs

### Create Job

Method:

```http
POST /jobs
```

Purpose:

Create recruiting job.

Response:

```text
JobResponse
```

---

### Get Job

Method:

```http
GET /jobs/{job_id}
```

Purpose:

Retrieve job details.

Response:

```text
JobResponse
```

---

## Match APIs

### Match Resume To Job

Method:

```http
POST /match/resume/{resume_id}/job/{job_id}
```

Purpose:

Generate or refresh match.

Response:

```text
MatchResponse
```

---

## Ranking APIs

### Get Ranked Candidates

Method:

```http
GET /analytics/job/{job_id}/ranking
```

Purpose:

Retrieve ranked candidate list.

Response:

```text
RankedCandidate[]
```

Pagination:

```text
limit
offset
```

---

## Analytics APIs

### Job Summary

Method:

```http
GET /analytics/job/{job_id}/summary
```

Purpose:

Recruiter hiring insights.

Response:

```text
JobAnalytics
```

---

# 6. Request Contract Inventory

## Resume Upload Request

| Field | Type   | Required |
| ----- | ------ | -------- |
| file  | binary | Yes      |

---

## Job Create Request

| Field           | Type          | Required |
| --------------- | ------------- | -------- |
| title           | string        | Yes      |
| description     | string        | Yes      |
| required_skills | array[string] | Yes      |
| min_experience  | integer       | Yes      |

---

# 7. Response Contract Inventory

## ResumeResponse

```json
{
  "resume_id": 1,
  "parse_status": "success",
  "skills_found": 12,
  "contact": {},
  "experience_years": 5,
  "text_snippet": "..."
}
```

---

## JobResponse

```json
{
  "id": 1,
  "title": "Backend Engineer",
  "description": "...",
  "required_skills": ["python"],
  "min_experience": 3,
  "status": "open",
  "created_at": "2026-01-01T00:00:00Z"
}
```

---

## MatchResponse

```json
{
  "resume_id": 1,
  "job_id": 10,
  "semantic_score": 0.82,
  "skill_score": 0.88,
  "experience_score": 0.75,
  "final_score": 0.83,
  "explanation": {}
}
```

---

## RankedCandidateResponse

```json
{
  "resume_id": 1,
  "scores": {
    "final": 0.91,
    "semantic": 0.88,
    "skills": 0.94,
    "experience": 0.85
  }
}
```

---

## JobAnalyticsResponse

```json
{
  "total_candidates": 250,
  "average_score": 0.63,
  "top_score": 0.96,
  "lowest_score": 0.12,
  "pool_quality": "strong applicants"
}
```

---

# 8. Standard Error Contract

All APIs must return:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Job not found"
  }
}
```

Standard Categories:

* VALIDATION_ERROR
* UNAUTHORIZED
* FORBIDDEN
* RESOURCE_NOT_FOUND
* CONFLICT
* INTERNAL_ERROR

---

# 9. Authentication Boundary

Authentication applies to all business APIs.

Excluded:

```text
/health
/docs
/openapi.json
```

Identity Source:

```text
Authenticated User
```

Transport:

```text
Bearer Token
```

---

# 10. Authorization Boundary

## Candidate

Permissions:

```text
Upload Resume
View Own Resume
View Own Matches
```

---

## Recruiter

Permissions:

```text
Create Job
View Job
View Rankings
View Analytics
```

---

## Admin

Permissions:

```text
Platform Administration
```

---

# 11. Pagination Standard

Supported Query Parameters:

```text
limit
offset
```

Defaults:

```text
limit = 10
offset = 0
```

---

# 12. OpenAPI Requirements

Every endpoint must define:

* summary
* description
* response_model
* status codes
* tags
* examples

Required API metadata:

* title
* description
* version
* contact

---

# 13. Governance Rules

API responses must never expose:

* embedding_vector
* file_path
* parsed_data
* internal database identifiers
* ML implementation details

Business APIs must never return raw ORM objects.

All responses must use schema contracts.

---

# 14. Platform Readiness Target

Contract Maturity:

```text
Excellent
```

OpenAPI Readiness:

```text
10/10
```

Frontend Readiness:

```text
10/10
```

Governance Readiness:

```text
10/10
```

Production Readiness:

```text
Ready
```
