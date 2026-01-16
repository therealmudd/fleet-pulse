# 🚚 FleetPulse — Delivery Fleet Management API

**Version:** 1.0
**Client:** FleetPulse Logistics (Fictional)
**Audience:** Backend Engineering Team

---

## 1. 🎯 Problem Statement

FleetPulse Logistics operates a same-day delivery service.
Job assignments are currently handled manually via WhatsApp and spreadsheets, resulting in:

* Missed deadlines
* Double-assigned drivers
* No audit trail
* Poor visibility into delivery status

FleetPulse needs a backend system to:

* Manage drivers and delivery jobs
* Assign jobs efficiently
* Handle failures gracefully
* Provide accountability and traceability

---

## 2. 🧑‍💼 User Roles

### 2.1 Admin

* Full system access
* Can manage drivers, jobs, and settings
* Can override any automated decision

### 2.2 Dispatcher

* Can create and assign jobs
* Can manually reassign jobs
* Can view fleet status

### 2.3 Driver

* Can view assigned jobs
* Can accept / reject jobs
* Can update job status
* Can upload proof of delivery

---

## 3. 📦 Core Domain Concepts

### Driver

* Unique ID
* Name
* Contact details
* Current status:

  * OFFLINE
  * AVAILABLE
  * ON_JOB
  * SUSPENDED
* Availability window (time-based)
* Vehicle type
* Last known location (optional)
* Rating (calculated)

### Job

* Unique ID
* Pickup location
* Drop-off location
* Delivery deadline
* Required vehicle type
* Status:

  * CREATED
  * ASSIGNED
  * ACCEPTED
  * IN_PROGRESS
  * DELIVERED
  * FAILED
  * CANCELLED
* Assigned driver (optional)
* Payment amount
* Proof of delivery (optional)
* Failure reason (if applicable)

### Assignment

* Job ↔ Driver link
* Assignment timestamp
* Assignment type:

  * AUTO
  * MANUAL
* Status:

  * PENDING
  * ACCEPTED
  * REJECTED
  * EXPIRED

---

## 4. 🔄 Job Lifecycle

```
CREATED
  ↓
ASSIGNED
  ↓
ACCEPTED
  ↓
IN_PROGRESS
  ↓
DELIVERED
```

### Failure Paths

* Driver rejects → REASSIGN
* Driver goes offline → REASSIGN
* Deadline missed → FAILED
* Admin cancels → CANCELLED

---

## 5. ⚙️ Functional Requirements

### 5.1 Driver Management

* Create, update, suspend drivers
* Drivers can toggle availability
* System must prevent assignment to:

  * Offline drivers
  * Suspended drivers
  * Drivers without required vehicle type

---

### 5.2 Job Creation

* Dispatcher or Admin can create jobs
* Job must include:

  * Pickup & drop-off
  * Deadline
  * Vehicle requirement
* Jobs start in `CREATED` state

---

### 5.3 Auto-Assignment Engine

The system should attempt auto-assignment when:

* A job is created
* A driver becomes available
* A job is unassigned due to failure

#### Assignment Rules (Initial Version)

1. Driver must be AVAILABLE
2. Vehicle type must match
3. Driver must be within availability window
4. Earliest deadline jobs take priority
5. If multiple drivers qualify, choose the least recently assigned driver

> ⚠️ Auto-assignment is *best-effort*, not guaranteed.

---

### 5.4 Driver Acceptance Flow

* Driver receives assignment
* Driver has **X minutes** to accept
* If not accepted → assignment EXPIRES
* Expired assignments trigger reassignment

---

### 5.5 Manual Override

* Dispatcher can:

  * Assign job to specific driver
  * Reassign job at any time
* Manual assignments bypass auto rules
* Overrides must be logged

---

### 5.6 Job Execution

* Driver marks job:

  * IN_PROGRESS
  * DELIVERED
* Proof of delivery required for completion
* Delivery timestamp must be recorded

---

### 5.7 Failure Handling

System must handle:

* Driver rejection
* Driver offline mid-job
* Deadline exceeded
* Upload failure

Each failure must:

* Record a reason
* Be auditable
* Trigger appropriate reassignment if possible

---

## 6. 📂 File Uploads (Proof of Delivery)

* Drivers upload image or PDF
* Files must be linked to job
* File size limits apply
* Failed uploads must not corrupt job state

---

## 7. 🔐 Authentication & Authorization

* JWT-based auth
* Role-based access control
* Drivers can only see their own jobs
* Dispatchers can see all jobs
* Admin can do everything

---

## 8. 📊 Audit & Observability

System must record:

* Job state changes
* Assignment attempts
* Manual overrides
* Failures & retries

Audit logs must be:

* Immutable
* Time-stamped
* Queryable

---

## 9. ⚠️ Non-Functional Requirements

### Reliability

* Assignment operations must be idempotent
* Duplicate job creation must be prevented

### Performance

* System must support 1,000+ active jobs
* Assignment must complete within 2 seconds

### Consistency

* A job can never be assigned to more than one driver at a time

---

## 10. 🚧 Out of Scope (for v1)

* Real-time GPS tracking
* Payments processing
* Customer-facing UI
* Route optimization

---

## 11. 🧪 Suggested Edge Cases (Intentional Traps 😈)

* Two drivers accept the same job
* Driver accepts after expiration
* Dispatcher reassigns mid-acceptance
* Job deadline changes after assignment
* Proof uploaded twice
* Retry after partial failure

---

## 12. 📁 Suggested Repo Structure

```
/docs
  product_spec.md
  architecture.md
  assignment_rules.md
/src
  /auth
  /drivers
  /jobs
  /assignments
  /audit
/tests
```

---

## 13. 🧑‍🏫 Mentorship Teaching Hooks

Use this project to teach:

* Domain modeling
* State machines
* Race conditions
* Idempotency
* Separation of concerns
* Defensive programming
* “Real systems are messy”

---

## Next steps (I can do these for you)

* Turn this into **GitHub issues & milestones**
* Design the **database schema**
* Create a **sequence diagram for assignments**
* Propose a **clean architecture**
* Add “client chaos” change requests

Just say the word.
This is a *killer* mentoring project 👊
