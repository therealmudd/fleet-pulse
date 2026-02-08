# 📘 FleetPulse — Starter User Stories

## EPIC 1: Authentication & Access Control

### US-001: User can authenticate

**As a** system user
**I want** to log in using secure credentials
**So that** I can access features based on my role

**Acceptance Criteria**

* Login returns a JWT
* Token includes user role
* Invalid credentials are rejected
* Token expiration is enforced

---

### US-002: Role-based access control

**As a** system administrator
**I want** actions to be restricted by role
**So that** users only access what they’re allowed to

**Acceptance Criteria**

* Drivers cannot access admin endpoints
* Dispatchers cannot manage system settings
* Admin can access all endpoints
* Unauthorized requests return appropriate HTTP status

---

## EPIC 2: Driver Management

### US-003: Admin can create a driver

**As an** admin
**I want** to create a driver profile
**So that** they can receive delivery jobs

**Acceptance Criteria**

* Driver includes name, contact info, vehicle type
* Driver starts in OFFLINE state
* Duplicate drivers are prevented

---

### US-004: Driver can update availability

**As a** driver
**I want** to mark myself AVAILABLE or OFFLINE
**So that** I only receive jobs when I can work

**Acceptance Criteria**

* Only the driver can update their own availability
* Driver cannot go AVAILABLE if suspended
* Availability changes are timestamped

🔥 Teaching hook: *Who is allowed to change what, and why?*

---

## EPIC 3: Job Creation & Viewing

### US-005: Dispatcher can create a job

**As a** dispatcher
**I want** to create a delivery job
**So that** it can be assigned to a driver

**Acceptance Criteria**

* Job includes pickup, drop-off, deadline, vehicle type
* Job starts in CREATED status
* Invalid deadlines are rejected

---

### US-006: Driver can view assigned jobs

**As a** driver
**I want** to see my assigned jobs
**So that** I know what I’m responsible for

**Acceptance Criteria**

* Drivers only see their own jobs
* Jobs are ordered by deadline
* Job status is clearly visible

---

## EPIC 4: Job Assignment

### US-007: System auto-assigns a job

**As the** system
**I want** to automatically assign jobs
**So that** dispatchers don’t have to do it manually

**Acceptance Criteria**

* Only AVAILABLE drivers are considered
* Vehicle type must match
* Job is assigned to exactly one driver
* Assignment is recorded with type AUTO

🔥 Teaching hook: *What happens if assignment fails halfway?*

---

### US-008: Dispatcher manually assigns a job

**As a** dispatcher
**I want** to assign a job to a specific driver
**So that** I can override automation when needed

**Acceptance Criteria**

* Manual assignment bypasses auto rules
* Previous assignments are invalidated
* Assignment type is MANUAL
* Override is audit-logged

---

## EPIC 5: Assignment Acceptance Flow

### US-009: Driver accepts an assigned job

**As a** driver
**I want** to accept a job
**So that** I can begin work

**Acceptance Criteria**

* Job moves to ACCEPTED state
* Driver status changes to ON_JOB
* Acceptance after expiration is rejected
* Action is idempotent

🔥 Teaching hook: *Why idempotency matters in mobile networks.*

---

### US-010: Assignment expires if not accepted

**As the** system
**I want** to expire unaccepted assignments
**So that** jobs don’t get stuck

**Acceptance Criteria**

* Expiration occurs after X minutes
* Expired assignments trigger reassignment
* Expiration is audit-logged

---

## EPIC 6: Job Execution

### US-011: Driver starts a job

**As a** driver
**I want** to mark a job IN_PROGRESS
**So that** the system knows I’ve started delivery

**Acceptance Criteria**

* Only ACCEPTED jobs can be started
* Timestamp is recorded
* Invalid transitions are rejected

---

### US-012: Driver completes a job

**As a** driver
**I want** to mark a job DELIVERED
**So that** it can be closed

**Acceptance Criteria**

* Proof of delivery is required
* Completion timestamp is recorded
* Job cannot be modified after completion

---

## EPIC 7: Failure & Recovery

### US-013: Driver rejects a job

**As a** driver
**I want** to reject an assigned job
**So that** it can be reassigned

**Acceptance Criteria**

* Rejection reason is required
* Job returns to unassigned state
* Reassignment is triggered

---

### US-014: Dispatcher reassigns a job mid-flow

**As a** dispatcher
**I want** to reassign a job at any time
**So that** operations can continue smoothly

**Acceptance Criteria**

* Previous assignment is closed
* New assignment is created
* All actions are audit-logged

🔥 Teaching hook: *Consistency vs flexibility.*

---

## EPIC 8: Audit & Observability

### US-015: System records audit logs

**As an** admin
**I want** to see a history of important actions
**So that** I can investigate issues

**Acceptance Criteria**

* All state changes are logged
* Logs are immutable
* Logs include actor, timestamp, action, entity

---
