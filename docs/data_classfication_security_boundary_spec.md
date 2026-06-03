# Data Classification & Security Boundary Specification

Version: 1.0

Status: Approved Target Architecture

Document Type: Data Governance & Security Classification Specification

Owner: Platform Engineering

Audience:

* Security Engineers
* Backend Engineers
* Platform Architects
* DevOps Engineers
* Compliance Teams
* QA Engineers
* Audit Teams

---

# 1. Purpose

This document defines the data classification framework and security boundaries for the ATS platform.

The objective is to establish:

* Data Classification Standards
* Security Boundaries
* Data Ownership Rules
* Storage Requirements
* Access Requirements
* Transmission Requirements
* Logging Restrictions
* Retention Requirements
* Compliance Controls

This document applies to all platform data.

---

# 2. Security Principles

The platform follows:

```text
Least Privilege
Need To Know
Zero Trust
Defense In Depth
Data Minimization
Secure By Default
```

Every data element must have:

```text
Classification
Owner
Retention Policy
Access Rules
Storage Rules
Transmission Rules
```

---

# 3. Classification Framework

The platform uses four classification levels.

```text
PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED
```

Each level introduces stricter controls.

---

# 4. Classification Hierarchy

```text
RESTRICTED
     │
CONFIDENTIAL
     │
INTERNAL
     │
PUBLIC
```

Higher classifications inherit controls from lower classifications.

---

# 5. Public Data

## Definition

Data approved for unrestricted exposure.

Unauthorized disclosure causes:

```text
Minimal Risk
```

---

## Examples

```text
API Documentation
Health Endpoint Status
Public Product Information
System Version Information
```

---

## Access Rules

| Actor     | Access |
| --------- | ------ |
| Candidate | Allow  |
| Recruiter | Allow  |
| Admin     | Allow  |
| Anonymous | Allow  |

---

## Storage Requirements

```text
Standard Storage Controls
```

---

## Encryption Requirements

```text
TLS In Transit
```

---

# 6. Internal Data

## Definition

Business operational information.

Unauthorized disclosure causes:

```text
Low To Moderate Risk
```

---

## Examples

```text
Job Titles
Job Descriptions
Required Skills
Analytics Aggregates
Operational Metrics
```

---

## Access Rules

| Actor     | Access  |
| --------- | ------- |
| Candidate | Limited |
| Recruiter | Allow   |
| Admin     | Allow   |
| Anonymous | Deny    |

---

## Storage Requirements

```text
Authenticated Access Required
```

---

## Encryption Requirements

```text
TLS In Transit
Encryption At Rest
```

---

# 7. Confidential Data

## Definition

Sensitive business or personal information.

Unauthorized disclosure causes:

```text
Business Risk
Privacy Risk
Regulatory Risk
```

---

## Examples

```text
Candidate Resume Content
Candidate Contact Information
Recruiter Information
User Accounts
Assignment Information
Match Scores
Ranking Results
Analytics Details
```

---

## Access Rules

| Actor     | Access             |
| --------- | ------------------ |
| Candidate | Own Data Only      |
| Recruiter | Business Need Only |
| Admin     | Allow              |
| Anonymous | Deny               |

---

## Storage Requirements

```text
Encrypted At Rest
Encrypted In Transit
Access Logging Required
```

---

## Audit Requirements

Mandatory.

Every access must be auditable.

---

# 8. Restricted Data

## Definition

Highly sensitive system or security information.

Unauthorized disclosure causes:

```text
Critical Security Risk
Platform Compromise
Compliance Violation
```

---

## Examples

```text
JWT Secrets
Private Keys
Refresh Tokens
Access Tokens
Database Credentials
Cloud Credentials
API Secrets
Encryption Keys
Internal Security Configurations
```

---

## Access Rules

| Actor     | Access     |
| --------- | ---------- |
| Candidate | Deny       |
| Recruiter | Deny       |
| Admin     | Restricted |
| System    | Allow      |

---

## Storage Requirements

```text
Secrets Management System
Encryption At Rest
Encryption In Transit
Rotation Policy
```

---

## Audit Requirements

Mandatory.

Every access must generate an audit record.

---

# 9. ATS Resource Classification Matrix

| Resource                      | Classification |
| ----------------------------- | -------------- |
| Resume Content                | Confidential   |
| Candidate Contact Information | Confidential   |
| Candidate Profile             | Confidential   |
| Job Description               | Internal       |
| Job Requirements              | Internal       |
| Match Score                   | Confidential   |
| Match Explanation             | Confidential   |
| Ranking Results               | Confidential   |
| Analytics Results             | Confidential   |
| Audit Logs                    | Confidential   |
| JWT Secret                    | Restricted     |
| Database Credentials          | Restricted     |
| Embedding Vector              | Restricted     |
| Parsed Resume Data            | Restricted     |
| File Storage Path             | Restricted     |

---

# 10. Candidate Data Boundary

## Data Owner

```text
Candidate
```

---

## Protected Assets

```text
Resume
Email
Phone
Address
Work History
Education
Skills
Parsed Data
```

---

## Allowed Consumers

```text
Candidate
Authorized Recruiters
Admins
System Services
```

---

## Prohibited Access

```text
Other Candidates
Unauthenticated Users
External Services Without Approval
```

---

# 11. Recruiter Data Boundary

## Protected Assets

```text
Recruiter Profile
Assignment Information
Activity History
Performance Metrics
```

---

## Allowed Consumers

```text
Recruiter
Admin
Authorized System Components
```

---

# 12. Job Data Boundary

## Owner

```text
Admin/System
```

---

## Classification

```text
Internal
```

---

## Consumers

```text
Recruiters
Admins
Authorized Services
```

---

## Candidate Visibility

Denied by default.

---

# 13. Matching Data Boundary

## Protected Assets

```text
Match Scores
Ranking Outputs
Explanations
Matching Metadata
```

---

## Classification

```text
Confidential
```

---

## Consumers

```text
Recruiters
Admins
Authorized System Components
```

---

## Candidate Access

Explicitly Denied.

Reason:

```text
Internal Decision Support Artifact
```

---

# 14. Analytics Data Boundary

## Protected Assets

```text
Pool Quality
Ranking Trends
Hiring Insights
Recruiter Analytics
```

---

## Classification

```text
Confidential
```

---

## Consumers

```text
Recruiters
Admins
```

---

# 15. Security Secrets Boundary

The following data must never leave secure secret storage.

```text
JWT Signing Keys
Database Credentials
Encryption Keys
Cloud Access Keys
API Secrets
Service Credentials
```

---

## Storage Requirements

Approved:

```text
AWS Secrets Manager
Azure Key Vault
Hashicorp Vault
GCP Secret Manager
```

---

## Prohibited

```text
Source Code
Git Repositories
Environment Files In Production
Application Logs
```

---

# 16. Logging Restrictions

The following data must never be logged.

```text
Passwords
JWT Tokens
Refresh Tokens
Private Keys
Database Passwords
Access Tokens
API Keys
Encryption Keys
```

---

## Resume Logging Restrictions

Never log:

```text
Full Resume Content
Candidate Contact Information
Phone Numbers
Addresses
```

Allowed:

```text
Resume ID
Processing Status
Metadata
```

---

# 17. API Exposure Rules

Public APIs must never expose:

```text
Embedding Vectors
Parsed Resume Internals
Database Identifiers
Internal File Paths
System Configuration
Secrets
```

---

## Allowed Exposure

Only schema-approved fields defined in:

```text
01_API_Inventory_Specification.md
```

---

# 18. Database Security Requirements

Mandatory:

```text
Encryption At Rest
Encrypted Backups
Role-Based Access
Least Privilege
Audit Logging
```

---

## Database Access

Direct database access limited to:

```text
Authorized Administrators
Platform Services
Migration Services
```

---

# 19. Storage Security Requirements

All uploaded resumes must:

```text
Be Stored Outside Public Directories
Use Access Controls
Support Audit Logging
Support Backup Policies
```

---

## File Storage

Allowed:

```text
Private Object Storage
Encrypted Storage Volumes
```

Forbidden:

```text
Public File Hosting
Unrestricted Downloads
```

---

# 20. Network Security Boundaries

Mandatory:

```text
TLS 1.2+
HTTPS Only
Secure Service Communication
```

---

## Forbidden

```text
Plain HTTP
Unencrypted Service Calls
Unencrypted Credential Transmission
```

---

# 21. Data Retention Policy

| Data Type        | Retention                 |
| ---------------- | ------------------------- |
| Audit Logs       | 7 Years                   |
| Security Logs    | 7 Years                   |
| Application Logs | 30 Days                   |
| Resume Data      | Business Retention Policy |
| Analytics Data   | Business Retention Policy |
| Match Data       | Business Retention Policy |

---

# 22. Data Deletion Policy

Data deletion must:

```text
Be Auditable
Be Authorized
Be Traceable
```

---

## Required Audit Events

```text
DATA_DELETED
USER_DELETED
RESUME_DELETED
PURGE_COMPLETED
```

---

# 23. Data Sharing Rules

Data may only be shared when:

```text
Business Need Exists
Authorization Exists
Audit Trail Exists
```

---

## Forbidden Sharing

```text
Resume Data To Unauthorized Users
Match Scores To Candidates
Secrets To External Systems
Confidential Data Without Approval
```

---

# 24. Third-Party Integration Requirements

Third-party systems must:

```text
Use TLS
Support Authentication
Support Audit Logging
Use Approved Contracts
```

---

## Data Minimization

Third parties receive:

```text
Minimum Required Data Only
```

---

# 25. Compliance Requirements

The platform must support:

```text
Data Governance Reviews
Security Audits
Compliance Audits
Privacy Reviews
Internal Risk Reviews
```

---

# 26. Security Monitoring Requirements

The following must be monitored:

```text
Unauthorized Access Attempts
Privilege Escalation Attempts
Secret Access
Data Export Activity
Authentication Failures
Authorization Failures
```

---

# 27. Incident Response Requirements

The platform must support:

```text
Security Investigation
Forensic Analysis
Breach Investigation
Access Reconstruction
```

using:

```text
Audit Logs
Security Logs
Access Logs
```

---

# 28. Governance Rules

Every data element must have:

```text
Classification
Owner
Access Policy
Retention Policy
Storage Policy
```

No data may exist without classification.

---

# 29. Compliance Matrix

| Requirement           | Mandatory |
| --------------------- | --------- |
| Data Classification   | Yes       |
| Encryption At Rest    | Yes       |
| Encryption In Transit | Yes       |
| Audit Logging         | Yes       |
| Access Control        | Yes       |
| Secret Management     | Yes       |
| Retention Policy      | Yes       |
| Security Monitoring   | Yes       |

---

# 30. Success Criteria

The Data Classification & Security Boundary Program is complete when:

```text
Every Data Element Has A Classification
Every Sensitive Asset Has Access Controls
Every Secret Uses Secret Management
Every Access Is Auditable
Sensitive Data Is Encrypted
Unauthorized Data Exposure Is Prevented
Compliance Reviews Can Be Performed
Incident Investigations Are Supported
Security Boundaries Are Enforced
```
