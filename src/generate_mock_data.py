import csv
import random
import os

# Ensure directories exist
os.makedirs('data/raw', exist_ok=True)

regions = ['Midwest', 'South', 'West', 'Northeast']
livestock_types = ['Dairy Cattle', 'Beef Cattle', 'Swine', 'Poultry']

# 1. Generate USDA NASS Data
print("Generating USDA NASS Livestock data...")
with open('data/raw/usda_nass_livestock.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['producer_id', 'producer_name', 'region', 'livestock_type', 'head_count', 'reporting_year', 'program_intervention_adopted'])
    
    for i in range(1, 501):
        producer_id = f"P{i:04d}"
        producer_name = f"Farm Operation {i}"
        
        # Introduce some data quality issues for the verification workflow to catch
        # E.g., 5% chance region is missing, 5% chance head count is negative/zero
        region = random.choice(regions) if random.random() > 0.05 else ''
        head_count = random.randint(50, 5000)
        if random.random() < 0.05:
            head_count = -1 * random.randint(10, 100) # Invalid
            
        l_type = random.choice(livestock_types)
        intervention = random.choice(['Yes', 'No', 'Planned'])
        
        # Add 2023 data
        writer.writerow([producer_id, producer_name, region, l_type, head_count, 2023, intervention])
        
        # Add 2024 data (maybe head count changed slightly)
        head_count_24 = head_count + int(head_count * random.uniform(-0.1, 0.1))
        intervention_24 = 'Yes' if intervention == 'Planned' else intervention
        writer.writerow([producer_id, producer_name, region, l_type, head_count_24, 2024, intervention_24])

# 2. Generate EPA GHG Factors
print("Generating EPA GHG Emissions Factors...")
with open('data/raw/epa_ghg_factors.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['livestock_type', 'region', 'emissions_factor_mt_co2e_per_head'])
    
    # Base factors
    base_factors = {'Dairy Cattle': 4.5, 'Beef Cattle': 2.8, 'Swine': 0.8, 'Poultry': 0.05}
    
    for l_type in livestock_types:
        for reg in regions:
            # Add some regional variation
            factor = base_factors[l_type] * random.uniform(0.9, 1.1)
            writer.writerow([l_type, reg, round(factor, 3)])
            
# 3. Generate Users Roles for RLS
print("Generating Users Roles...")
with open('data/raw/users_roles.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['user_email', 'role', 'region_access', 'producer_id_access'])
    
    # Regional Managers
    for reg in regions:
        writer.writerow([f"manager_{reg.lower()}@elanco.com", 'Regional Manager', reg, 'ALL'])
        
    # Producers
    for i in range(1, 501):
        producer_id = f"P{i:04d}"
        writer.writerow([f"owner_{producer_id.lower()}@farm.com", 'Producer', 'ALL', producer_id])

print("Mock data generation complete.")
