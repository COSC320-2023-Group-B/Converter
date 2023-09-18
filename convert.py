import csv
import tkinter as tk
from tkinter import filedialog, messagebox


def main():
	# Inform the user about the input file selection
	tk.messagebox.showinfo("Select Input File", "Please select a CSV file to load.")

	# Load the data
	inputPath = select_input_csv()
	# dates, times, systolics, diastolics, maps, heart_rates, respirations, as_values, sqes, timestamps = load_csv(inputPath)
	csv_file = load_csv(inputPath)

	# botch until someone fixes this 
	dates, times, systolics, diastolics, maps, heart_rates, respirations, as_values, sqes, timestamps = csv_file["Date"], csv_file["Time"], csv_file["Systolic (mmHg)"], csv_file["Diastolic (mmHg)"], csv_file["MAP (mmHg)"], csv_file["HeartRate (bpm)"], csv_file["Respiration (Bpm)"], csv_file["AS"], csv_file["SQE"], csv_file["TimeStamp (mS)"]
	# make all ints
	timestamps = [int(t) for t in timestamps]

	# Adjust timestamps
	adjusted_timestamps = []
	for i in range(len(timestamps)):
		adjusted_timestamps.append(timestamps[i] - timestamps[0])

	# Inform the user about the output file selection
	tk.messagebox.showinfo("Select Output File", "Please choose a location and filename to save the formatted CSV data.")

	# Format the wanted data into a list of lists
	data = []
	for i in range(len(adjusted_timestamps)):
		data.append([adjusted_timestamps[i], systolics[i], diastolics[i], maps[i], heart_rates[i], respirations[i], as_values[i], sqes[i]])

	# Save the data
	outputPath = select_output_csv()
	header = ["Adjusted Timestamp", "Systolic", "Diastolic", "MAP", "Heart Rate", "Respiration", "AS Value", "SQE"]
	save_file(outputPath, header, data)

	# Inform the user that the process is complete
	tk.messagebox.showinfo("Process Complete", "The CSV data has been successfully formatted and saved!")


def load_csv(filename):
	# initialise csvs
	csv_file = {}

	with open(filename, 'r') as file:
		reader = csv.reader(file)

		# get the header
		csv_file["headers"] = next(reader)
		# initialize headers in csv dict
		for header in csv_file["headers"]:
			csv_file[header] = []

		# Process each row and store values in arrays
		for row in reader:
			for value, header in zip(row, csv_file["headers"]):
				csv_file[header].append(value)

	return csv_file


# filename string, header string, list of data arrays
def save_file(filename, header, data):
	with open(filename, 'w', newline='') as file:
		writer = csv.writer(file)

		# Write the header
		writer.writerow(header)

		# Write the data
		for row in data:
			writer.writerow(row)


def select_input_csv():
	# Create a root window and immediately hide it
	root = tk.Tk()
	root.withdraw()

	# Expected header for the CSV file
	expected_header = ["Date", "Time", "Systolic (mmHg)", "Diastolic (mmHg)", "MAP (mmHg)", "HeartRate (bpm)",
					   "Respiration (Bpm)", "AS", "SQE", "TimeStamp (mS)"]

	while True:
		# Show the file selection dialog
		file_path = filedialog.askopenfilename(
			title="Select a CSV file", filetypes=[("CSV files", "*.csv")])

		# If the user cancels the file dialog, return None
		if not file_path:
			print("No file selected")
			exit()

		# Check if the selected file has the expected header
		with open(file_path, 'r') as file:
			reader = csv.reader(file)
			header = next(reader, None)  # Read the first line (header)

			if header == expected_header:
				return file_path
			else:
				tk.messagebox.showerror(
					"Error", "The selected file does not have the expected header. Please select a valid CSV file.")


def select_output_csv():
	# Create a root window and immediately hide it
	root = tk.Tk()
	root.withdraw()

	# Show the save file dialog
	file_path = filedialog.asksaveasfilename(
		title="Save CSV file",
		filetypes=[("CSV files", "*.csv")],
		defaultextension=".csv"
	)

	# If the user cancels the save file dialog, return None
	if not file_path:
		print("No output file selected")
		exit()

	return file_path

main()
