# Customer Due Wizard - Security Setup Guide

## Overview
This module implements record-level security for the Customer Due Wizard, allowing administrators to control which users can see which records based on their assigned security groups.

## Security Groups

The module uses **standard Odoo security groups** to control access:

### 1. Sales: User - Own Documents Only
- **Odoo Group**: `sales_team.group_sale_salesman`
- **Purpose**: Sales users can only see customer due records where they are assigned as the salesperson
- **Access Level**: Restricted to own records
- **Domain Filter**: `[('user_id', '=', user.id)]`
- **Location**: Settings → Users → Sales section

### 2. Sales: Administrator
- **Odoo Group**: `sales_team.group_sale_salesman_all_leads`
- **Purpose**: Sales managers/administrators can see all customer due records
- **Access Level**: Full access to all records
- **Domain Filter**: `[(1, '=', 1)]` (no restrictions)
- **Location**: Settings → Users → Sales section

### 3. Accounting/Invoicing: Full Access
- **Odoo Groups**: 
  - `account.group_account_invoice` (Invoicing)
  - `account.group_account_user` (Billing)
- **Purpose**: Accounting and invoicing users have full access to all customer due records
- **Access Level**: Full access to all records
- **Domain Filter**: `[(1, '=', 1)]` (no restrictions)
- **Location**: Settings → Users → Accounting section

## How to Assign Security Groups

### Via Odoo UI:
1. Go to **Settings** → **Users & Companies** → **Users**
2. Select the user you want to configure
3. Configure access in the relevant sections:

#### For Sales Users:
- Scroll to the **Sales** section
- Select one of:
  - **User: Own Documents Only** - User sees only their assigned customers
  - **Administrator** - User sees all customer due records

#### For Accounting Users:
- Scroll to the **Accounting** section
- Select one of:
  - **Invoicing** - User has full access to customer due records
  - **Billing** - User has full access to customer due records

### Default Behavior:
- If a user has **no group assigned**, they will not see any customer due records (most restrictive)
- If a user has **Sales: User - Own Documents Only**, they see only records where `user_id` matches their user ID
- If a user has **Sales: Administrator**, they see all records
- If a user has **Accounting/Invoicing** access, they see all records

## Technical Details

### Record Rules Created:
1. **customer_due_wizard_rule_own**
   - Applies to: `sales_team.group_sale_salesman`
   - Domain: `[('user_id', '=', user.id)]`
   - Permissions: Read, Write, Create, Delete

2. **customer_due_wizard_rule_all**
   - Applies to: `sales_team.group_sale_salesman_all_leads`
   - Domain: `[(1, '=', 1)]`
   - Permissions: Read, Write, Create, Delete

3. **customer_due_wizard_rule_accounting**
   - Applies to: `account.group_account_invoice`, `account.group_account_user`
   - Domain: `[(1, '=', 1)]`
   - Permissions: Read, Write, Create, Delete

### Field Used for Filtering:
- **user_id**: Related field from `partner_id.user_id` (the salesperson assigned to the customer)

## Example Scenarios

### Scenario 1: Sales Representative
- **Group**: Sales: User - Own Documents Only
- **Result**: Can only see customer due records for customers assigned to them
- **Use Case**: Field sales reps who should only manage their own customer relationships

### Scenario 2: Sales Manager
- **Group**: Sales: Administrator
- **Result**: Can see all customer due records across all salespeople
- **Use Case**: Managers who need visibility into all customer accounts

### Scenario 3: Accountant
- **Group**: Accounting: Invoicing or Billing
- **Result**: Can see all customer due records for financial analysis and collections
- **Use Case**: Accountants who need to track customer balances and outstanding payments

### Scenario 4: Other Users (No Group)
- **Group**: None
- **Result**: Cannot see any customer due wizard records
- **Use Case**: Users who don't need access to this specific feature

## Access Matrix

| User Role | Group | Access Level | Can See |
|-----------|-------|--------------|---------|
| Sales Rep | Sales: User - Own Documents Only | Own Records | Only customers assigned to them |
| Sales Manager | Sales: Administrator | All Records | All customer due records |
| Accountant | Accounting: Invoicing/Billing | All Records | All customer due records |
| Other | None | No Access | Nothing |

## Upgrading the Module

After updating the module, make sure to:
1. Upgrade the module in Odoo
2. Verify that existing users have appropriate security groups assigned
3. Test access with different user accounts

## Troubleshooting

**Issue**: User cannot see any records
- **Solution**: Check if the user has been assigned to one of the security groups (Sales or Accounting)

**Issue**: User sees too many/too few records
- **Solution**: Verify the correct security group is assigned and that the `user_id` field is properly set on customer records

**Issue**: Changes not taking effect
- **Solution**: Clear browser cache, restart Odoo server, or try logging out and back in

**Issue**: Accounting users cannot access records
- **Solution**: Ensure the user has either "Invoicing" or "Billing" access in the Accounting section of their user profile

