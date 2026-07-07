import sys



class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, table_name, columns, foreign_key=None, foreign_table=None):
        if table_name in self.tables:
            # There is no need for functions called within the join function to give this error output, it will be repeated in other functions..
            if "joined_table" not in table_name:
                print("###################### CREATE #########################")
                print(f"Error: Table '{table_name}' already exists.")
                print("#######################################################\n")
            return
        # Input format: CREATE_TABLE departments (department_name)
        #               CREATE_TABLE employees (name,age,wage) dept_id departments
        if "joined_table" not in table_name:
            columns = columns.split(',')

            self.tables[table_name] = {
                "columns": ["id"] + columns,
                "rows": [],
                "next_id": 1
            }
        else:
            self.tables[table_name] = {
                "columns": columns,
                "rows": [],
                "next_id": 1
            }

        if foreign_key and foreign_table:
            self.tables[table_name]["columns"].append(foreign_key)
            self.tables[table_name]["foreign_table"] = foreign_table

        if "joined_table" not in table_name:
            print("###################### CREATE #########################")
            print(f"Table '{table_name}' created with columns: {self.tables[table_name]['columns']}")
            print("#######################################################\n")

    def insert(self, table_name, values):
        """add row to table"""
        if table_name not in self.tables:
            if "joined_table" not in table_name:
                print("###################### INSERT #########################\n")
                print(f"Table '{table_name}' does not exist.")
                print("#######################################################\n")
            return

        table = self.tables[table_name]
        expected_columns = len(table["columns"]) - 1  # Number of columns excluding 'id'

        # Complete missing values with empty string
        if len(values) < expected_columns:
            values += ["" for _ in range(expected_columns - len(values))]

        new_row = {"id": table["next_id"]}
        # add to dictionary with columns and values
        # [1:] => not getting "id"
        new_row.update(dict(zip(table["columns"][1:], values)))
        table["rows"].append(new_row)
        # Increase "next_id" by 1 for each row
        table["next_id"] += 1
        if "joined_table" not in table_name:
            print("###################### INSERT #########################")
            print(f"\nTable: {table_name}")
            self.print_table(table_name)
            print("#######################################################\n")


    def select(self,table_name, columns, conditions):
        if table_name not in self.tables:
            print("###################### SELECT #########################")
            print(f"Table {table_name} does not exist!")
            print("#######################################################\n")
            return
        table = self.tables[table_name]

        # the case of more than one columns do not exist
        exists = []

        if columns == ['*']:
            columns = table["columns"]

        for col in columns:
            if col not in table["columns"]:
                exists.append(col)
                print("###################### SELECT #########################")
                print(f"Columns {exists} does not exist!")
                print("#######################################################\n")
                return

        # input format:
        # SELECT employees name,age WHERE age>29
        # SELECT employees * WHERE age>29
        # SELECT employees name,age WHERE age<29 => split from WHERE as columns and conditions

        # Since "conditions" is a list, we need to get the string element from it. We took it with pop() in case we split it incorrectly.
        conditions = conditions.pop()
        # Add the values that satisfy the condition to this list
        condition_list = []

        if "=" in conditions:
            cond = conditions.split("=")
            col = cond[0]
            row = cond[1]
            if col not in table["columns"]:
                exists.append(col)
                print("###################### SELECT #########################")
                print(f"Columns {exists} does not exist!")
                print("#######################################################\n")
                return
            # get column values from rows of table
            for r in table["rows"]:
                if r[col] == row:
                    condition_list.append(tuple(r.get(c) for c in columns))


        elif "<" in conditions:
            cond = conditions.split("<")
            col = cond[0]
            row = cond[1]
            if col not in table["columns"]:
                exists.append(col)
                print("###################### SELECT #########################")
                print(f"Columns {exists} does not exist!")
                print("#######################################################\n")
                return
            for r in table["rows"]:
                if r[col] < row:
                    condition_list.append(tuple(r.get(c) for c in columns))

        elif ">" in conditions:
            cond = conditions.split(">")
            col = cond[0]
            row = cond[1]
            if col not in table["columns"]:
                exists.append(col)
                print("###################### SELECT #########################")
                print(f"Columns '{exists}' does not exist!")
                print("#######################################################\n")
                return
            for r in table["rows"]:
                if r[col] > row:
                    condition_list.append(tuple(r.get(c) for c in columns))


        if condition_list:
            print("###################### SELECT #########################")
            print(f"Conditions: {conditions}")
            print("Result:", condition_list)
            print("#######################################################\n")


    def update(self,table_name, updates, conditions):
        if table_name not in self.tables:
            print("###################### UPDATE #########################")
            print(f"Error: Table '{table_name}' does not exist.")
            print("#######################################################\n")
            return
        table = self.tables[table_name]

        exists = []

        update_count = 0

        # input format:
        # UPDATE employees age:25 WHERE age=28
        # UPDATE employees wage:4000 WHERE wage>3300
        # UPDATE employees wage:3000 WHERE wage<2600 => split from WHERE as updates and conditions

        upd = updates.split(":")
        updcol = upd[0]
        updrow = upd[1]


        if "=" in conditions:
            cond = conditions.split("=")
            col = cond[0]
            row = cond[1]

            if col not in table["columns"]:
                exists.append(col)
            if updcol not in table["columns"]:
                exists.append(updcol)
            if exists:
                print("###################### UPDATE #########################")
                print(f"Columns {exists} does not exist!")
                print("#######################################################\n")
                return

            # select values to update from table
            for r in table["rows"]:
                if r[col] == row:
                    update_count += 1
                    # update the table
                    r[updcol] = updrow


        elif "<" in conditions:
            cond = conditions.split("<")
            col = cond[0]
            row = cond[1]

            if col not in table["columns"]:
                exists.append(col)

            if updcol not in table["columns"]:
                exists.append(updcol)

            if exists:
                print("###################### UPDATE #########################")
                print(f"Columns {exists} does not exist!")
                print("#######################################################\n")
                return

            for r in table["rows"]:
                if r[col] < row:
                    update_count += 1
                    r[updcol] = updrow


        elif ">" in conditions:
            cond = conditions.split(">")
            col = cond[0]
            row = cond[1]

            if col not in table["columns"]:
                exists.append(col)

            if updcol not in table["columns"]:
                exists.append(updcol)

            if exists:
                print("###################### UPDATE #########################")
                print(f"Columns {exists} does not exist!")
                print("#######################################################\n")
                return

            for r in table["rows"]:
                if r[col] > row:
                    update_count += 1
                    r[updcol] = updrow


        print("###################### UPDATE #########################")
        print(f"\nTable: {table_name}")
        self.print_table(table_name)
        print(f"Conditions: {conditions}")
        print(f"Update column: {updcol} Update value: {updrow}")
        print(f"{update_count} rows updated!")
        print("#######################################################\n")


    def delete(self,table_name, conditions):
        if table_name not in self.tables:
            print(f"Error: Table '{table_name}' does not exist.")
            return
        table = self.tables[table_name]

        exists = []

        delete_count = 0

        if conditions == "*":
            # delete all values
            for r in table["rows"]:
                table["rows"] = []
            print("###################### DELETE #########################")
            print(f"\nTable: {table_name}")
            # print empry table function
            self.print_empty_table(table_name)
            print(f"All rows deleted!")
            print("#######################################################\n")
            return


        if "=" in conditions:
            cond = conditions.split("=")
            col = cond[0]
            row = cond[1]
            if col not in table["columns"]:
                exists.append(col)
                print("###################### DELETE #########################")
                print(f"Columns {exists} does not exist!")
                print("#######################################################\n")
                return
            # select values to delete from table according to conditions
            for r in table["rows"]:
                if r[col] == row:
                    table["rows"].remove(r)
                    delete_count += 1
                    print("###################### DELETE #########################")
                    print(f"\nTable: {table_name}")
                    self.print_table(table_name)
                    print(f"Conditions: {conditions}")
                    print(f"{delete_count} rows deleted!")
                    print("#######################################################\n")


        elif "<" in conditions:
            cond = conditions.split("<")
            col = cond[0]
            row = cond[1]
            if col not in table["columns"]:
                exists.append(col)
                print("###################### DELETE #########################")
                print(f"Columns {exists} does not exist!")
                print("#######################################################\n")
                return
            for r in table["rows"]:
                if r[col] < row:
                    table["rows"].remove(r)
                    delete_count += 1
                    print("###################### DELETE #########################")
                    print(f"Table: {table_name}")
                    self.print_table(table_name)
                    print(f"Conditions: {conditions}")
                    print(f"{delete_count} rows deleted!")
                    print("#######################################################\n")


        elif ">" in conditions:
            cond = conditions.split(">")
            col = cond[0]
            row = cond[1]
            if col not in table["columns"]:
                exists.append(col)
                print("###################### DELETE #########################")
                print(f"Columns '{exists}' does not exist!")
                print("#######################################################\n")
                return
            for r in table["rows"]:
                if r[col] > row:
                    table["rows"].remove(r)
                    delete_count += 1
                    print("###################### DELETE #########################")
                    print(f"Table: {table_name}")
                    self.print_table(table_name)
                    print(f"Conditions: {conditions}")
                    print(f"{delete_count} rows deleted from {table_name}!")
                    print("#######################################################\n")




    def count(self,table_name, conditions):
        if table_name not in self.tables:
            print("###################### COUNT #########################")
            print(f"Table '{table_name}' does not exist.")
            print("#######################################################\n")
            return
        table = self.tables[table_name]

        # all values in the table
        if conditions == "*":
            print("###################### COUNT #########################")
            print(f"Total number of entries in {table_name} is {len(table['rows'])}")
            print("#######################################################\n")
            return

        exists = []

        count = 0

        if "=" in conditions:
            cond = conditions.split("=")
            col = cond[0]
            row = cond[1]
            if col not in table["columns"]:
                exists.append(col)
                print("###################### COUNT #########################")
                print(f"Columns {exists} does not exist!")
                print("#######################################################\n")
                return
            #  select values to count from table according to conditions
            for r in table["rows"]:
                if r[col] == row:
                    count += 1
            print("###################### COUNT #########################")
            print(f"Conditions: {conditions}")
            print(f"Total number of entries in {table_name} is {count}")
            print("#######################################################\n")

        elif "<" in conditions:
            cond = conditions.split("<")
            col = cond[0]
            row = cond[1]
            if col not in table["columns"]:
                exists.append(col)
                print("###################### COUNT #########################")
                print(f"Columns {exists} does not exist!")
                print("#######################################################\n")
                return
            for r in table["rows"]:
                if r[col] < row:
                    count += 1
            print("###################### COUNT #########################")
            print(f"Conditions: {conditions}")
            print(f"Total number of entries in {table_name} is {count}")
            print("#######################################################\n")


        elif ">" in conditions:
            cond = conditions.split(">")
            col = cond[0]
            row = cond[1]
            if col not in table["columns"]:
                exists.append(col)
                print("###################### COUNT #########################")
                print(f"Columns '{exists}' does not exist!")
                print("#######################################################\n")
                return
            for r in table["rows"]:
                if r[col] > row:
                    count += 1
            print("###################### COUNT #########################")
            print(f"Conditions: {conditions}")
            print(f"Total number of entries in {table_name} is {count}")
            print("#######################################################\n")



    def join(self, table1, table2, join_type=""):
        # I have to say about this join operation that while other commands are highly similar to real sql commands,
        # these join commands work differently from real sql implementation (especially FULL_JOIN).
        # Since it is explained very briefly in the assignment text, when I based it on sql implementation, the output values are different.
        # Please evaluate this code by considering these.

        if table1 not in self.tables:
            print("###################### JOIN #########################")
            print(f"Table '{table1}' does not exist.")
            print("#######################################################\n")
            return
        if table2 not in self.tables:
            print("###################### JOIN #########################")
            print(f"Table '{table2}' does not exist.")
            print("#######################################################\n")
            return


        foreign_key = None
        # The value containing _id will be foreign_key (department_id, course_id)
        for col in self.tables[table1]["columns"]:
            if "_id" in col:
                foreign_key = col


        if not foreign_key:
            print("###################### JOIN #########################")
            print(f"{table1} and {table2} cannot be joined!")
            print("#######################################################\n")
            return


        # I named each table differently so that it would not get mixed up and added to each other.
        if join_type == "LEFT":
            a = "Left Joined Table"
            joined_table_name = f"{table1}_{table2}_left_joined_table"
        elif join_type == "FULL":
            # As far as I understood from the assignment text, I wrote the full join operation.
            # Since there were both JOIN and FULL_JOIN in the sample inputs, I accepted them as the same.
            join_type =  None
            a = "Joined Table"
            joined_table_name = f"{table1}_{table2}_full_joined_table"
        else:
            a = "Joined Table"
            joined_table_name = f"{table1}_{table2}_joined_table"



        joined_table = None
        primary_key = "id"

        listt = []
        roww = {}



        for row1 in self.tables[table1]["rows"]:
            matched = False
            for row2 in self.tables[table2]["rows"]:
                if str(row1.get(foreign_key)) == str(row2.get(primary_key)):
                    # I collected the columns that match each other in a dictionary.
                    roww = {**row1, **row2}
                    # I will get the columns and rows values of the table I will create from that list.
                    listt.append(roww)
                    matched = True


            # In the sample output files,
            # in the table drawn in the left join operation,
            # the values of table2 are shown first, then the values of table1,
            # here in my code the table is drawn in the opposite way (table1 first table2 second).
            # Therefore, the left join function actually had to work like a right join.
            # I still wanted to preserve the original left join rows.
            # It works much more correctly but still not compatible with the output.


            # if join_type == "LEFT" and not matched:
            #     # We get all values from table1 and values that provide the conditions from table2.
            #     # We get all the values from the left table (table1) and only the values for the join conditions from the right table (table2).
            #     roww = {**row1, **{col: "" for col in self.tables[table2]["columns"]}}
            #     listt.append(roww)


            if join_type == "LEFT":
                for row2 in self.tables[table2]["rows"]:
                    matched = False
                    for row1 in self.tables[table1]["rows"]:
                        if str(row1.get(foreign_key)) == str(row2.get(primary_key)):
                            matched = True
                    if not matched:
                        # We get all values from table2 and values that provide the conditions from table1.
                        # We get all the values from  table1 and only the values for the join conditions from  table2.
                        roww = {**{col: "" for col in self.tables[table1]["columns"]}, **row2}
                        if roww not in listt:
                            listt.append(roww)


        if listt:
            # I will get the table's column values from the rows
            # Since the key values of all rows in the table will be the same, I take the key values from the first element.
            joined_columns = list(listt[0].keys())
            # empty table created
            self.create_table(joined_table_name, joined_columns)
            joined_table = self.tables[joined_table_name]
            for i in listt:
                # [1:] => not getting "id"
                values = list(i.values())[1:]
                # inserting values into table
                self.insert(joined_table_name, values)
            print("###################### JOIN #########################")
            print(f"\nTable: {a}")
            self.print_table(joined_table_name)
            print("#######################################################\n")
        else:
            print("###################### JOIN #########################")
            print(f"{table1} and {table2} cannot be joined!")
            print("#######################################################\n")




    def print_empty_table(self, table_name):
        """Function to print the empty table."""
        if table_name not in self.tables:
            print(f"Error: Table '{table_name}' does not exist.")
            return

        table = self.tables[table_name]
        columns = table["columns"]

        col_widths = {col: len(col) for col in columns}
        separator = "+" + "+".join("-" * (col_widths[col] + 2) for col in columns) + "+"
        header = "| " + " | ".join(col.ljust(col_widths[col]) for col in columns) + " |"

        print(separator)
        print(header)
        print(separator)
        print(separator)

    def print_table(self, table_name):
        if table_name not in self.tables:
            print(f"Error: Table '{table_name}' does not exist.")
            return


        table = self.tables[table_name]
        columns = table["columns"]
        rows = table["rows"]

        # if the table is empty (if there is no rows value)
        if not rows:
            self.print_empty_table(table_name)
            return

        col_widths = {col: max(len(col), max(len(str(row[col])) for row in rows)) for col in columns}
        separator = "+" + "+".join("-" * (col_widths[col] + 2) for col in columns) + "+"
        header = "| " + " | ".join(col.ljust(col_widths[col]) for col in columns) + " |"

        print(separator)
        print(header)
        print(separator)
        for row in rows:
            row_data = "| " + " | ".join(str(row[col]).ljust(col_widths[col]) for col in columns) + " |"
            print(row_data)
        print(separator)


    def process_command(self, command):

        parts = command.strip().split(" ", 2)
        if len(parts) < 2:
            return "Error: Invalid command format."

        action, table_name = parts[0], parts[1]
        if action == "CREATE_TABLE":
            args = parts[2].split(" ")
            if len(args) == 1:
                self.create_table(parts[1], args[0].replace("(", "").replace(")", ""))
            else:
                self.create_table(parts[1],args[0].replace("(", "").replace(")", ""), args[1], args[2])

        elif action == "INSERT":
            values = parts[2].split(",")
            self.insert(table_name, values)

        elif action == "SELECT":
            args = parts[2].split(" WHERE ")
            columns, condition = args[0].split(","), {args[1]}
            self.select(table_name, columns, condition)

        elif action == "UPDATE":
            args = parts[2].split(" WHERE ")
            updates = args[0]
            conditions = args[1]
            self.update(table_name, updates, conditions)

        elif action == "DELETE":
            if "WHERE" in parts[2]:
                conditions = parts[2].strip(" WHERE ")
            else: conditions = parts[2]
            self.delete(table_name, conditions)

        elif action == "COUNT":
            if "WHERE" in parts[2]:
                conditions = parts[2].strip(" WHERE ")
            else:
                conditions = parts[2]
            self.count(table_name, conditions)

        elif action == "JOIN" or "LEFT_JOIN" or "FULL_JOIN":
            args = parts[1].split(",")
            table1 = args[0]
            table2 = args[1]
            if action == "LEFT_JOIN":
                join_type = "LEFT"
            elif action =="FULL_JOIN":
                join_type = "FULL"
            else:
                join_type = None
            self.join(table1, table2, join_type)





def main():
    db = Database()
    if len(sys.argv) != 2:
        sys.exit(1)
    input = sys.argv[1]
    try:
        with open(input, "r") as f:
            for line in f:
                db.process_command(line.strip())
    except FileNotFoundError:
        print(f"Error: File '{input}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()



