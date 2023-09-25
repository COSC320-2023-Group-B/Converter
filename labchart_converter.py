import csv

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

class labchart_CSV:
	DELIMITER = '\t'
	NEW_LINE = '\n'

	def __init__(self, filename):
		if not labchart_CSV.valid_csv(filename):
			raise RuntimeError("CSV is not of correct format")
		
		loaded_csv = load_csv(filename)
		
		self._data = {}

		for header in loaded_csv["headers"]:
			self._data[header] = loaded_csv[header]
			# shorten data for testing
			self._data[header] = self._data[header][:10]

		self.header_feild_names = (
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
		
		self.header_feild: dict[str, tuple] = {
			"Interval": (1, "ms"),
			"ExelDateTime": ("GET", "DATE", "TIME"),
			"TimeFormat": ("StartOfBlock",),
			# "DateFormat": (), # dont know how, something with the date time
			"ChannelTitle": (
				"Systolic (mmHg)",
				"Diastolic (mmHg)",
				"MAP (mmHg)",
				"HeartRate (bpm)",
				"Respiration (Bpm)",
				"AS",
				"SQE"
			),
			"Range": (
				(1.0, "mmHg"),
				(1.0, "mmHg"),
				(1.0, "mmHg"),
				(1.0, "bpm"),
				(1.0, "Bpm"),
				(1.0, "AS"),		# Fix This
				(1.0, "SQE"),	# Fix This
			),
		}
		# fill with stars, gonna have to fix this
		for header in ["UnitName", "TopValue", "BottomValue"]:
			self.header_feild[header] = ["*" for _ in range(len(self.header_feild["ChannelTitle"]))]


	@staticmethod
	def valid_csv(filename):
		# Validate header to determine if valid file
		expected_header = ["Date", "Time", "Systolic (mmHg)", "Diastolic (mmHg)", "MAP (mmHg)", "HeartRate (bpm)", "Respiration (Bpm)", "AS", "SQE", "TimeStamp (mS)"]
		with open(filename, 'r') as file:
			reader = csv.reader(file)
			header = next(reader, None)
			if header != expected_header:
				return False
		return True
	
	def save_to_file(self, filepath):
		with open(filepath, 'w') as file:
			file.write("hello world" + labchart_CSV.NEW_LINE)
			file.write("here world")

if __name__ == "__main__":
	input_file = "./csv files/nathanhall1_vitals_2023-09-14_08-48-161.csv"
	output_file = "./test.txt"

	labchart_object = labchart_CSV(input_file)
	labchart_object.save_to_file(output_file)
	
