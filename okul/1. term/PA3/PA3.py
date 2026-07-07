import sys

# Global dictionary to store tables
tables = {}

def create_table(table_name, columns):
    if table_name in tables:
        print(f"Error: Table '{table_name}' already exists.")
        return
    tables[table_name] = {"columns": columns, "rows": []}
    print(f"Table '{table_name}' created with columns: {columns}")

def insert(table_name, values):
    if table_name not in tables:
        print(f"Error: Table '{table_name}' does not exist.")
        return
    table = tables[table_name]
    if len(values) != len(table["columns"]):
        print(f"Error: Column count mismatch in table '{table_name}'.")
        return
    table["rows"].append(dict(zip(table["columns"], values)))
    print(f"Inserted into '{table_name}': {values}")

def parse_conditions(condition_str):
    """Parse conditions like '{"key": "value"}' into a dictionary."""
    condition_str = condition_str.strip("{}").replace('"', '')
    return dict(pair.split(":") for pair in condition_str.split(","))

def select(table_name, columns, conditions=None):
    if table_name not in tables:
        print(f"Error: Table '{table_name}' does not exist.")
        return
    table = tables[table_name]
    rows = table["rows"]
    if conditions:
        filtered_rows = []
        for row in rows:
            match = True
            for key, value in conditions.items():
                if row.get(key) != value:
                    match = False
                    break
            if match:
                filtered_rows.append(row)
        rows = filtered_rows

    result = [[row[col] for col in columns] for row in rows]
    print(f"Select result from '{table_name}': {result}")

def update(table_name, updates, conditions=None):
    if table_name not in tables:
        print(f"Error: Table '{table_name}' does not exist.")
        return
    table = tables[table_name]
    updated_count = 0
    for row in table["rows"]:
        if not conditions or all(row.get(k) == v for k, v in conditions.items()):
            for k, v in updates.items():
                row[k] = v
            updated_count += 1
    print(f"Updated {updated_count} rows in '{table_name}'.")

def delete(table_name, conditions=None):
    if table_name not in tables:
        print(f"Error: Table '{table_name}' does not exist.")
        return
    table = tables[table_name]
    before_count = len(table["rows"])
    if conditions:
        table["rows"] = [row for row in table["rows"] if not all(row.get(k) == v for k, v in conditions.items())]
    else:
        table["rows"] = []
    deleted_count = before_count - len(table["rows"])
    print(f"Deleted {deleted_count} rows from '{table_name}'.")

def count(table_name, conditions=None):
    if table_name not in tables:
        print(f"Error: Table '{table_name}' does not exist.")
        return
    table = tables[table_name]
    rows = table["rows"]
    if conditions:
        rows = [row for row in rows if all(row.get(k) == v for k, v in conditions.items())]
    print(f"Count result: {len(rows)} rows match the conditions.")

def process_command(command):
    parts = command.split(maxsplit=2)
    if not parts:
        return
    action = parts[0]
    if action == "CREATE_TABLE":
        table_name, columns = parts[1], parts[2].split(",")
        create_table(table_name, columns)
    elif action == "INSERT":
        table_name, values_str = parts[1], parts[2]
        values = values_str.split(",")
        insert(table_name, values)
    elif action == "SELECT":
        args = parts[1].split(" WHERE ")
        table_name, columns = args[0].split()[0], args[0].split()[1].split(",")
        conditions = parse_conditions(args[1]) if len(args) > 1 else None
        select(table_name, columns, conditions)
    elif action == "UPDATE":
        args = parts[1].split(" WHERE ")
        table_name = args[0].split()[0]
        updates = parse_conditions(args[0].split()[1])
        conditions = parse_conditions(args[1]) if len(args) > 1 else None
        update(table_name, updates, conditions)
    elif action == "DELETE":
        args = parts[1].split(" WHERE ")
        table_name = args[0]
        conditions = parse_conditions(args[1]) if len(args) > 1 else None
        delete(table_name, conditions)
    elif action == "COUNT":
        args = parts[1].split(" WHERE ")
        table_name = args[0]
        conditions = parse_conditions(args[1]) if len(args) > 1 else None
        count(table_name, conditions)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 database.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, "r") as f:
            for line in f:
                process_command(line.strip())
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
