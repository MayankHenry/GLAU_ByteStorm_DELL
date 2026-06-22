import pandas as pd
import glob
import os

def load_network_data(target_path):
    """Handles both single massive CSVs and folders of batch CSVs."""
    print(f"[*] Initializing ingestion engine for: {target_path}")
    
    # We added columns 7 (sbytes) and 8 (dbytes) to monitor for data exfiltration
    columns_to_keep = [0, 1, 2, 3, 7, 8, 26]
    column_names = ['srcip', 'sport', 'dstip', 'dsport', 'sbytes', 'dbytes', 'timestamp']
    
    dataframes = []

    # Check if the target is a directory or a single file
    if os.path.isdir(target_path):
        csv_files = glob.glob(os.path.join(target_path, "*.csv"))
        if not csv_files:
            print(f"[!] No CSV files found in directory '{target_path}'.")
            return None
    else:
        csv_files = [target_path]

    for file in csv_files:
        print(f"    -> Ingesting {os.path.basename(file)}...")
        try:
            df_chunk = pd.read_csv(
                file, header=None, usecols=columns_to_keep, 
                names=column_names, low_memory=False
            )
            df_chunk.dropna(subset=['srcip', 'dstip', 'dsport'], inplace=True)
            
            # Ensure bytes are numeric
            df_chunk['sbytes'] = pd.to_numeric(df_chunk['sbytes'], errors='coerce').fillna(0)
            dataframes.append(df_chunk)
        except Exception as e:
            print(f"    [!] Error reading {file}: {e}")

    if not dataframes:
        return None

    print("[*] Consolidating batch data...")
    master_df = pd.concat(dataframes, ignore_index=True)
    print(f"[+] Successfully loaded {len(master_df):,} total rows.")
    
    return master_df