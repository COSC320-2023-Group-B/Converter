#include <stdio.h>

#include "csv.c"

int main() {
    // const char *file_path = "SampleVitalsLog1.csv";
    const char *file_path = "nathanhall1_vitals_2023-09-14_08-48-161.csv";
    
    const char *output_path = "formatted.csv";

    CSV_File input_csv = csv_to_CSV_File(file_path);
    // DEBUG_CSV_FILE(input_csv);

    const char *string = CSV_Line_to_string(input_csv.header, ", ");

    CSV_File_to_csv(input_csv, output_path);

    return 0;
}