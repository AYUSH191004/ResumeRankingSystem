# Audit Logging Specification

Version: 1.0

Status: Approved Target Architecture

Document Type: Audit & Activity Logging Governance Specification

Owner: Platform Engineering

Audience:

* Backend Engineers
* Security Engineers
* DevOps Engineers
* Platform Architects
* Compliance Teams
* QA Engineers
* Incident Response Teams

---

# 1. Purpose

This document defines the audit logging standards for the ATS platform.

The audit logging framework exists to provide:

* Traceability
* Accountability
* Security Monitoring
* Compliance Support
* Operational Visibility
* Incident Investigation
* Forensic Analysis

Audit logs are considered business records and must be treated as immutable system artifacts.

---

# 2. Design Principles

The audit system must satisfy:

```text
Traceability
Integrity
Immutability
Consistency
Non-Repudiation
Observability
```

Audit logs must answer:

```text
Who performed an action?
What action occurred?
Which resource was affected?
When did it happen?
Where did it originate?
What was the outcome?
```

---

# 3. Logging Categories

The platform maintains three distinct logging layers.

## Application Logs

Purpose:

```text
Debugging
Operational Monitoring
Performance Analysis
```

Retention:

```text
30 Days
```

---

## Audit Logs

Purpose:

```text
Security
Compliance
Business Traceability
```

Retention:

```text
7 Years
```

Minimum.

---

## Security Logs

Purpose:

```text
Authentication
Authorization
Threat Detection
Incident Response
```

Retention:

```text
7 Years
```

Minimum.

---

# 4. Audit Event Model

Every audit event must contain:

| Field         | Required |
| ------------- | -------- |
| event_id      | Yes      |
| timestamp     | Yes      |
| actor_id      | Yes      |
| actor_role    | Yes      |
| action        | Yes      |
| resource_type | Yes      |
| resource_id   | Yes      |
| outcome       | Yes      |
| request_id    | Yes      |

---

# 5. Standard Audit Event Format

```json
{
  "event_id": "evt_123",
  "timestamp": "2026-06-02T12:00:00Z",
  "actor_id": 15,
  "actor_role": "admin",
  "action": "JOB_CREATED",
  "resource_type": "job",
  "resource_id": 100,
  "outcome": "SUCCESS",
  "request_id": "req_123"
}
```

---

# 6. Actor Information

Every audit record must identify:

| Field       | Description           |
| ----------- | --------------------- |
| actor_id    | User Identifier       |
| actor_role  | User Role             |
| actor_email | User Email (Optional) |

---

## Supported Roles

```text
candidate
recruiter
admin
system
```

---

# 7. Resource Identification

Every audit event must reference:

| Field         | Description         |
| ------------- | ------------------- |
| resource_type | Resource Category   |
| resource_id   | Resource Identifier |

---

## Supported Resource Types

```text
resume
job
match_result
ranking
analytics
user
assignment
authentication
system
```

---

# 8. Outcome Standards

Every event must have a final outcome.

Allowed Values:

```text
SUCCESS
FAILURE
DENIED
PARTIAL_SUCCESS
```

---

# 9. Request Correlation

Every audit event must include:

```text
request_id
```

Purpose:

```text
Trace API Request
Correlate Logs
Investigate Incidents
```

---

# 10. Authentication Audit Events

The following events are mandatory.

---

## LOGIN_SUCCESS

Triggered when:

```text
User Successfully Authenticates
```

---

## LOGIN_FAILED

Triggered when:

```text
Authentication Fails
```

---

## LOGOUT

Triggered when:

```text
User Session Ends
```

---

## TOKEN_REFRESH

Triggered when:

```text
Refresh Token Is Used
```

---

## ACCOUNT_LOCKED

Triggered when:

```text
Account Lockout Occurs
```

---

## ACCOUNT_SUSPENDED

Triggered when:

```text
Administrative Suspension Occurs
```

---

# 11. Authorization Audit Events

---

## ACCESS_GRANTED

Triggered when:

```text
Protected Resource Access Allowed
```

---

## ACCESS_DENIED

Triggered when:

```text
Permission Check Fails
```

---

## RESOURCE_ACCESS_DENIED

Triggered when:

```text
Ownership Or Assignment Rules Fail
```

---

# 12. Resume Audit Events

---

## RESUME_UPLOADED

Triggered when:

```text
Resume Successfully Uploaded
```

---

## RESUME_UPDATED

Triggered when:

```text
Resume Modified
```

---

## RESUME_VIEWED

Triggered when:

```text
Resume Accessed
```

---

## RESUME_DELETED

Triggered when:

```text
Resume Removed
```

---

## RESUME_PARSE_FAILED

Triggered when:

```text
Resume Processing Fails
```

---

# 13. Job Audit Events

---

## JOB_CREATED

Triggered when:

```text
Job Created
```

---

## JOB_UPDATED

Triggered when:

```text
Job Modified
```

---

## JOB_ARCHIVED

Triggered when:

```text
Job Archived
```

---

## JOB_VIEWED

Triggered when:

```text
Job Accessed
```

---

# 14. Recruiter Assignment Events

---

## RECRUITER_ASSIGNED

Triggered when:

```text
Recruiter Assigned To Job
```

---

## RECRUITER_UNASSIGNED

Triggered when:

```text
Recruiter Removed From Job
```

---

## ASSIGNMENT_UPDATED

Triggered when:

```text
Assignment Modified
```

---

# 15. Matching Audit Events

---

## MATCH_GENERATED

Triggered when:

```text
Match Computation Completes
```

---

## MATCH_RECOMPUTED

Triggered when:

```text
Manual Re-Match Triggered
```

---

## MATCH_FAILED

Triggered when:

```text
Matching Pipeline Fails
```

---

# 16. Ranking Audit Events

---

## RANKING_VIEWED

Triggered when:

```text
Candidate Ranking Retrieved
```

---

## SHORTLIST_GENERATED

Triggered when:

```text
Shortlist Produced
```

---

# 17. Analytics Audit Events

---

## ANALYTICS_VIEWED

Triggered when:

```text
Analytics Endpoint Accessed
```

---

## REPORT_EXPORTED

Triggered when:

```text
Analytics Export Generated
```

---

# 18. User Administration Events

---

## USER_CREATED

Triggered when:

```text
New User Created
```

---

## USER_UPDATED

Triggered when:

```text
User Modified
```

---

## USER_DEACTIVATED

Triggered when:

```text
User Disabled
```

---

## ROLE_CHANGED

Triggered when:

```text
User Role Modified
```

---

# 19. System Events

---

## APPLICATION_STARTED

Triggered when:

```text
Application Startup Completes
```

---

## APPLICATION_STOPPED

Triggered when:

```text
Application Shutdown Begins
```

---

## DATABASE_FAILURE

Triggered when:

```text
Database Unavailable
```

---

## MODEL_LOAD_FAILED

Triggered when:

```text
Embedding Model Fails To Initialize
```

---

# 20. Audit Data Classification

Audit logs contain:

```text
Sensitive Operational Data
```

Audit logs must never be publicly exposed.

---

## Restricted Fields

Never log:

```text
Passwords
JWT Tokens
Refresh Tokens
API Secrets
Database Credentials
Private Keys
Session Secrets
```

---

# 21. PII Handling Rules

Allowed:

```text
User ID
Email
Role
Business Resource Identifiers
```

Avoid logging:

```text
Full Resume Content
Candidate Contact Information
Phone Numbers
Sensitive Parsed Data
```

unless explicitly required for compliance.

---

# 22. Log Storage Requirements

Audit logs must be:

```text
Immutable
Encrypted At Rest
Backed Up
Searchable
```

Recommended Storage:

```text
ELK Stack
OpenSearch
Cloud Logging Platform
SIEM Platform
```

---

# 23. Retention Policy

| Log Type         | Retention |
| ---------------- | --------- |
| Application Logs | 30 Days   |
| Security Logs    | 7 Years   |
| Audit Logs       | 7 Years   |

---

# 24. Audit Query Requirements

Security teams must be able to query:

```text
By User
By Role
By Resource
By Action
By Request ID
By Time Range
By Outcome
```

---

# 25. Monitoring Requirements

The following metrics must be available:

```text
Authentication Failures
Authorization Failures
Resume Upload Volume
Job Creation Volume
Assignment Changes
Matching Failures
Analytics Access Volume
```

---

# 26. Incident Response Support

Audit logs must support:

```text
Security Investigations
Compliance Reviews
Operational Root Cause Analysis
Forensic Investigations
```

Audit records must never be modified after creation.

---

# 27. Compliance Requirements

The audit system must support:

```text
Internal Security Reviews
External Audits
Operational Reviews
Compliance Reporting
```

without requiring application code changes.

---

# 28. OpenAPI Integration

Endpoints that create audit events should document:

```text
Generated Audit Events
```

Example:

```text
POST /jobs

Audit Events:
JOB_CREATED
```

---

# 29. Governance Rules

Every protected endpoint must generate:

```text
Authentication Event
Authorization Event
Business Activity Event
```

where applicable.

No critical business action may occur without an audit record.

---

# 30. Success Criteria

The Audit Logging Program is considered complete when:

```text
Every Sensitive Action Is Audited
Every Authentication Event Is Logged
Every Authorization Decision Is Traceable
Every Business Event Has An Audit Trail
Logs Are Immutable
Logs Are Searchable
Logs Support Incident Investigation
Logs Support Compliance Reviews
Request Correlation Exists Across Services
```
