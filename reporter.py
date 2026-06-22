import pandas as pd
from datetime import datetime
import requests
import json
import pandas as pd
from datetime import datetime

# Paste your copied Discord webhook URL here
DISCORD_WEBHOOK_URL = "YOUR_WEBHOOK_URL_HERE"

def send_discord_alert(row):
    """Fires a real-time push notification to a SOC channel for Critical threats."""
    if not DISCORD_WEBHOOK_URL or DISCORD_WEBHOOK_URL == "YOUR_WEBHOOK_URL_HERE":
        return

    payload = {
        "content": "🚨 **CRITICAL THREAT DETECTED** 🚨",
        "embeds": [{
            "title": f"Active Attack from IP: {row['srcip']}",
            "color": 16711680, # Red
            "fields": [
                {"name": "Severity", "value": "CRITICAL", "inline": True},
                {"name": "Ports Scanned", "value": f"{row['unique_dst_ports']:,}", "inline": True},
                {"name": "Data Exfiltrated", "value": f"{row['total_bytes_sent']:,} Bytes", "inline": False},
                {"name": "Critical Infrastructure Targeted", "value": "Yes" if row['critical_targets'] else "No", "inline": False}
            ],
            "footer": {"text": "The Network Bouncer - Automated SOC Alert"}
        }]
    }

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"[!] Failed to send webhook alert: {e}")

# ... (Keep your existing generate_html_dashboard and generate_report functions here) ...
def generate_html_dashboard(df, filename="dashboard.html"):
    """Generates a standalone, dark-mode HTML/CSS dashboard for the Analyst."""
    html_content = f"""
    <html>
    <head>
        <title>The Network Bouncer - SOC Dashboard</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 40px; }}
            h1 {{ color: #ff7b72; text-align: center; border-bottom: 2px solid #30363d; padding-bottom: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #161b22; }}
            th, td {{ padding: 12px; border: 1px solid #30363d; text-align: left; }}
            th {{ background-color: #21262d; color: #58a6ff; }}
            .critical {{ color: #ff7b72; font-weight: bold; }}
            .high {{ color: #ffa657; font-weight: bold; }}
            .exfil {{ background-color: rgba(255, 123, 114, 0.1); }}
        </style>
    </head>
    <body>
        <h1>🛡️ The Network Bouncer - Threat Intelligence Report</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <table>
            <tr><th>Source IP</th><th>Severity</th><th>Unique Ports Scanned</th><th>Total Data Sent (Bytes)</th><th>Exfil Risk</th><th>Critical Targets Hit</th></tr>
    """
    
    for _, row in df.iterrows():
        sev_class = "critical" if row['severity'] == 'CRITICAL' else "high" if row['severity'] == 'High' else ""
        exfil_row = "class='exfil'" if row['exfiltration_risk'] else ""
        
        html_content += f"""
            <tr {exfil_row}>
                <td>{row['srcip']}</td>
                <td class="{sev_class}">[{row['severity']}]</td>
                <td>{row['unique_dst_ports']:,}</td>
                <td>{row['total_bytes_sent']:,}</td>
                <td>{'🚨 YES' if row['exfiltration_risk'] else 'NO'}</td>
                <td>{'🚨 YES' if row['critical_targets'] else 'NO'}</td>
            </tr>
        """
        
    html_content += "</table></body></html>"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[+] Interactive UI Dashboard generated: {filename}")

def generate_report(suspicious_df, output_csv="suspicious_activity_report.csv"):
    if suspicious_df.empty:
        print("\n[+] No suspicious activity detected. The network is secure.")
        return

    print("\n" + "="*70)
    print("🚨 SUSPICIOUS ACTIVITY DETECTED 🚨".center(70))
    print("="*70)
    
    for index, row in suspicious_df.head(5).iterrows():
        print(f"Source IP:           {row['srcip']}")
        print(f"Severity:            [{row['severity'].upper()}]")
        print(f"Unique Ports:        {row['unique_dst_ports']:,}")
        if row['critical_targets']:
            print("Warning:             Targeted Infrastructure (SSH/FTP/DB)")
        if row['exfiltration_risk']:
            print(f"Warning:             Data Exfiltration Risk ({row['total_bytes_sent']:,} Bytes)")
        print("-" * 70)

    suspicious_df.to_csv(output_csv, index=False)
    print(f"\n[+] CSV Report saved to: {output_csv}")
    
    generate_html_dashboard(suspicious_df)

def export_json_feed(df, filename="threat_feed.json"):
    """
    Decouples the architecture by exporting a live JSON data feed.
    This allows a modern frontend to consume the threat data asynchronously.
    """
    print("[*] Exporting live JSON feed for frontend decoupling...")
    
    # We convert the dataframe to a dictionary, making sure to handle the sets/booleans cleanly
    export_df = df.copy()
    export_df['critical_targets'] = export_df['critical_targets'].astype(bool)
    export_df['exfiltration_risk'] = export_df['exfiltration_risk'].astype(bool)
    
    # Export to a clean JSON array
    export_df.to_json(filename, orient="records", indent=4)
    print(f"[+] JSON API Feed updated at: {filename}")