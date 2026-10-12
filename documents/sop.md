## Standard Operating Procedure (SOP): End-to-End Procure-to-Pay (P2P) Lifecycle

**SOP ID:** SOP-FIN-P2P-001

**Version:** 1.0

**Effective Date:** October 2026

**Departments Involved:** Requesting Department, Procurement, Warehouse/Logistics, Accounts Payable (AP), and Finance

---

### 1. Purpose & Scope

This Standard Operating Procedure (SOP) defines the formal multi-departmental workflow for the corporate Procure-to-Pay (P2P) lifecycle. It outlines the operational handoffs, role accountabilities, system data capture points, and APQC standard alignments from initial purchase requisition through final vendor payment disbursement.

---

### 2. Operational Process Flow & Step-by-Step Instructions

| Step | Phase | APQC Code & ID | Responsible Role | Operational Instructions | System Data Captured | Target SLA |
|------|-------|----------------|------------------|--------------------------|---------------------|------------|
| **1.0** | Clarify Requirements | `4.2.1.2` *(10282)* | Requesting Department | Clarify purchasing plans and refine initial requirements. | `Req_ID`, `Clarification_Timestamp` | ≤ 4 hours |
| **1.1** | Contingency Planning | `2.4.1.3` *(10283)* | Requesting Department | Establish material contingency plans for critical items. | `Plan_ID`, `Contingency_Flag` | ≤ 8 hours |
| **2.0** | PR Approval & Gateway | `4.2.4.2` *(10293)* | Requesting Department & Procurement | Analyze spend profile (Gateway: Amount > $10k?). Auto-approve if ≤ $10,000; route to manager manual review if > $10,000. | `Approval_Status`, `Approver_ID`, `Approval_Timestamp` | ≤ 4 hours |
| **3.0** | Supplier Selection & PO | `4.2.4.4` *(10295)* | Procurement / Buyer | Select suppliers, maintain contracts (`4.2.3`), and create/distribute purchase orders to the supplier pool. | `PO_ID`, `Vendor_ID`, `PO_Issue_Timestamp` | ≤ 2 hours |
| **4.0** | Inbound Logistics | `4.4.2.1` *(1039)* | Warehouse & Logistics Planner | Plan inbound material receipts and monitor supplier delivery performance. | `Shipment_ID`, `Expected_Arrival_Date` | $\le 24 \text{ hours}$ prior to arrival |   
| **5.0** | Goods Receipt (GR) | `4.4.3.2` *(10354)* | Warehouse Clerk | Receive, inspect, and store inbound deliveries upon physical goods arrival. | `GR_ID`, `Received_Qty`, `GR_Timestamp`| $\le 24 \text{ hours}$ of receipt |
| **6.0** | AP Verification | `9.6.1.1` *(10869)* | Accounts Payable | Verify AP pay file with purchase order and vendor master file. | `Invoice_ID`, `Billed_Amount`, `Invoice_Timestamp` | $\le 24 \text{ hours}$ of entry |
| **7.0** | Invoice Audit (3-Way Match) | `9.6.1.3` *(10871)* | Accounts Payable / System | Audit invoices and execute automated 3-way match verifying price and quantity consistency.| `Match_Status` (`Success` / `Mismatch`)  | Automated |
| **7b** | Exception Handling *(Branch)* | `9.6.1.7` *(10875)* | AP Audit Lead | *If Match Fails:* Research and resolve payable exceptions before moving forward. | `Exception_Flag`, `Resolution_Notes` | $\le 48 \text{ hours}$ |
| **8.0** | Payment Approval | `9.6.1.4` *(10872)* | Finance Manager | Review matched batches and approve payments for financial disbursement. | `Approval_Batch_ID`, `Signoff_Timestamp` | $\le 24 \text{ hours}$ post-match |
| **9.0** | Payment Disbursement | `9.6.1.8` *(10876)* | Accounts Payable / Finance | Process payments and execute final payout to the vendor. | `Payment_ID`, `Disbursement_Timestamp`| Vendor Net Terms |

---
### 3. Key Performance Indicators (KPIs) & Controls

* **Procurement Cycle Time:** $\le 3 \text{ business days}$ from Requisition submission to PO distribution.
* **3-Way Match Automation Rate:** Target $\ge 85\%$ straight-through processing without manual exception handling.
* **Early Payment Discount Capture:** Maximize capture of available vendor cash discounts (e.g., 2/10 Net 30) by ensuring prompt invoice auditing.