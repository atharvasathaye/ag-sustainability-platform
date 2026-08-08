# Implementing Row-Level Security (RLS) in Power BI

Row-Level Security (RLS) is critical for the Agricultural Sustainability Reporting Platform to ensure that producers only see their own operation's data, while regional managers can see all data within their assigned region.

## Prerequisites
Ensure your Power BI Data Model is set up correctly:
1. `fact_emissions` is connected to `dim_producer` via `producer_id` (Many-to-1).
2. `users_roles` table is loaded (from `data/raw/users_roles.csv`).

## Setting up the Roles

Open Power BI Desktop, go to the **Modeling** tab, and select **Manage Roles**.

### Role 1: Producer
This role restricts a user to only see their specific farm operation.
1. Click **Create**, name the role **Producer**.
2. Select the `users_roles` table.
3. Enter the following DAX filter expression:
   ```dax
   [user_email] = USERPRINCIPALNAME() && [role] = "Producer"
   ```
4. Now, we must filter the actual data. Select the `dim_producer` table.
5. Enter the following DAX filter expression to connect the user's allowed `producer_id_access` to the producer table:
   ```dax
   [producer_id] = LOOKUPVALUE(users_roles[producer_id_access], users_roles[user_email], USERPRINCIPALNAME())
   ```

### Role 2: Regional Manager
This role restricts a user to only see farm operations within their assigned region.
1. Click **Create**, name the role **Regional Manager**.
2. Select the `users_roles` table.
3. Enter the following DAX filter expression:
   ```dax
   [user_email] = USERPRINCIPALNAME() && [role] = "Regional Manager"
   ```
4. Select the `dim_producer` table.
5. Enter the following DAX filter expression:
   ```dax
   [region] = LOOKUPVALUE(users_roles[region_access], users_roles[user_email], USERPRINCIPALNAME())
   ```

## Testing the Roles
1. In the **Modeling** tab, click **View as**.
2. Check the box for **Producer** and check **Other user**.
3. Enter a mock producer email, e.g., `owner_p0012@farm.com`.
4. Observe the dashboards filter down to only show data for Producer P0012.
5. Repeat for **Regional Manager** using an email like `manager_midwest@elanco.com` and observe it showing all Midwest operations.
