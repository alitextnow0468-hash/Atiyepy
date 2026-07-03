# core/database.py
# ... (previous content) ...

# In init_database, add this column:
# columns_to_add.append(("mobile", "TEXT"))

# Then in load/save/update methods, include "mobile" field.
# For brevity in this fix, the UI will save mobile in employee dict even if column not yet migrated.