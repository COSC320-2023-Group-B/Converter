import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox


class CSV_conversion_window(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("CSV Converter")
		self.geometry("300x250")
		self.configure(background="#aaf")

		# Initialize variables to store file paths
		self.input_path = tk.StringVar(value="")
		self.output_path = tk.StringVar(value="")
		self.input_path_display = tk.StringVar(value="")
		self.output_path_display = tk.StringVar(value="")

		# Center the window (roughly)
		posx = self.winfo_screenwidth()//2 - self.winfo_reqwidth()
		posy = self.winfo_screenheight()//2 - self.winfo_reqheight()
		self.geometry("+{}+{}".format(posx, posy))

		# Create widgets
		self.create_widgets()

	def create_widgets(self):
		# input
		tk.Button(self, text="Select Input CSV", command=self.select_input_csv, bg='#faf').pack(pady=10)
		tk.Label(self, textvariable=self.input_path_display, bg='#aaf').pack(pady=5)
		# output
		tk.Button(self, text="Select Output CSV",command=self.select_output_csv, bg='#faf').pack(pady=10)
		tk.Label(self, textvariable=self.output_path_display, bg='#aaf').pack(pady=5)
		# convert
		tk.Button(self, text="Convert", command=self.convert, bg='#faf').pack(pady=20)

	def select_input_csv(self):
		file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])
		if not file_path:
			return

		# Validate header to determine if valid file
		expected_header = ["Date", "Time", "Systolic (mmHg)", "Diastolic (mmHg)", "MAP (mmHg)", "HeartRate (bpm)", "Respiration (Bpm)", "AS", "SQE", "TimeStamp (mS)"]
		with open(file_path, 'r') as file:
			reader = csv.reader(file)
			header = next(reader, None)
			if header != expected_header:
				messagebox.showerror("Invalid File", "The selected file does not have the expected header.")
				return

		self.input_path.set(file_path)
		self.input_path_display.set(os.path.basename(file_path))

	def select_output_csv(self):
		file_path = filedialog.asksaveasfilename(title="Save CSV file", filetypes=[("CSV files", "*.csv")], defaultextension=".csv")
		if file_path:
			self.output_path.set(file_path)
			self.output_path_display.set(os.path.basename(file_path))

	def convert(self):
		input_path = self.input_path.get()
		output_path = self.output_path.get()

		if not input_path:
			messagebox.showerror("Error", "Please select an input file.")
			return			
		if not output_path:
			messagebox.showerror("Error", "Please select an output file.")
			return

		# Load the data
		csv_file = self.load_csv(input_path)

		# Extract and process the data
		timestamps = [int(t) for t in csv_file["TimeStamp (mS)"]]
		adjusted_timestamps = [t - timestamps[0] for t in timestamps]

		# Format the wanted data into a list of lists
		# the [2:-1] is a shorthand, may expand out once we know exactly which data we required, for now we take all but the date and time
		data = [[adjusted_timestamps[i]] + [int(csv_file[header][i]) for header in csv_file["headers"][2:-1]] for i in range(len(adjusted_timestamps))]
		
		def lerp(a, b, interp):
			return a + (b-a) * interp
		interval = 500 # ms
		lerped_data = []
		timestamps = [entry[0] for entry in data]
		for tick in range(0, adjusted_timestamps[-1], interval):
			last_timestamp = min(filter(lambda v, t=tick: (v <= t), timestamps))
			next_timestamp = max(filter(lambda v, t=tick: (v >= t), timestamps))
			last_index = timestamps.index(last_timestamp)
			next_index = timestamps.index(next_timestamp)
			interp = (tick-last_timestamp)/(next_timestamp-last_timestamp)
			lerp_data_entry = [tick]
			for i in range(1, len(data[0])):
				lerp_data_entry.append(int(lerp(data[last_index][i], data[next_index][i], interp)))
			lerped_data.append(lerp_data_entry)


		# Save the data
		header = ["Adjusted Timestamp"] + csv_file["headers"][2:-1]	# [2:-1] is shorthand, see above
		self.save_csv(output_path, header, lerped_data)

		messagebox.showinfo("Success", "Conversion completed successfully!")

	def load_csv(self, filename):
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

	def save_csv(self, filename, header, data):
		with open(filename, 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(header)
			writer.writerows(data)


if __name__ == "__main__":
	app = CSV_conversion_window()
	app.mainloop()
