import csv
import tkinter as tk
from tkinter import filedialog, messagebox


def main():
	# Inform the user about the input file selection
	tk.messagebox.showinfo("Select Input File", "Please select a CSV file to load.")

	# Load the data
	inputPath = select_input_csv()
	dates, times, systolics, diastolics, maps, heart_rates, respirations, as_values, sqes, timestamps = load_file(inputPath)

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


def load_file(filename):
	# Initialize arrays to store data
	dates = []
	times = []
	systolics = []
	diastolics = []
	maps = []
	heart_rates = []
	respirations = []
	as_values = []
	sqes = []
	timestamps = []

	with open(filename, 'r') as file:
		reader = csv.reader(file)

		# Skip the header
		next(reader)

		# Process each row and store values in arrays
		for row in reader:
			dates.append(row[0])
			times.append(row[1])
			systolics.append(int(row[2]))
			diastolics.append(int(row[3]))
			maps.append(int(row[4]))
			heart_rates.append(int(row[5]))
			respirations.append(int(row[6]))
			as_values.append(int(row[7]))
			sqes.append(int(row[8]))
			timestamps.append(int(row[9]))

	return dates, times, systolics, diastolics, maps, heart_rates, respirations, as_values, sqes, timestamps


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
