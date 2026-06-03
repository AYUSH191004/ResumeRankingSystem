# Authentication Contract Specification

Version: 1.0

Status: Approved Target Architecture

Scope:

ATS Platform

Audience:

* Backend Engineers
* Frontend Engineers
* QA Engineers
* DevOps Engineers
* Security Reviewers
* Platform Governance

---

# 1. Purpose

This document defines the authentication architecture for the ATS platform.

The authentication contract establishes:

* Identity model
* User session model
* JWT contract
* Authentication boundaries
* Current user resolution
* Security requirements
* Token lifecycle

This document does not define permissions.

Permissions are governed by the Authorization & Resource Access Specification.

---

# 2. Authentication Principles

The platform follows:

```text
Identity First
Authentication Second
Authorization Third
```

Authentication answers:

```text
Who is the user?
```

Authorization answers:

```text
What may the user do?
```

These concerns must remain separate.

---

# 3. Authentication Architecture

Authentication Strategy:

```text
JWT Bearer Authentication
```

Transport:

```http
Authorization: Bearer <access_token>
```

Identity Source:

```text
Signed JWT Access Token
```

Trust Boundary:

```text
Backend API validates token.
Backend API never trusts client supplied identity.
```

Examples:

Forbidden:

```http
POST /resume/upload?user_id=5
```

Forbidden:

```json
{
  "user_id": 5
}
```

Allowed:

```http
Authorization: Bearer eyJ...
```

Identity is resolved from token claims.

---

# 4. User Identity Model

## User

Every authenticated actor is a User.

Core Identity Fields:

| Field     | Type    |
| --------- | ------- |
| user_id   | integer |
| email     | string  |
| role      | enum    |
| is_active | boolean |

---

# 5. Role Model

Supported Roles:

```text
candidate
recruiter
admin
```

## Candidate

Purpose:

```text
Resume owner
```

Capabilities:

```text
Resume management
```

---

## Recruiter

Purpose:

```text
Candidate evaluation
Job execution
Analytics consumption
```

Capabilities:

```text
View jobs
View rankings
View analytics
```

---

## Admin

Purpose:

```text
Platform management
```

Capabilities:

```text
User management
Job creation
Recruiter assignment
Platform administration
```

---

# 6. JWT Contract

JWT Type:

```text
Access Token
```

Algorithm:

```text
RS256 (Preferred)
```

Fallback:

```text
HS256
```

Only for non-production environments.

---

# 7. JWT Claims

Required Claims

| Claim | Required | Purpose          |
| ----- | -------- | ---------------- |
| sub   | Yes      | User Identifier  |
| email | Yes      | User Email       |
| role  | Yes      | User Role        |
| iat   | Yes      | Issued At        |
| exp   | Yes      | Expiration       |
| jti   | Yes      | Token Identifier |

Example:

```json
{
  "sub": "123",
  "email": "user@company.com",
  "role": "recruiter",
  "iat": 1730000000,
  "exp": 1730003600,
  "jti": "4fd0c0c5-0f7e-4d08-b8e9-fdb26fcbca21"
}
```

---

# 8. Access Token Policy

Lifetime:

```text
15 Minutes
```

Purpose:

```text
API Access
```

Storage:

```text
Memory Preferred
HttpOnly Cookie Allowed
```

Never:

```text
Local Storage
Session Storage
```

for enterprise production environments.

---

# 9. Refresh Token Policy

Lifetime:

```text
30 Days
```

Purpose:

```text
Session Renewal
```

Storage:

```text
HttpOnly Secure Cookie
```

Required:

```text
Token Rotation
```

Every refresh generates:

```text
New Access Token
New Refresh Token
```

---

# 10. Authentication Endpoints

## Login

Method:

```http
POST /auth/login
```

Purpose:

```text
Authenticate user
```

Request:

```json
{
  "email": "user@company.com",
  "password": "********"
}
```

Response:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "Bearer",
  "expires_in": 900
}
```

---

## Refresh Token

Method:

```http
POST /auth/refresh
```

Purpose:

```text
Renew session
```

Response:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "Bearer",
  "expires_in": 900
}
```

---

## Logout

Method:

```http
POST /auth/logout
```

Purpose:

```text
Terminate session
```

Behavior:

```text
Invalidate refresh token
```

Response:

```json
{
  "message": "logout successful"
}
```

---

## Current User

Method:

```http
GET /auth/me
```

Purpose:

```text
Resolve authenticated identity
```

Response:

```json
{
  "user_id": 123,
  "email": "user@company.com",
  "role": "recruiter"
}
```

---

# 11. Current User Dependency

Every business endpoint must resolve identity through:

```python
current_user
```

Example:

```python
current_user: User = Depends(get_current_user)
```

Prohibited:

```python
user_id: int
recruiter_id: int
```

inside request payloads.

Identity originates from authentication only.

---

# 12. Protected API Surface

Authentication Required:

```text
/resume/*
/jobs/*
/match/*
/analytics/*
```

Authentication Not Required:

```text
/health
/docs
/openapi.json
```

---

# 13. Account State Rules

User States:

```text
active
inactive
locked
suspended
```

Only:

```text
active
```

may authenticate.

---

# 14. Password Policy

Minimum Length:

```text
12 Characters
```

Requirements:

```text
Uppercase
Lowercase
Number
Special Character
```

Passwords:

```text
Never Logged
Never Returned
Never Stored Plaintext
```

Hashing:

```text
Argon2id (Preferred)
```

Fallback:

```text
bcrypt
```

---

# 15. Security Controls

Mandatory:

```text
HTTPS Only
JWT Signature Validation
Token Expiration Validation
Role Validation
Account State Validation
```

---

# 16. Audit Requirements

Authentication Events:

```text
LOGIN_SUCCESS
LOGIN_FAILED
TOKEN_REFRESH
LOGOUT
ACCOUNT_LOCKED
```

Must be logged.

---

# 17. Authentication Failure Contract

Invalid Token:

```json
{
  "error": {
    "code": "AUTH_INVALID_TOKEN",
    "message": "Token is invalid"
  }
}
```

Expired Token:

```json
{
  "error": {
    "code": "AUTH_TOKEN_EXPIRED",
    "message": "Token has expired"
  }
}
```

Inactive User:

```json
{
  "error": {
    "code": "AUTH_USER_INACTIVE",
    "message": "User account inactive"
  }
}
```

---

# 18. Future SSO Compatibility

The contract must support future integration with:

```text
Azure AD
Okta
Google Workspace
SAML
OIDC
```

without changing business APIs.

Authentication providers may change.

JWT identity contract must remain stable.

---

# 19. Governance Rules

Business services must never:

```text
Trust client supplied identity
Trust role values from request payloads
Trust recruiter_id parameters
Trust user_id parameters
```

Identity must always originate from:

```text
Validated JWT Claims
```

---

# 20. Success Criteria

Authentication Contract is considered complete when:

```text
Every business API resolves current_user.
No endpoint accepts user_id ownership fields.
JWT authentication protects all business APIs.
Role information is available for authorization checks.
Audit logs exist for authentication events.
Future SSO integration is possible without API redesign.
```
