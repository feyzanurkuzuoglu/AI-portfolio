import sys

tables = {}

def create_table(table_name, columns):
    if table_name in tables:
        print(f"Table '{table_name}' already exists.")
        return
    tables[table_name] = {"columns": columns, "rows": []}
    print(f"Table '{table_name}' created with columns: {columns}")

def insert(table_name, values):
    if table_name not in tables:
        print(f"Error: Table '{table_name}' does not exist.")
        return
    table = tables[table_name]
    table["rows"].append(dict(zip(table["columns"], values)))
    print(f"Inserted into '{table_name}': {values}")



def select(table_name, columns, curlies):
    table = tables[table_name]
    rows = table["rows"]

    selected_rows = []
    for row in rows:
        for curly in curlies:
            for key, value in curly.items():
                if row[key] == value:
                    selected_rows.append(row)
        rows = selected_rows
        for row in rows:
            for col in columns:
                print(f"Selected from '{table_name}': {col} {row[col]}")




def update(table_name, updates, curly):
    table = tables[table_name]
    updated_count = 0
    for row in table["rows"]:
        for key, value in curly.items():
            if row.get(key) == value:
                for k, v in updates.items():
                    row[k] = v
                updated_count += 1
    print(f"Updated {updated_count} rows in '{table_name}'.")
    print(f"Updated {curly} rows to '{updates}'.")
    table_s(tables[table_name])




def delete(table_name, curlies):
    table = tables[table_name]
    rows = table["rows"]
    deleted_count = 0
    for curly in curlies:
        for row in rows:
            for key, value in curly.items():
                if row[key] == value:
                    row[key] = []
                    deleted_count += 1
    print(f"Deleted {deleted_count} rows from '{table_name}'.")
    table_s(tables[table_name])



def count(table_name, curlies):
    table = tables[table_name]
    rows = table["rows"]
    count = 0
    for curly in curlies:
        for k, v in curly.items():
            for row in rows:
                if row[k] == v:
                    count += 1
    print(f"Count result: {count} rows match the conditions.")

def table_s(table):
    list = []
    for a, b in table.items():
        list.append(b)
    print(f"{list[0]}\n")

    for l in list[1]:
        print(f"{l}\n")

def merge(line):
    parts = line.split(maxsplit=2)
    if not parts:
        return
    action = parts[0]
    if action == "CREATE_TABLE":
        table_name, columns = parts[1], parts[2].split(",")
        create_table(table_name, columns)

    elif action == "INSERT":
        table_name, values_s = parts[1], parts[2]
        values = values_s.split(",")
        insert(table_name, values)

    elif action == "SELECT":
        table_name = parts[1].strip()
        args = parts[2].split(" WHERE ")
        columns = args[0].split(",")
        b = args[1].strip("{}").replace('"', '').split(",")
        curlies = []
        for a in b:
            m = a.index(":")
            curly = {a[0:m].strip(): a[m + 1:].strip()}
            curlies.append(curly)

        if table_name in tables:
            test = [c for c in columns if c not in tables[table_name]["columns"]]
            for curly in curlies:
                for a in curly:
                    if a not in tables[table_name]["columns"] :
                        print(f"Error: Column '{a}' does not exist!")
                    elif test:
                        for c in test:
                            print(f"Error: Column '{c}' does not exist!")
                    else:
                        select(table_name, columns, curlies)
        else:
            print(f"Error: Table '{table_name}' does not exist!")

    elif action == "UPDATE":
        table_name = parts[1].strip()
        args = parts[2].split(" WHERE ")
        a = args[0].strip("{}").replace('"', '').split(":")
        b = args[1].strip("{}").replace('"', '').split(":")
        updates = {a[0].strip(): a[1].strip()}
        curly = {b[0].strip(): b[1].strip()}
        if table_name in tables:
            if (a[0] not in tables[table_name]["columns"]):
                print(f"Error: Column '{a[0]}' does not exist.")
            elif (b[0] not in tables[table_name]["columns"]):
                print(f"Error: Column '{b[0]}' does not exist.")
            else:
                update(table_name, updates, curly)
        else:
            print(f"Error: Table '{table_name}' does not exist!")



    elif action == "DELETE":
        table_name = parts[1].strip()
        args = parts[2].split(maxsplit=1)
        b = args[1].strip("{}").replace('"', '').split(",")
        curlies = []
        for a in b:
            m = a.index(":")
            curly = {a[0:m].strip(): a[m + 1:].strip()}
            curlies.append(curly)
        if table_name in tables:
            for curly in curlies:
                for a in curly:
                    if a not in tables[table_name]["columns"]:
                        print(f"Error: Column '{a}' does not exist!")
                    else:

                        delete(table_name, curlies)
        else:
            print(f"Error: Table '{table_name}' does not exist!")

    elif action == "COUNT":
        table_name = parts[1].strip()
        args = parts[2].split(maxsplit=1)
        b = args[1].strip("{}").replace('"', '').split(",")
        curlies = []
        for a in b:
            m = a.index(":")
            curly = {a[0:m].strip(): a[m + 1:].strip()}
            curlies.append(curly)
        if table_name in tables:
            for curly in curlies:
                for a in curly:
                    if a not in tables[table_name]["columns"] :
                        print(f"Error: Column '{a}' does not exist!")
                    else:

                        count(table_name, curlies)
        else:
            print(f"Error: Table '{table_name}' does not exist!")

    elif action == "JOIN":
        a = parts[2].split()
        print(f"{parts[1]} joined on {a[1].strip()}.")




def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    input = sys.argv[1]
    try:
        with open(input, "r") as f:
            for line in f:
                merge(line.strip())
    except FileNotFoundError:
        print(f"Error: File '{input}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()




















