# Identity, Roles & Ownership Specification

Version: 1.0

Status: Approved Target Architecture

Document Type: Identity Governance Specification

Owner: Platform Engineering

Audience:

* Backend Engineers
* Frontend Engineers
* Security Engineers
* QA Engineers
* DevOps Engineers
* Platform Governance Reviewers

---

# 1. Purpose

This document defines:

* Identity Model
* Actor Model
* Role Hierarchy
* Resource Ownership
* Resource Assignment
* Visibility Rules
* Access Boundaries

This document serves as the authoritative source of truth for:

* Authentication Design
* Authorization Design
* Resource Security
* Audit Logging
* Frontend Access Control
* API Governance

---

# 2. Core Principles

The ATS platform follows the following principles:

```text
Identity → Role → Ownership → Authorization
```

The platform never grants access based solely on:

```text
User ID
Email
Client Supplied Data
```

Access decisions are always derived from:

```text
Authenticated Identity
Assigned Role
Resource Ownership
Resource Assignment
```

---

# 3. Identity Model

## User

Every authenticated actor in the system is a User.

A User represents a uniquely identifiable platform principal.

### User Attributes

| Field      | Type     |
| ---------- | -------- |
| user_id    | integer  |
| email      | string   |
| role       | enum     |
| status     | enum     |
| created_at | datetime |
| updated_at | datetime |

---

## User Status

Supported states:

| Status    | Description               |
| --------- | ------------------------- |
| active    | User may authenticate     |
| inactive  | User cannot authenticate  |
| locked    | Security lockout          |
| suspended | Administrative suspension |

Only:

```text
active
```

users may access business APIs.

---

# 4. Actor Model

The platform supports three actor types.

```text
Candidate
Recruiter
Admin
```

---

# 5. Candidate Role

## Purpose

Represents a job applicant.

Candidate is the owner of their resume profile.

---

## Responsibilities

```text
Upload Resume
Maintain Resume Information
Manage Candidate Profile
```

---

## Business Scope

Candidates are data providers.

They are not decision makers.

---

## Candidate Permissions

Allowed:

```text
Upload Resume
Update Own Resume
View Own Resume
Manage Own Profile
```

Denied:

```text
Create Job
Modify Job
View Rankings
View Analytics
View Match Scores
Manage Users
```

---

## Candidate Visibility

Can View:

```text
Own Resume
Own Profile
```

Cannot View:

```text
Other Candidate Profiles
Match Scores
Rankings
Recruiter Analytics
Jobs
```

---

# 6. Recruiter Role

## Purpose

Represents recruiting operations personnel.

Recruiters evaluate candidates and execute hiring workflows.

---

## Responsibilities

```text
Candidate Evaluation
Shortlisting
Ranking Review
Analytics Review
Assigned Job Management
```

---

## Business Scope

Recruiters operate on jobs assigned to them.

Recruiters do not own jobs.

---

## Recruiter Permissions

Allowed:

```text
View Jobs
View Candidate Profiles
View Rankings
View Analytics
View Match Results
Manage Assigned Jobs
Trigger Re-Match
```

Denied:

```text
Create Jobs
Delete Jobs
Assign Recruiters
Manage Users
Modify Platform Configuration
```

---

## Recruiter Visibility

Can View:

```text
All Active Jobs
Candidate Profiles
Match Results
Rankings
Analytics
```

Can Modify:

```text
Assigned Jobs Only
Assigned Candidate Pipelines Only
```

Cannot Modify:

```text
Unassigned Jobs
Platform Configuration
User Accounts
```

---

# 7. Admin Role

## Purpose

Represents platform administration and hiring governance.

Admins own the hiring lifecycle.

---

## Responsibilities

```text
Create Jobs
Manage Jobs
Assign Recruiters
Manage Users
Govern Platform Operations
```

---

## Admin Permissions

Allowed:

```text
Create Job
Update Job
Archive Job
Assign Recruiters
Manage Users
View Analytics
View Rankings
View Match Results
View Candidate Profiles
Manage Platform Configuration
```

---

## Admin Visibility

Can View:

```text
All Resources
All Users
All Jobs
All Candidates
All Analytics
All Match Results
```

Can Modify:

```text
Any Resource
```

---

# 8. Role Hierarchy

```text
Admin
  │
  ▼
Recruiter
  │
  ▼
Candidate
```

Inheritance Model:

```text
Admin inherits Recruiter permissions.
Recruiter does not inherit Admin permissions.
Candidate does not inherit Recruiter permissions.
```

---

# 9. Ownership Model

Ownership determines the authoritative controller of a resource.

Ownership and assignment are different concepts.

```text
Ownership ≠ Assignment
```

---

# 10. Resume Ownership

Resource:

```text
Resume
```

Owner:

```text
Candidate
```

Lifecycle Controller:

```text
Candidate
Admin
```

---

## Visibility

| Actor           | Access |
| --------------- | ------ |
| Candidate Owner | Full   |
| Recruiter       | Read   |
| Admin           | Full   |

---

# 11. Job Ownership

Resource:

```text
Job
```

Owner:

```text
Admin/System
```

Lifecycle Controller:

```text
Admin
```

---

## Visibility

| Actor     | Access |
| --------- | ------ |
| Candidate | None   |
| Recruiter | Read   |
| Admin     | Full   |

---

# 12. Job Assignment Model

Jobs may be assigned to one or more recruiters.

Assignment does not transfer ownership.

Example:

```text
Job Owner:
Admin

Assigned Recruiters:
Recruiter A
Recruiter B
```

Ownership remains:

```text
Admin
```

---

# 13. Recruiter Assignment Rules

Recruiters may:

```text
View Assigned Jobs
Work Assigned Jobs
Manage Assigned Candidate Pipelines
Trigger Match Recalculation
```

Recruiters may not:

```text
Transfer Ownership
Delete Jobs
Assign Recruiters
Archive Jobs Outside Assignment Scope
```

---

# 14. MatchResult Ownership

Resource:

```text
MatchResult
```

Owner:

```text
System
```

Reason:

```text
Generated automatically by platform logic.
```

---

## Visibility

| Actor     | Access |
| --------- | ------ |
| Candidate | None   |
| Recruiter | Read   |
| Admin     | Full   |

---

# 15. Ranking Ownership

Resource:

```text
Ranking
```

Owner:

```text
System
```

Generated From:

```text
MatchResult
```

---

## Visibility

| Actor     | Access |
| --------- | ------ |
| Candidate | None   |
| Recruiter | Read   |
| Admin     | Full   |

---

# 16. Analytics Ownership

Resource:

```text
Analytics
```

Owner:

```text
System
```

Generated From:

```text
MatchResult
```

---

## Visibility

| Actor     | Access |
| --------- | ------ |
| Candidate | None   |
| Recruiter | Read   |
| Admin     | Full   |

---

# 17. Resource Visibility Matrix

| Resource     | Candidate  | Recruiter | Admin |
| ------------ | ---------- | --------- | ----- |
| Own Resume   | Read/Write | Read      | Full  |
| Other Resume | None       | Read      | Full  |
| Job          | None       | Read      | Full  |
| Assigned Job | None       | Manage    | Full  |
| Match Result | None       | Read      | Full  |
| Ranking      | None       | Read      | Full  |
| Analytics    | None       | Read      | Full  |
| User Account | Own Only   | None      | Full  |

---

# 18. Identity Resolution Rules

Identity must never originate from:

```text
Request Payload
Query Parameters
Path Parameters
Headers Controlled By Client
```

Forbidden Examples:

```json
{
  "user_id": 123
}
```

```json
{
  "recruiter_id": 50
}
```

Allowed Source:

```text
Validated Authentication Token
```

---

# 19. Security Boundaries

Candidates are isolated from:

```text
Recruiter Data
Analytics
Ranking
Match Scores
Administrative Resources
```

Recruiters are isolated from:

```text
User Management
Platform Configuration
Administrative Controls
```

Admins have unrestricted access.

---

# 20. Audit Requirements

The following identity-related events must be auditable:

```text
User Login
User Logout
Role Change
Recruiter Assignment
Job Assignment
Account Lock
Account Suspension
Permission Denial
Authorization Failure
```

Audit records must include:

```text
Actor
Role
Action
Resource
Timestamp
Outcome
```

---

# 21. Governance Rules

The platform must never:

```text
Trust Client-Supplied Ownership
Trust Client-Supplied Role Values
Trust Client-Supplied User IDs
Grant Access Without Identity Verification
```

Ownership must always be derived from:

```text
Authenticated Identity
Persisted Resource Ownership
Persisted Resource Assignment
```

---

# 22. Success Criteria

The Identity & Ownership Model is considered complete when:

```text
Every User Has Exactly One Role
Every Resource Has Defined Ownership
Every Resource Has Defined Visibility
Assignment Rules Are Explicit
Authentication Can Resolve Identity
Authorization Can Resolve Access Rights
Audit Logging Can Trace Resource Actions
```
