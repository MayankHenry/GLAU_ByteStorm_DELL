def generate_firewall_rules(suspicious_df):
    """
    Generates active defense mitigation commands for Critical threats.
    Outputs Windows Advanced Firewall (netsh) rules.
    """
    critical_threats = suspicious_df[suspicious_df['severity'] == 'CRITICAL']
    
    if critical_threats.empty:
        return

    print("\n" + "="*60)
    print("🛡️ ACTIVE DEFENSE: MITIGATION COMMANDS GENERATED 🛡️".center(60))
    print("="*60)
    print("Run the following commands in an Administrator command prompt to block active attackers:\n")
    
    for _, row in critical_threats.iterrows():
        ip = row['srcip']
        rule_name = f"Block_Scanner_{ip}"
        
        # Windows netsh command to block inbound traffic from the attacker
        cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip}'
        print(f"  > {cmd}")
        
    print("\n" + "="*60 + "\n")