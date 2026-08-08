import csv

def build_star_schema():
    print("Building Star Schema for Power BI consumption...")
    
    # 1. Load EPA Factors
    epa_factors = {}
    with open('data/raw/epa_ghg_factors.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['region'], row['livestock_type'])
            epa_factors[key] = float(row['emissions_factor_mt_co2e_per_head'])
            
    fact_emissions = []
    dim_producer = {}
    
    with open('data/processed/clean_usda.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            p_id = row['producer_id']
            # Populate Dim_Producer (upsert logic)
            if p_id not in dim_producer:
                dim_producer[p_id] = {
                    'producer_id': p_id,
                    'producer_name': row['producer_name'],
                    'region': row['region']
                }
                
            # Populate Fact_Emissions
            l_type = row['livestock_type']
            reg = row['region']
            head_count = int(row['head_count'])
            factor = epa_factors.get((reg, l_type), 0.0)
            
            total_emissions = head_count * factor
            
            fact_emissions.append({
                'producer_id': p_id,
                'reporting_year': row['reporting_year'],
                'livestock_type': l_type,
                'head_count': head_count,
                'emissions_factor': factor,
                'total_emissions_mt_co2e': round(total_emissions, 2),
                'program_intervention_adopted': row['program_intervention_adopted']
            })
            
    # Write Dim_Producer
    with open('data/processed/dim_producer.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['producer_id', 'producer_name', 'region'])
        writer.writeheader()
        writer.writerows(dim_producer.values())
        
    # Write Fact_Emissions
    with open('data/processed/fact_emissions.csv', 'w', newline='') as f:
        fieldnames = ['producer_id', 'reporting_year', 'livestock_type', 'head_count', 
                      'emissions_factor', 'total_emissions_mt_co2e', 'program_intervention_adopted']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(fact_emissions)
        
    print(f"Star schema complete. Fact records: {len(fact_emissions)}, Producer records: {len(dim_producer)}")

if __name__ == "__main__":
    build_star_schema()
