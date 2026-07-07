z= {'columns': ['id', 'name', 'age', 'major'], 'rows': [{'id': '1', 'name': 'John Doe', 'age': '20', 'major': 'SE'}, {'id': '2', 'name': 'Jane Smith', 'age': '22', 'major': 'EE'}, {'id': '3', 'name': 'Bob Wilson', 'age': '21', 'major': 'CS'}, {'id': '3', 'name': 'Ted Wilson', 'age': '21', 'major': 'CS'}]}

def table(table):
    list = []
    for a ,b in table.items():
        list.append(b)
    print(f"{list[0]}\n")

    for l in list[1]:
        print(f"{l}\n")


table(z)