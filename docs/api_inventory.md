# ATS Platform API Inventory Specification

Version: 1.0

Status: Target Enterprise Contract

Document Type: Authoritative API Inventory

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

This document defines the complete API inventory for the ATS platform.

The API Inventory Specification acts as the authoritative source of truth for:

* Public API Surface
* Resource Ownership
* API Contracts
* Request Models
* Response Models
* Security Boundaries
* Authorization Boundaries
* Data Exposure Rules
* OpenAPI Governance
* Contract Stabilization Activities

This document intentionally describes the API contract and business boundaries rather than implementation details.

---

# 2. Platform Overview

The ATS platform is designed as a recruiter-centric enterprise hiring system.

Primary Business Objectives:

```text
Resume Ingestion
Job Management
Candidate Matching
Candidate Ranking
Recruiter Analytics
```

The platform is intended for:

```text
Candidates
Recruiters
Administrators
```

---

# 3. Domain Architecture

```text
Candidate
     │
     ▼
 Resume
     │
     ▼
 Resume Processing
     │
     ▼
 Resume Embedding
     │

Job
     │
     ▼
 Job Processing
     │
     ▼
 Job Embedding

Resume + Job
     │
     ▼
 Matching Engine
     │
     ▼
 MatchResult
     │
 ┌───┴───────────┐
 │               │
 ▼               ▼
Ranking      Analytics
```

---

# 4. Domain Inventory

## Resume Domain

Purpose:

Candidate profile ingestion and resume processing.

Primary Resource:

```text
Resume
```

Owner:

```text
Candidate
```

Consumers:

```text
Candidate
Recruiter
Admin
```

---

## Job Domain

Purpose:

Job lifecycle management.

Primary Resource:

```text
Job
```

Owner:

```text
Admin/System
```

Consumers:

```text
Recruiter
Admin
```

---

## Match Domain

Purpose:

Resume-to-job matching.

Primary Resource:

```text
MatchResult
```

Owner:

```text
System
```

Consumers:

```text
Recruiter
Admin
```

---

## Ranking Domain

Purpose:

Candidate ranking and shortlist generation.

Primary Resource:

```text
RankedCandidate
```

Owner:

```text
System
```

Consumers:

```text
Recruiter
Admin
```

---

## Analytics Domain

Purpose:

Recruiter decision support and hiring intelligence.

Primary Resource:

```text
JobAnalytics
```

Owner:

```text
System
```

Consumers:

```text
Recruiter
Admin
```

---

# 5. Actor Inventory

## Candidate

Description:

Resume owner.

Responsibilities:

```text
Upload Resume
Maintain Resume
Manage Candidate Profile
```

---

## Recruiter

Description:

Hiring operations user.

Responsibilities:

```text
Review Candidates
View Rankings
View Analytics
Manage Assigned Jobs
```

---

## Admin

Description:

Platform administrator.

Responsibilities:

```text
Create Jobs
Manage Jobs
Assign Recruiters
Manage Users
Manage Platform
```

---

# 6. Resource Inventory

---

## Resume

Description:

Represents a candidate resume.

### Public Fields

| Field            | Type    |
| ---------------- | ------- |
| resume_id        | integer |
| parse_status     | string  |
| skills_found     | integer |
| contact          | object  |
| experience_years | integer |
| text_snippet     | string  |

### Internal Fields

Not exposed through API.

| Field            |
| ---------------- |
| file_path        |
| parsed_data      |
| embedding_vector |

---

## Job

Description:

Represents a recruiting position.

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

| Field                 |
| --------------------- |
| recruiter_assignments |
| recruiter_id          |
| embedding_vector      |
| updated_at            |

---

## MatchResult

Description:

Persisted matching outcome.

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

Read-optimized ranking projection.

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

Recruiter-facing hiring insights.

### Public Fields

| Field            | Type    |
| ---------------- | ------- |
| total_candidates | integer |
| average_score    | float   |
| top_score        | float   |
| lowest_score     | float   |
| pool_quality     | string  |

---

# 7. Endpoint Inventory

## Resume APIs

### Upload Resume

Method:

```http
POST
```

Path:

```http
/api/v1/resume/upload
```

Authentication:

```text
Required
```

Authorized Roles:

```text
Candidate
```

Purpose:

```text
Upload and process resume.
```

Request:

```text
multipart/form-data
```

Response:

```text
ResumeResponse
```

Side Effects:

```text
Store Resume
Generate Embedding
Trigger Matching
```

---

## Job APIs

### Create Job

Method:

```http
POST
```

Path:

```http
/api/v1/jobs
```

Authentication:

```text
Required
```

Authorized Roles:

```text
Admin
```

Purpose:

```text
Create Job
```

Response:

```text
JobResponse
```

Side Effects:

```text
Generate Embedding
Trigger Matching
```

---

### Get Job

Method:

```http
GET
```

Path:

```http
/api/v1/jobs/{job_id}
```

Authentication:

```text
Required
```

Authorized Roles:

```text
Recruiter
Admin
```

Response:

```text
JobResponse
```

---

## Match APIs

### Match Resume To Job

Method:

```http
POST
```

Path:

```http
/api/v1/match/resume/{resume_id}/job/{job_id}
```

Authentication:

```text
Required
```

Authorized Roles:

```text
Recruiter
Admin
```

Purpose:

```text
Force Match Refresh
```

Response:

```text
MatchResponse
```

---

## Analytics APIs

### Job Summary

Method:

```http
GET
```

Path:

```http
/api/v1/analytics/job/{job_id}/summary
```

Authentication:

```text
Required
```

Authorized Roles:

```text
Recruiter
Admin
```

Response:

```text
JobAnalyticsResponse
```

---

### Job Ranking

Method:

```http
GET
```

Path:

```http
/api/v1/analytics/job/{job_id}/ranking
```

Authentication:

```text
Required
```

Authorized Roles:

```text
Recruiter
Admin
```

Query Parameters:

| Name   | Type    | Default |
| ------ | ------- | ------- |
| limit  | integer | 10      |
| offset | integer | 0       |

Response:

```text
RankedCandidateResponse[]
```

---

## Health APIs

### Health Check

Method:

```http
GET
```

Path:

```http
/health
```

Authentication:

```text
Not Required
```

Purpose:

```text
Service Health Verification
```

---

# 8. Request Contract Inventory

## Resume Upload Request

| Field | Type   | Required |
| ----- | ------ | -------- |
| file  | binary | Yes      |

Content Type:

```text
multipart/form-data
```

---

## JobCreateRequest

| Field           | Type          | Required |
| --------------- | ------------- | -------- |
| title           | string        | Yes      |
| description     | string        | Yes      |
| required_skills | array[string] | Yes      |
| min_experience  | integer       | Yes      |

Validation:

```text
Title Length
Description Length
Skill Normalization
Experience Bounds
```

---

# 9. Response Contract Inventory

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

# 10. Authentication Boundary

Protected APIs:

```text
/resume/*
/jobs/*
/match/*
/analytics/*
```

Public APIs:

```text
/health
/docs
/openapi.json
```

Authentication Method:

```text
JWT Bearer Token
```

Identity Source:

```text
Validated JWT Claims
```

---

# 11. Authorization Boundary

| Resource        | Candidate | Recruiter     | Admin |
| --------------- | --------- | ------------- | ----- |
| Resume Upload   | Allow     | Deny          | Deny  |
| Resume View     | Own Only  | Allow         | Allow |
| Job Create      | Deny      | Deny          | Allow |
| Job View        | Deny      | Allow         | Allow |
| Job Modify      | Deny      | Assigned Only | Allow |
| Match View      | Deny      | Allow         | Allow |
| Analytics View  | Deny      | Allow         | Allow |
| Ranking View    | Deny      | Allow         | Allow |
| User Management | Deny      | Deny          | Allow |

---

# 12. Business Events Inventory

Generated Events:

```text
RESUME_UPLOADED
RESUME_PARSED
EMBEDDING_GENERATED
JOB_CREATED
MATCH_GENERATED
MATCH_REFRESHED
RANKING_VIEWED
ANALYTICS_VIEWED
```

---

# 13. Audit Requirements

The following actions must generate audit records:

```text
Resume Upload
Job Creation
Job Modification
Recruiter Assignment
Authentication Events
Authorization Failures
Match Recompute
Analytics Access
```

---

# 14. Data Classification

## Public Business Data

```text
Job Title
Job Description
Required Skills
```

---

## Internal Business Data

```text
Rankings
Match Scores
Analytics
```

---

## Sensitive Data

```text
Candidate Contact Information
Resume Content
User Email
Authentication Data
```

---

## Restricted System Data

```text
Embedding Vectors
Internal Parser Data
File Paths
System Secrets
JWT Secrets
```

---

# 15. OpenAPI Readiness Requirements

Every endpoint must define:

```text
Summary
Description
Tags
Request Model
Response Model
Status Codes
Examples
Security Requirements
```

---

# 16. Governance Rules

The API must never expose:

```text
embedding_vector
file_path
parsed_data
internal database identifiers
authentication secrets
```

Business APIs must never trust:

```text
user_id from request
recruiter_id from request
role values from request
```

Identity must always originate from:

```text
Validated JWT Claims
```

---

# 17. Platform Readiness Targets

Contract Maturity:

```text
Excellent
```

Frontend Readiness:

```text
10/10
```

OpenAPI Readiness:

```text
10/10
```

Security Readiness:

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
