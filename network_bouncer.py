import argparse
from parser import load_network_data
from detector import detect_suspicious_activity
from reporter import generate_report, export_json_feed
from visualizer import generate_charts
from ml_model import run_ml_classification
from database import log_incidents
from mitigation import generate_firewall_rules

def main():
    parser_arg = argparse.ArgumentParser(description="The Network Bouncer: Enterprise SOC Engine")
    parser_arg.add_argument("target", help="Path to a CSV file or a folder containing multiple CSVs")
    parser_arg.add_argument("--max-ports", type=int, default=50, help="Threshold for unique ports")
    parser_arg.add_argument("--max-ips", type=int, default=20, help="Threshold for unique IPs")
    
    args = parser_arg.parse_args()

    print("\n🛡️ Starting The Network Bouncer 🛡️")
    print("-" * 50)
    
    df = load_network_data(args.target)
    if df is None: return

    suspicious_ips, all_metrics = detect_suspicious_activity(df, max_ports=args.max_ports, max_ips=args.max_ips)
    ml_flagged_ips = run_ml_classification(all_metrics)

    log_incidents(suspicious_ips)
    
    # Trigger the new decoupled API export
    export_json_feed(suspicious_ips)
    
    # Trigger the Webhooks and CSV generation
    generate_report(suspicious_ips)
    generate_charts(suspicious_ips)
    
    # Trigger Active Defense
    generate_firewall_rules(suspicious_ips)

if __name__ == "__main__":
    main()