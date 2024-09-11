def initialize_main_unit_conversion_file(all_units, main_file):
  print("------------------------")
  with open(main_file, "r") as file:
    file_data = file.readlines()[2:]

  for line in file_data:
    unit = line.split(",")
    key = unit[2].strip()
    all_units[key] = {"name": unit[0], "symbol": unit[1], "units": []}

  print("(Main Units): Main File is COMPLETE!")
  
def initialize_sub_unit_conversion_files(all_units, sub_files):
  sub_files_length = len(sub_files)
  sub_file_index = 0

  # For every unit category.
  for unit_key in all_units.keys():
    if sub_file_index + 1 > sub_files_length:
        break

    # Open a sub-unit file for a current unit category.
    sub_unit_file_data = read_all_lines_from_file(sub_files[sub_file_index])
    for line in sub_unit_file_data:
      # Split by "|".This is our seperator for unit name, value, description.
      single_unit_dict = split_single_unit_to_dict(line)
      all_units[unit_key]["units"].append(single_unit_dict)

    print("(Sub Units):", sub_files[sub_file_index], " is COMPLETE!")
    sub_file_index += 1
    print("------------------------\n")

def split_single_unit_to_dict(line):
  single_unit_list = line.split("|")
  single_unit_dict = {"unit": single_unit_list[0], "value": single_unit_list[1]}

  # If unit has description, take it, overwhise write "-".
  if len(single_unit_list) == 3:
    single_unit_dict["desc"] = single_unit_list[2]
  else:
    single_unit_dict["desc"] = "-"

  return single_unit_dict

def read_all_lines_from_file(file):
  file = open(file, "r", encoding='ascii', errors='ignore')
  return file.readlines()

# Initializes currencies.
def initialize_all_currencies(all_units, currency_file):
  file_data = read_all_lines_from_file(currency_file)

  for item in file_data:
    single_currency = {"unit": item, "value": 0, "desc": "N/A"}
    all_units["currencies"]["units"].append(single_currency)