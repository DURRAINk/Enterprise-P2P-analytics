## Standard Operating Procedure (SOP): Enterprise Procure-to-Pay (P2P) Lifecycle

**SOP ID:** SOP-FIN-P2P-001

**Version:** 1.0

**Effective Date:** October 2026

**Source Framework:** APQC PCF v8.0 / Lucidchart BPMN Architecture

**Departments Involved:** Requesting Department, Procurement, Warehouse & Inbound Logistics, Accounts Payable, Finance, and External Supplier Pool

---

### 1. Purpose & Scope

This Standard Operating Procedure (SOP) defines the comprehensive multi-departmental workflow for the corporate Procure-to-Pay (P2P) lifecycle. It outlines operational handoffs, role accountabilities, system data capture points, and APQC standard alignments from initial requirement planning and contingency setup through purchase order distribution, goods receipt, 3-way match auditing, and final vendor payment disbursement.

Additionally, this SOP establishes the foundational data schema required for generating synthetic event logs and conducting automated bottleneck analysis using Python (`pm4py`).

---

### 2. Departmental Swimlanes & Architecture

The workflow is distributed across three internal enterprise swimlanes and one external partner pool:

1. **Requesting Department & Procurement:** Manages initial requirement clarification, material contingency plans, spend analysis, requisition approvals, supplier selection, contract maintenance, and purchase order creation.


2. **Warehouse & Inbound Logistics:** Manages inbound material planning, dock scheduling, shipment tracking, and physical goods receipt/inspection.


3. **Accounts Payable & Finance:** Manages invoice receipt verification, vendor master validation, automated 3-way match execution, exception resolution, payment approvals, and final electronic disbursements.


4. **Supplier (External Pool):** Fulfills orders, delivers physical shipments, and submits billing invoices.



---

### 3. Step-by-Step Standard Operating Procedure Table

| Step | Phase / Stage | APQC Code & ID | Responsible Role | Operational Instructions | System Data Captured | Target SLA |
| --- | --- | --- | --- | --- | --- | --- |
| **1.0** | Clarify Requirements | `4.2.1.2` *(10282)* | Requesting Department | Clarify purchasing plans and refine initial project/operational material requirements. | `Req_ID`, `Clarification_Timestamp` | $\le 4 \text{ hours}$ |
| **1.1** | Contingency Planning | `2.4.1.3` *(10283)* | Requesting Department | Establish material contingency and back-up supply plans for critical items. | `Plan_ID`, `Contingency_Flag` | $\le 8 \text{ hours}$ |
| **2.0** | PR Approval & Gateway | `4.2.4.2` *(10293)* | Requesting Department & Procurement | Analyze spend profile (Gateway: Amount > $10k?). Auto-approve if $\le \$10,000$; route to manager manual review if $> \$10,000$. | `Approval_Status`, `Approver_ID`, `Approval_Timestamp` | $\le 4 \text{ hours}$ |
| **3.0** | Supplier Selection & PO | `4.2.4.4` *(10295)*<br> | Procurement / Buyer | Select qualified vendors, maintain contracts (`4.2.3`), and create/distribute purchase orders to the supplier pool. | `PO_ID`, `Vendor_ID`, `PO_Issue_Timestamp` | $\le 2 \text{ hours}$ |
| **4.0** | Inbound Logistics | `4.4.2.1` *(1039)* | Warehouse & Logistics Planner | Plan inbound material receipts and monitor supplier delivery performance against active commitments. | `Shipment_ID`, `Expected_Arrival_Date`<br> | $\le 24 \text{ hours}$ prior to arrival |
| **5.0** | Goods Receipt (GR) | `4.4.3.2` *(10354)*<br> | Warehouse Clerk | Receive physical delivery at the dock, inspect items for quality/quantity compliance, and log Goods Receipt. | `GR_ID`, `Received_Qty`, `GR_Timestamp` | $\le 24 \text{ hours}$ of receipt |
| **6.0** | AP Verification | `9.6.1.1` *(10869)* | Accounts Payable | Verify AP pay file parameters with purchase order and vendor master file records. | `Invoice_ID`, `Billed_Amount`, `Invoice_Timestamp` | $\le 24 \text{ hours}$ of entry |
| **7.0** | Invoice Audit (3-Way Match) | `9.6.1.3` *(10871)* | Accounts Payable / System | Execute automated 3-way match verifying price consistency ($\text{PO} = \text{Invoice}$) and quantity accuracy ($\text{GR} = \text{Billed}$). | `Match_Status` (`Success` / `Mismatch`) | Automated |
| **7b** | Exception Handling *(Branch)* | `9.6.1.7` *(10875)* | AP Audit Lead | *If Match Fails:* Place invoice on hold, flag variance, and research/resolve payable exceptions with procurement and vendor. | `Exception_Flag`, `Resolution_Notes` | $\le 48 \text{ hours}$ |
| **8.0** | Payment Approval | `9.6.1.4` *(10872)* | Finance Manager | Review matched invoice batches and execute final financial sign-off for disbursement authorization. | `Approval_Batch_ID`, `Signoff_Timestamp` | $\le 24 \text{ hours}$ post-match |
| **9.0** | Payment Disbursement | `9.6.1.8` *(10876)* | Accounts Payable / Finance | Execute final electronic fund transfer (ACH, EFT, or wire) to vendor based on agreed Net terms. | `Payment_ID`, `Disbursement_Timestamp` | Vendor Net Terms |

---

### 4. Synthetic Data Generation & Python (`pm4py`) Bottleneck Analysis

To evaluate operational efficiency and uncover throughput delays, the data attributes captured in this workflow are ingested into a Python process mining pipeline.

#### A. Synthetic Event Log Schema

The synthetic data generator maps cases across the process variants using these core headers:

* `Req_ID`, `Clarification_Timestamp`, `Plan_ID`, `Contingency_Flag`

* `Approval_Status`, `Approver_ID`, `Approval_Timestamp`

* `PO_ID`, `Vendor_ID`, `PO_Issue_Timestamp`

* `Shipment_ID`, `Expected_Arrival_Date`, `GR_ID`, `Received_Qty`, `GR_Timestamp`

* `Invoice_ID`, `Billed_Amount`, `Invoice_Timestamp`, `Match_Status`

* `Exception_Flag`, `Resolution_Notes`

* `Approval_Batch_ID`, `Signoff_Timestamp`, `Payment_ID`, `Disbursement_Timestamp`


#### B. Process Mining Implementation (`pm4py`)

Using `pm4py`, the synthetic event log is formatted into standard process mining parameters (`case:concept:name`, `concept:name`, and `time:timestamp`) to execute:

1. **Process Discovery:** Automatically mining the event log to construct a Directly-Follows Graph (DFG) validating adherence to the APQC-aligned BPMN flow.
2. **Bottleneck Detection:** Calculating average waiting times and transition durations between handoffs (specifically highlighting delays during manual manager reviews and exception handling queues like step `9.6.1.7`).
3. **Performance Spectrum Analysis:** Quantifying throughput bottlenecks across procurement and accounts payable to verify performance against target SLAs.