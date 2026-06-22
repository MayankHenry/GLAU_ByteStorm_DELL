from sklearn.ensemble import IsolationForest
import pandas as pd

def run_ml_classification(metrics_df):
    print("[*] Running Isolation Forest Anomaly Detection Engine...")
    
    ip_metrics = metrics_df.groupby('srcip').agg(
        total_conns=('total_connections', 'sum'),
        max_ports=('unique_dst_ports', 'max'),
        total_payload=('total_bytes_sent', 'sum')
    ).reset_index()

    model = IsolationForest(contamination=0.01, random_state=42)
    
    # The ML model now analyzes 3 dimensions of the attack
    features = ip_metrics[['total_conns', 'max_ports', 'total_payload']]
    ip_metrics['ml_anomaly'] = model.fit_predict(features)

    ml_flagged = ip_metrics[ip_metrics['ml_anomaly'] == -1]
    
    print(f"[+] ML Engine flagged {len(ml_flagged)} IPs as highly anomalous.")
    return ml_flagged