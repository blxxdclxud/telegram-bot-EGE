spreadsheet_id = input("Введите id новой таблицы:")
personal_id = input("Введите id листа 'Personal':")
general_id = input("Введите id листа 'General':")

with open("./data/config.txt", 'w') as file:
    file.write("SPREADSHEET_ID=" + spreadsheet_id + "\n")
    file.write("PERSONAL_SHEET_ID=" + personal_id + "\n")
    file.write("GENERAL_SHEET_ID=" + general_id + "\n")
