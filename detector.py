import pandas as pd

# High-value ports: SSH (22), FTP (21), RDP (3389), MySQL (3306), MSSQL (1433)
CRITICAL_PORTS = {'22', '21', '3389', '3306', '1433'}

def assign_severity(ports, hit_critical):
    if hit_critical and ports > 1000: return 'CRITICAL'
    elif ports > 5000: return 'CRITICAL'
    elif ports > 1000: return 'High'
    elif ports > 100: return 'Medium'
    return 'Low'

def check_critical_ports(port_list):
    """Returns True if any critical infrastructure ports were scanned."""
    return any(port in CRITICAL_PORTS for port in port_list)

def detect_suspicious_activity(df, max_ports=50, max_ips=20, time_window=10):
    print(f"[*] Analyzing traffic using {time_window}-second windows with Signature Detection...")

    df['dsport'] = df['dsport'].astype(str)
    df['time_bucket'] = (df['timestamp'] // time_window) * time_window

    # Group by IP and Time, but now aggregate data payload and port lists
    metrics = df.groupby(['srcip', 'time_bucket']).agg(
        total_connections=('dstip', 'count'),
        unique_dst_ips=('dstip', 'nunique'),
        unique_dst_ports=('dsport', 'nunique'),
        total_bytes_sent=('sbytes', 'sum'),
        ports_scanned=('dsport', lambda x: set(x))
    ).reset_index()

    suspicious = metrics[
        (metrics['unique_dst_ports'] >= max_ports) | 
        (metrics['unique_dst_ips'] >= max_ips)
    ].copy()

    suspicious = suspicious.sort_values('unique_dst_ports', ascending=False).drop_duplicates('srcip')

    # Advanced Classification Logic
    suspicious['critical_targets'] = suspicious['ports_scanned'].apply(check_critical_ports)
    suspicious['severity'] = suspicious.apply(lambda row: assign_severity(row['unique_dst_ports'], row['critical_targets']), axis=1)
    
    # Flag IPs moving more than 5MB of data as Exfiltration risks
    suspicious['exfiltration_risk'] = suspicious['total_bytes_sent'] > 5000000 
    
    # Clean up the set of ports so it can be saved to CSV/JSON easily
    suspicious['ports_scanned'] = suspicious['ports_scanned'].apply(lambda x: "Multiple" if len(x) > 5 else str(list(x)))

    return suspicious, metrics