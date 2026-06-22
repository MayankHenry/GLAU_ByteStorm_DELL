import matplotlib.pyplot as plt

def generate_charts(suspicious_df):
    """
    Generates a bar chart visualizing the most aggressive port scanners.
    """
    if suspicious_df.empty:
        return

    print("[*] Generating visualization charts...")
    
    # Take the top 10 worst offenders
    top_scanners = suspicious_df.head(10)
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(top_scanners['srcip'], top_scanners['unique_dst_ports'], color='darkred')
    
    plt.title('Top Suspicious IPs by Unique Ports Scanned (10s Window)', fontsize=14)
    plt.xlabel('Source IP Address', fontsize=12)
    plt.ylabel('Number of Unique Ports Targeted', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add the exact numbers on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 50, int(yval), ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig('suspicious_activity_chart.png')
    print("[+] Chart saved to: suspicious_activity_chart.png")