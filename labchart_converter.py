import csv

# constants
DELIMITER = '\t'
NEW_LINE = '\n'
HEADER_FIELD_NAMES = (
	"Interval",
	"ExcelDateTime",
	"TimeFormat",
	"DateFormat",
	"ChannelTitle",
	"Range",
	"UnitName",
	"TopValue",
	"BottomValue",
)

def lerp(a, b, interp):
	return a + (b-a) * interp
def lerp_values_by_time(t1, v1, t2, v2, t3):
	interp = (t3 - t1) / (t2 - t1)
	return lerp(v1, v2, interp)
def lerp_two_rows_by_interp(row1, row2, interp_time):
	t1, t2 = row1[0], row2[0]
	lerped_row = [interp_time]
	for v1, v2 in zip(row1[1:], row2[1:]):
		lerped_row.append(lerp_values_by_time(t1, v1, t2, v2, interp_time))
	return lerped_row


def load_csv(filename):
		csv_file = {}
		with open(filename, 'r') as file:
			reader = csv.reader(file)
			csv_file["headers"] = next(reader)
			for header in csv_file["headers"]:
				csv_file[header] = []
			for row in reader:
				for value, header in zip(row, csv_file["headers"]):
					csv_file[header].append(value)
		return csv_file

def convert_CSV_To_Labchart(input_filename, output_filename, lerp_interval=500):
	if not valid_csv(input_filename):
		raise RuntimeError("CSV is not of correct format")
	
	loaded_csv = load_csv(input_filename)

	header = get_header_information(loaded_csv, lerp_interval)
	
	data = lerp_data(loaded_csv, lerp_interval)

	save_to_file(output_filename, header, data)


def get_header_information(loaded_csv, lerp_interval):
	header_field = {
		"Interval": (f"{lerp_interval} ms",),
		"ExcelDateTime": ("GET", "DATE TIME"),
		"TimeFormat": ("StartOfBlock",),
		"DateFormat": (), # dont know how, something with the date time
		"ChannelTitle": (
			"Systolic",
			"Diastolic",
			"MAP",
			"HeartRate",
			"Respiration",
			"AS",
			"SQE"
		),
		"Range": (
			f"{1.0} mmHg",
			f"{1.0} mmHg",
			f"{1.0} mmHg",
			f"{1.0} bpm",
			f"{1.0} Bpm",
			f"{1.0} AS",	# Fix This
			f"{1.0} SQE",	# Fix This
		),
	}
	# fill with stars, gonna have to fix this
	for header in ["UnitName", "TopValue", "BottomValue"]:
		header_field[header] = ["*" for _ in range(len(header_field["ChannelTitle"]))]
	
	return header_field

def find_closest_timestamps(timestamps: list[int], time: int):
	last_timestamp = max(timestamps, key=lambda t: t * (t < time))
	last_index = timestamps.index(last_timestamp)
	next_index = last_index + 1
	next_timestamp = timestamps[next_index]

	return last_timestamp, next_timestamp

def lerp_data(loaded_csv, lerp_interval):
	csv_headers = loaded_csv["headers"]

	timestamps = [int(t) for t in loaded_csv["TimeStamp (mS)"]]
	adjusted_timestamps = [t - timestamps[0] for t in timestamps]

	# the headers in data, and the order there in
	wanted_headers = ["Systolic (mmHg)", "Diastolic (mmHg)", "MAP (mmHg)", "HeartRate (bpm)", "Respiration (Bpm)", "AS", "SQE"]

	# dont remove the date to keep track of positions
	data = [[adjusted_timestamps[i]] + [int(loaded_csv[header][i]) for header in wanted_headers] for i in range(len(adjusted_timestamps))]


	if lerp_interval is not None:
		lerped_data = []
		timestamps = [entry[0] for entry in data]
		for tick in range(0, adjusted_timestamps[-1], lerp_interval):
			last_timestamp, next_timestamp = find_closest_timestamps(timestamps, tick)
			
			last_index = timestamps.index(last_timestamp)
			next_index = timestamps.index(next_timestamp)
			last_row = data[last_index]
			next_row = data[next_index]

			lerped_data.append(lerp_two_rows_by_interp(last_row, next_row, tick))

		data = lerped_data
	
	return data


def valid_csv(filename):
	# Validate header to determine if valid file
	expected_header = ["Date", "Time", "Systolic (mmHg)", "Diastolic (mmHg)", "MAP (mmHg)", "HeartRate (bpm)", "Respiration (Bpm)", "AS", "SQE", "TimeStamp (mS)"]
	with open(filename, 'r') as file:
		reader = csv.reader(file)
		header = next(reader, None)
		if header != expected_header:
			return False
	return True

def save_to_file(filepath, header, data):
	with open(filepath, 'w') as file:
		# write header
		for header_name in HEADER_FIELD_NAMES:
			file.write(f"{header_name}=")
			for h in header[header_name]:
				file.write(f"{DELIMITER}{h}")
			if len(header[header_name]) == 0:
				file.write(f"{DELIMITER}")
			file.write(f"{NEW_LINE}")
		
		for row in data:
			# write time info
			file.write(f"{row[0]}")
			# write data
			for item in row[1:]:
				file.write(f"{DELIMITER}{item}")
			file.write(f"{NEW_LINE}")


if __name__ == "__main__":
	input_file = "./csv files/nathanhall1_vitals_2023-09-14_08-48-161.csv"
	output_file = "./test.txt"

	convert_CSV_To_Labchart(input_file, output_file)
	
