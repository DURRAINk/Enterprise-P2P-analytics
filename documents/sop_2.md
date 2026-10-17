## Standard Operating Procedure (SOP): End-to-End Procure-to-Pay (P2P) Lifecycle

**SOP ID:** SOP-FIN-P2P-002

**Version:** 1.0

**Effective Date:** October 2026

**Departments Involved:** Requesting Department, Procurement, Warehouse/Logistics, Accounts Payable (AP), and Finance

---

### 1. Purpose & Scope

This Standard Operating Procedure (SOP) defines the formal multi-departmental workflow for the corporate Procure-to-Pay (P2P) lifecycle. It outlines the operational handoffs, role accountabilities, system data capture points, and APQC standard alignments from initial purchase requisition through final vendor payment disbursement.Relevant process fields are mapped to a ready-made Purchase Orders & Supplier Performance dataset and documented as System Data Captured throughout the workflow for analysis and Dashboard creation.

---

### 2. Operational Process Flow & Step-by-Step Instructions

| Step | Phase | APQC Code & ID | Responsible Role | Operational Instructions | System Data Captured | Target SLA |
|------|-------|----------------|------------------|--------------------------|---------------------|------------|
| **1.0** | Clarify Requirements | `4.2.1.2` *(10282)* | Requesting Department | Clarify purchasing plans and refine initial requirements. | `Department`, `Cost_Centre`, `Requestor_Name`, `Category`, `Sub_Category`, `Item_Code`, `Item_Description`, `Quantity`, `Budget_Unit_Price`, `Budget_Total` | ≤ 4 hours |
| **1.1** | Contingency Planning | `2.4.1.3` *(10283)* | Requesting Department | Establish material contingency plans for critical items. | `Supplier_Tier`, `Supplier_Risk`, `Supplier_Status`, `Supplier_ESG_Score`, `Single_Source_Flag`, `Preferred_Supplier`, `Local_International` | ≤ 8 hours |
| **2.0** | PR Approval & Gateway | `4.2.4.2` *(10293)* | Requesting Department & Procurement | Analyze spend profile (Gateway: Amount > $10k?). Auto-approve if ≤ $10,000; route to manager manual review if > $10,000. | `Budget_Total`, `Line_Net`, `Line_Total_Gross`, `Line_Total_Inc_Tax`, `Savings_Amount`, `Savings_Pct` | ≤ 4 hours |
| **3.0** | Supplier Selection & PO | `4.2.4.4` *(10295)* | Procurement / Buyer | Select suppliers, maintain contracts (`4.2.3`), and create/distribute purchase orders to the supplier pool. | `PO_Number`, `PO_Date`, `PO_Type`, `PO_Status`, `Supplier_ID`, `Supplier_Name`, `Supplier_Country`, `Supplier_Region`, `Contract_ID`, `Contract_Type`, `Contract_Start`, `Contract_End`, `Payment_Terms`, `Approver_Name` | ≤ 2 hours |
| **4.0** | Inbound Logistics | `4.4.2.1` *(1039)* | Warehouse & Logistics Planner | Plan inbound material receipts and monitor supplier delivery performance. | `Supplier_ID`, `Supplier_Name`, `Requested_Delivery`, `Lead_Time_Days`, `Supplier_Risk` | $\le 24 \text{ hours}$ prior to arrival |   
| **5.0** | Goods Receipt (GR) | `4.4.3.2` *(10354)* | Warehouse Clerk | Receive, inspect, and store inbound deliveries upon physical goods arrival. | `Actual_Delivery`, `Requested_Delivery`, `Days_Late`, `On_Time_Delivery`, `Quantity`, `Unit_of_Measure` | $\le 24 \text{ hours}$ of receipt |
| **6.0** | AP Verification | `9.6.1.1` *(10869)* | Accounts Payable | Verify AP pay file with purchase order and vendor master file. | `PO_Number`, `Supplier_ID`, `Supplier_Name`, `Payment_Terms`, `Currency`, `Line_Total_Inc_Tax` | $\le 24 \text{ hours}$ of entry |
| **7.0** | Invoice Audit (3-Way Match) | `9.6.1.3` *(10871)* | Accounts Payable / System | Audit invoices and execute automated 3-way match verifying price and quantity consistency.| `PO_Number`,`Invoice_Match_Type`, `Invoice_Status`,`Quantity`,`Unit_Price`,`Line_Net`,`Line_Total_Inc_Tax`,`Tax_Amount`,`Discount_Amount` | Automated |
| **7b** | Exception Handling *(Branch)* | `9.6.1.7` *(10875)* | AP Audit Lead | *If Match Fails:* Research and resolve payable exceptions before moving forward. | `Invoice_Status`,`Invoice_Match_Type`,`Supplier_ID`,`Supplier_Name`,`PO_Status` | $\le 48 \text{ hours}$ |
| **8.0** | Payment Approval | `9.6.1.4` *(10872)* | Finance Manager | Review matched batches and approve payments for financial disbursement. | `Approver_Name`,`Invoice_Status`,`Payment_Status`,`Line_Total_Inc_Tax`,`Payment_Terms` | $\le 24 \text{ hours}$ post-match |
| **9.0** | Payment Disbursement | `9.6.1.8` *(10876)* | Accounts Payable / Finance | Process payments and execute final payout to the vendor. | `Supplier_ID`, `Supplier_Name`,`Payment_Status`,`Payment_Terms`, `Currency`, `Line_Total_Inc_Tax` | Vendor Net Terms |

---
### 3. Key Performance Indicators (KPIs) & Controls

* **Procurement Cycle Time:** $\le 3 \text{ business days}$ from Requisition submission to PO distribution.
* **3-Way Match Automation Rate:** Target $\ge 85\%$ straight-through processing without manual exception handling.
* **Early Payment Discount Capture:** Maximize capture of available vendor cash discounts (e.g., 2/10 Net 30) by ensuring prompt invoice auditing.