# Authorization & Resource Access Specification

Purpose

This document defines:

* Roles
* Permissions
* Ownership Rules
* Resource Visibility Rules
* Access Enforcement Rules

It becomes the authoritative source for:

* Authentication implementation
* Authorization middleware
* Frontend permission handling
* QA security testing
* Audit logging

Scope

Resources:

* Resume
* Job
* MatchResult
* Ranking
* Analytics
* User Management

Actors:

* Candidate
* Recruiter
* Admin

Ownership Model

## Resume

Owner:

Candidate

Visibility:

* Owner Candidate
* Recruiters
* Admins

Modification:

* Owner Candidate
* Admin

## Job

Owner:

Admin/System

Assignment:

One or more Recruiters

Visibility:

* Recruiters
* Admins

Modification:

* Assigned Recruiters
* Admins

## MatchResult

Owner:

System

Visibility:

* Recruiters
* Admins

Candidate Access:

Denied

## Analytics

Owner:

System

Visibility:

* Recruiters
* Admins

Candidate Access:

Denied

Permission Matrix

| Action                | Candidate | Recruiter     | Admin |
| --------------------- | --------- | ------------- | ----- |
| Upload Resume         | Allow     | Deny          | Deny  |
| Update Own Resume     | Allow     | Deny          | Allow |
| View Own Resume       | Allow     | Deny          | Allow |
| View Candidate Resume | Deny      | Allow         | Allow |
| Create Job            | Deny      | Deny          | Allow |
| Edit Job              | Deny      | Assigned Only | Allow |
| Archive Job           | Deny      | Assigned Only | Allow |
| View Job              | Deny      | Allow         | Allow |
| View Ranking          | Deny      | Allow         | Allow |
| View Analytics        | Deny      | Allow         | Allow |
| View Match Scores     | Deny      | Allow         | Allow |
| Trigger Re-Match      | Deny      | Assigned Only | Allow |
| Assign Recruiter      | Deny      | Deny          | Allow |
| Manage Users          | Deny      | Deny          | Allow |

Enforcement Rules

All business APIs must:

1. Authenticate user.
2. Resolve role.
3. Resolve ownership.
4. Evaluate permissions.
5. Log access decision.

Default Rule

Any permission not explicitly granted is denied.
