#include <stdio.h>

#include "csv.c"

CSV_File normalize_Timestamps(CSV_File input_file) {
    CSV_File output_file = {0};

    // TODO: check if csv is a valid caretaker csv
    // same headers
    output_file.header = input_file.header;


    // get first timestamp to normalize by
    CSV_Line first_line = input_file.items[0];

    // assume "TimeStamp (mS)" is the last item
    int first_timestamp = atoi(first_line.items[first_line.count - 1]);
    DEBUG_INT(first_timestamp);


    // for every line in the input file
    for (size_t i = 0; i < input_file.count; i++) {
        CSV_Line new_line = {0};
        CSV_Line *current_line = &input_file.items[i];

        // copy the other information into the new line
        for (size_t j = 0; j < current_line->count - 1; j++) {
            // these are the same pointers, dont free the input file and we'll be good
            da_append(&new_line, current_line->items[j]);
        }

        // normalize the timestamp
        int timestamp = atoi(current_line->items[current_line->count - 1]);
        int normalized_timestamp = timestamp - first_timestamp;

        char *timestamp_string = calloc(256, sizeof(char));
        sprintf(timestamp_string, "%d", normalized_timestamp);
        // DEBUG_STR(timestamp_string);

        da_append(&new_line, timestamp_string);
        
        da_append(&output_file, new_line);
    }

    DEBUG_CSV_FILE(output_file);
    
    return output_file;
}


int main() {
    const char *file_path = "SampleVitalsLog1.csv";
    // const char *file_path = "nathanhall1_vitals_2023-09-14_08-48-161.csv";
    
    const char *output_path = "formatted.csv";

    CSV_File input_csv = csv_to_CSV_File(file_path);
    // DEBUG_CSV_FILE(input_csv);

    // const char *string = CSV_Line_to_string(input_csv.header, ", ");
    CSV_File output_csv = normalize_Timestamps(input_csv);

    CSV_File_to_csv(output_csv, output_path);

    return 0;
}