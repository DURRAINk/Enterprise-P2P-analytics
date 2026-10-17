import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

NUM_CASES = 10000

vendors = [f"VEN{str(i).zfill(4)}" for i in range(1, 101)]
approvers = [f"APR{str(i).zfill(3)}" for i in range(1, 21)]

event_log = []
transactions = []

for i in range(1, NUM_CASES + 1):

    # -----------------------------
    # Master identifiers
    # -----------------------------

    case_id = f"CASE{i:06d}"
    req_id = f"REQ{i:06d}"
    plan_id = f"PLAN{i:06d}"
    po_id = f"PO{i:06d}"
    shipment_id = f"SHP{i:06d}"
    gr_id = f"GR{i:06d}"
    invoice_id = f"INV{i:06d}"
    payment_id = f"PAY{i:06d}"

    vendor_id = random.choice(vendors)
    approver_id = random.choice(approvers)

    # -----------------------------
    # Commercial values
    # -----------------------------

    amount = round(
        np.random.lognormal(mean=9.5, sigma=0.8),
        2
    )

    billed_amount = round(
        amount * random.uniform(0.97, 1.03),
        2
    )

    contingency_flag = random.choice(
        ["Yes", "No"]
    )

    approval_status = random.choices(
        ["Approved", "Rejected"],
        weights=[95, 5]
    )[0]

    match_status = random.choices(
        ["Matched", "Mismatch"],
        weights=[90, 10]
    )[0]

    exception_flag = (
        "Yes"
        if match_status == "Mismatch"
        else "No"
    )

    resolution_notes = (
        fake.sentence()
        if exception_flag == "Yes"
        else "None"
    )

    approval_batch_id = (
        f"BATCH{random.randint(1,100):03d}"
    )

    received_qty = random.randint(1, 500)

    # -----------------------------
    # Timeline generation
    # -----------------------------

    start_ts = fake.date_time_between(
        start_date="-2y",
        end_date="now"
    )

    clarification_ts = start_ts + timedelta(
        hours=random.randint(1, 24)
    )

    approval_delay = random.randint(2, 48)

    # Inject approval bottleneck
    if random.random() < 0.20:
        approval_delay += random.randint(
            72,
            240
        )

    approval_ts = clarification_ts + timedelta(
        hours=approval_delay
    )

    po_issue_ts = approval_ts + timedelta(
        hours=random.randint(1, 12)
    )

    expected_arrival_date = (
        po_issue_ts +
        timedelta(days=random.randint(3, 20))
    )

    goods_delay = random.randint(0, 5)

    # Inject logistics bottleneck
    if random.random() < 0.15:
        goods_delay += random.randint(
            5,
            15
        )

    gr_timestamp = (
        expected_arrival_date +
        timedelta(days=goods_delay)
    )

    invoice_timestamp = (
        gr_timestamp +
        timedelta(days=random.randint(1, 5))
    )

    signoff_timestamp = (
        invoice_timestamp +
        timedelta(days=random.randint(1, 4))
    )

    payment_delay = random.randint(7, 30)

    # Inject finance bottleneck
    if random.random() < 0.20:
        payment_delay += random.randint(
            15,
            45
        )

    disbursement_timestamp = (
        signoff_timestamp +
        timedelta(days=payment_delay)
    )

    # -----------------------------
    # Transaction record
    # -----------------------------

    transactions.append({
        "Case_ID": case_id,
        "Req_ID": req_id,
        "Clarification_Timestamp": clarification_ts,
        "Plan_ID": plan_id,
        "Contingency_Flag": contingency_flag,
        "Approval_Status": approval_status,
        "Approver_ID": approver_id,
        "Approval_Timestamp": approval_ts,
        "Amount": amount,
        "PO_ID": po_id,
        "Vendor_ID": vendor_id,
        "PO_Issue_Timestamp": po_issue_ts,
        "Shipment_ID": shipment_id,
        "Expected_Arrival_Date": expected_arrival_date,
        "GR_ID": gr_id,
        "Received_Qty": received_qty,
        "GR_Timestamp": gr_timestamp,
        "Invoice_ID": invoice_id,
        "Billed_Amount": billed_amount,
        "Invoice_Timestamp": invoice_timestamp,
        "Match_Status": match_status,
        "Exception_Flag": exception_flag,
        "Resolution_Notes": resolution_notes,
        "Approval_Batch_ID": approval_batch_id,
        "Signoff_Timestamp": signoff_timestamp,
        "Payment_ID": payment_id,
        "Disbursement_Timestamp": disbursement_timestamp
    })

    # -----------------------------
    # Process Mining Event Log
    # -----------------------------

    process_events = [
        ("Create Requisition", start_ts),
        ("Clarification", clarification_ts),
        ("Approval", approval_ts),
        ("Issue Purchase Order", po_issue_ts),
        ("Goods Receipt", gr_timestamp),
        ("Invoice Receipt", invoice_timestamp),
        ("Finance Signoff", signoff_timestamp),
        ("Vendor Payment", disbursement_timestamp)
    ]

    for activity, timestamp in process_events:

        event_log.append({
            "Case_ID": case_id,
            "Activity": activity,
            "Timestamp": timestamp,
            "Vendor_ID": vendor_id,
            "Approver_ID": approver_id,
            "Amount": amount,
            "Exception_Flag": exception_flag,
            "Approval_Status": approval_status,
            "Match_Status": match_status
        })

    # Rework loop for process mining
    if exception_flag == "Yes":

        rework_ts = (
            invoice_timestamp +
            timedelta(days=random.randint(1, 3))
        )

        event_log.append({
            "Case_ID": case_id,
            "Activity": "Resolve Exception",
            "Timestamp": rework_ts,
            "Vendor_ID": vendor_id,
            "Approver_ID": approver_id,
            "Amount": amount,
            "Exception_Flag": "Yes",
            "Approval_Status": approval_status,
            "Match_Status": match_status
        })

# ---------------------------------
# Export
# ---------------------------------

transaction_df = pd.DataFrame(transactions)

event_log_df = (
    pd.DataFrame(event_log)
    .sort_values(["Case_ID", "Timestamp"])
)

transaction_df.to_csv(
    "data/p2p_transaction_table.csv",
    index=False
)

event_log_df.to_csv(
    "data/p2p_event_log.csv",
    index=False
)

print("Transaction rows:", len(transaction_df))
print("Event log rows:", len(event_log_df))