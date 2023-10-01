import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox

from labchart_converter import convert_CSV_To_Labchart

def lerp(a, b, interp):
	return a + (b-a) * interp

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

def save_csv(filename, header, data):
	with open(filename, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(header)
		writer.writerows(data)

class CSV_conversion_window(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("CSV Converter")
		self.geometry("400x350")
		self.configure(background="#ccc")
		self.wm_resizable(False, False)
		# self.configure(background="#aaf")

		# Initialize variables to store conversion parameters
		self.input_path = tk.StringVar(value="")
		self.output_path = tk.StringVar(value="")
		self.input_path_display = tk.StringVar(value="<No File Selected>")
		self.output_path_display = tk.StringVar(value="<No File Selected>")
		self.is_interpolate = tk.BooleanVar(value=True)
		self.interval = tk.StringVar(value="620")

		# Center the window (roughly)
		posx = self.winfo_screenwidth()//2 - self.winfo_reqwidth()
		posy = self.winfo_screenheight()//2 - self.winfo_reqheight()
		self.geometry("+{}+{}".format(posx, posy))

		# Create widgets
		self.create_widgets()

	def create_widgets(self):
		# input
		tk.Button(self, text="Select Input CSV", command=self.select_input_csv).pack(pady=10)
		tk.Label(self, textvariable=self.input_path_display, bg='#ccc').pack(pady=5)
		# output
		tk.Button(self, text="Select Output CSV",command=self.select_output_csv).pack(pady=10)
		tk.Label(self, textvariable=self.output_path_display, bg='#ccc').pack(pady=5)
		# interpolation checkbox
		tk.Checkbutton(self, variable=self.is_interpolate, text="Interpolate values").pack(pady=10)
		# interpolation interval
		frame = tk.Frame(self)
		tk.Label(frame, text='Interpolation interval (ms):').pack(side = tk.LEFT)
		tk.Entry(frame, textvariable=self.interval).pack(side = tk.RIGHT)
		frame.pack(pady=5)
		# convert
		tk.Button(self, text="Convert", command=self.convert).pack(pady=20)

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

		# # Load the data to calculate the average interval
		# csv_file = load_csv(file_path)
		# timestamps = [int(t) for t in csv_file["TimeStamp (mS)"]]
		# if len(timestamps) > 1:
		# 	total_duration = timestamps[-1] - timestamps[0]
		# 	average_interval = total_duration / (len(timestamps) - 1)
		# 	self.interval.set(f"{average_interval:.2f}")

	def select_output_csv(self):
		file_path = filedialog.asksaveasfilename(title="Save text file", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")], defaultextension=".txt")
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
		
		if not self.interval.get().isdigit():
			messagebox.showerror("Error", "Interval must be an integer (ms).")
			return
		
		inperpolation = int(self.interval.get()) if self.is_interpolate.get() else None

		convert_CSV_To_Labchart(input_path, output_path, inperpolation)

		messagebox.showinfo("Success", "Conversion completed successfully!")


if __name__ == "__main__":
	app = CSV_conversion_window()
	app.mainloop()
