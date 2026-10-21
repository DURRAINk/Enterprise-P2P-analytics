import pandas as pd 
import matplotlib.pyplot as plt

class BottleneckAnalyzer:
     
    def __init__(self, df):
        self.df = df
        self.sla_sample = {'clarif_approval_diff': 48, 
                'approval_poissue_diff': 2, 
                'poissue_gr_diff': 600, 
                'gr_invoice_diff': 120, 
                'invoice_signoff_diff': 72, 
                'signoff_payment_diff': 720} 
        self.diff_df = pd.DataFrame({
                "clarif_approval_diff": (self.df.approval_timestamp - self.df.clarification_timestamp).dt.total_seconds() / 3600,
                "approval_poissue_diff": (self.df.po_issue_timestamp - self.df.approval_timestamp).dt.total_seconds() / 3600,
                "poissue_gr_diff": (self.df.gr_timestamp - self.df.po_issue_timestamp).dt.total_seconds() / 3600,
                "gr_invoice_diff": (self.df.invoice_timestamp - self.df.gr_timestamp).dt.total_seconds() / 3600,
                "invoice_signoff_diff": (self.df.signoff_timestamp - self.df.invoice_timestamp).dt.total_seconds() / 3600,
                "signoff_payment_diff": (self.df.disbursement_timestamp - self.df.signoff_timestamp).dt.total_seconds() / 3600
            })

    def timetaken_distribution(self):
        fig, axes = plt.subplots(3, 2, figsize=(14, 12))
        for ax, (title, diff) in zip(axes.flat, self.diff_df.items()):
            ax.hist(diff.dropna(), bins=30, edgecolor="black")
            ax.set(title=title, xlabel="Duration (hours)", ylabel="Number of transactions")

        fig.tight_layout()
        plt.show()


    def identify_bottlenecks(self, sla_dict):
        self.sla = sla_dict
        time_taken_df = self.diff_df.copy()
        time_taken_df['case_id'] = self.df['case_id']

        time_taken_df['clarif_approval_time_extend'] = time_taken_df['clarif_approval_diff'] - self.sla['clarif_approval_diff']
        time_taken_df['approval_poissue_time_extend'] = time_taken_df['approval_poissue_diff'] - self.sla['approval_poissue_diff']
        time_taken_df['poissue_gr_time_extend'] = time_taken_df['poissue_gr_diff'] - self.sla['poissue_gr_diff']
        time_taken_df['gr_invoice_time_extend'] = time_taken_df['gr_invoice_diff'] - self.sla['gr_invoice_diff']
        time_taken_df['invoice_signoff_time_extend'] = time_taken_df['invoice_signoff_diff'] - self.sla['invoice_signoff_diff']
        time_taken_df['signoff_payment_time_extend'] = time_taken_df['signoff_payment_diff'] - self.sla['signoff_payment_diff']

        self.time_taken_df = time_taken_df

        bn_case_ids = {'clarif_approval': time_taken_df[time_taken_df['clarif_approval_time_extend'] > 0]['case_id'],
                        'approval_poissue': time_taken_df[time_taken_df['approval_poissue_time_extend'] > 0]['case_id'],
                        'poissue_gr': time_taken_df[time_taken_df['poissue_gr_time_extend'] > 0]['case_id'],
                        'gr_invoice': time_taken_df[time_taken_df['gr_invoice_time_extend'] > 0]['case_id'],
                        'invoice_signoff': time_taken_df[time_taken_df['invoice_signoff_time_extend'] > 0]['case_id'],
                        'signoff_payment': time_taken_df[time_taken_df['signoff_payment_time_extend'] > 0]['case_id']}
        
        cases = len(time_taken_df)
        bottleneck_map = f'''
        Total_cases({cases})
          |
          ↓
        Clarification Requirements
          |
        {cases - len(bn_case_ids['clarif_approval'])} ie. ({((cases - len(bn_case_ids['clarif_approval'])) / cases) * 100:.2f}%)
          ↓
        PR Approval
          |
        {cases-len(bn_case_ids['approval_poissue'])} ie. ({((cases - len(bn_case_ids['approval_poissue']  )) / cases) * 100:.2f}%)
          ↓
        PO Issue
          |
        {cases-len(bn_case_ids['poissue_gr'])} ie. ({((cases - len(bn_case_ids['poissue_gr'])) / cases) * 100:.2f}%)
          ↓
        Goods Receipt
          |
        {cases-len(bn_case_ids['gr_invoice'])} ie. ({((cases - len(bn_case_ids['gr_invoice'])) / cases) * 100:.2f}%)
          ↓
        Invoice
          |
        {cases-len(bn_case_ids['invoice_signoff'])} ie. ({((cases - len(bn_case_ids['invoice_signoff'])) / cases) * 100:.2f}%)
          ↓
        Sign-off
          |
        {cases-len(bn_case_ids['signoff_payment'])} ie. ({((cases - len(bn_case_ids['signoff_payment'])) / cases) * 100:.2f}%)
          ↓
        Payment'''

        return bottleneck_map, bn_case_ids