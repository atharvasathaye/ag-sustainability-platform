import csv

def ingest_and_verify():
    print("Starting Databricks simulated ingestion & data verification...")
    
    clean_records = []
    quarantined_records = []
    
    with open('data/raw/usda_nass_livestock.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Business rules for verification
            is_valid = True
            reason = []
            
            if not row['region']:
                is_valid = False
                reason.append("Missing Critical Data Element: Region")
                
            try:
                head_count = int(row['head_count'])
                if head_count <= 0:
                    is_valid = False
                    reason.append("Invalid Integrity Check: Negative/Zero Head Count")
            except ValueError:
                is_valid = False
                reason.append("Invalid Integrity Check: Non-integer Head Count")
                
            if is_valid:
                clean_records.append(row)
            else:
                row['quarantine_reason'] = " | ".join(reason)
                quarantined_records.append(row)
                
    # Write clean data
    if clean_records:
        with open('data/processed/clean_usda.csv', 'w', newline='') as f:
            writer = csv.DictReader(open('data/raw/usda_nass_livestock.csv', 'r'))
            out_writer = csv.DictWriter(f, fieldnames=writer.fieldnames)
            out_writer.writeheader()
            out_writer.writerows(clean_records)
            
    # Write quarantined data
    if quarantined_records:
        with open('data/quarantine/quarantined_usda.csv', 'w', newline='') as f:
            # Need to get fieldnames from the first record
            fieldnames = list(quarantined_records[0].keys())
            out_writer = csv.DictWriter(f, fieldnames=fieldnames)
            out_writer.writeheader()
            out_writer.writerows(quarantined_records)
            
    print(f"Ingestion complete. Clean records: {len(clean_records)}, Quarantined records: {len(quarantined_records)}")
    
if __name__ == "__main__":
    ingest_and_verify()
