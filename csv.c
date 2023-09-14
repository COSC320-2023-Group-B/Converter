#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdbool.h>


#ifdef DEBUG
    #define DEBUG_STR(var) { printf("DEBUG STR %s: (%s)\n", #var, var); }
    #define DEBUG_CSV_LINE(var) { printf("DEBUG CSV-LINE %s: ", #var); print_CSV_Line(var); printf("\n"); }
    #define DEBUG_CSV_FILE(var) { printf("DEBUG CSV-FILE %s:\n", #var); print_CSV_File(var, true); }
#else
    #define DEBUG_STR(var)
    #define DEBUG_CSV_LINE(var)
    #define DEBUG_CSV_FILE(var)
#endif

// thanks Tsoding
#define DA_INIT_CAP 32
#define da_append(da, item)                                                          \
    do {                                                                             \
        if ((da)->count >= (da)->capacity) {                                         \
            (da)->capacity = (da)->capacity == 0 ? DA_INIT_CAP : (da)->capacity*2;   \
            (da)->items = realloc((da)->items, (da)->capacity*sizeof(*(da)->items)); \
            assert((da)->items != NULL && "Buy more RAM lol");                       \
        }                                                                            \
                                                                                     \
        (da)->items[(da)->count++] = (item);                                         \
    } while (0)


typedef struct CSV_Line {
    const char **items;
    size_t count;
    size_t capacity;
} CSV_Line;

typedef struct CSV_File {
    CSV_Line header;
    CSV_Line *items;
    size_t count;
    size_t capacity;
} CSV_File;

const char *CSV_Line_to_string(CSV_Line line, const char *delim) {
    assert(line.count > 0 && "cannot get string of empty line");

    const char *str = calloc(256, sizeof(char));
    char *str_ptr = (char *) str;

    assert(str != NULL && "Buy more ram lol");

    strcpy(str_ptr, line.items[0]); str_ptr += strlen(line.items[0]);
    
    for (size_t i = 1; i < line.count; i++) {
        strcpy(str_ptr, delim); str_ptr += strlen(delim);
        strcpy(str_ptr, line.items[i]); str_ptr += strlen(line.items[i]);

        assert(str_ptr - str < 256 && "buffer not big enough");
    }
    
    return str;
}

void print_CSV_Line(CSV_Line line) {
    const char *str = CSV_Line_to_string(line, ", ");
    fprintf(stdout, "%s", str);
}
void print_CSV_File(CSV_File file, bool line_numbers) {
    print_CSV_Line(file.header);
    // dont know why we need this. think the header is weird
    fprintf(stdout, "\r");
    for (size_t i = 0; i < file.count; i++) {
        // line number
        if (line_numbers) fprintf(stdout, "%d: ", i);
        print_CSV_Line(file.items[i]);
        fprintf(stdout, "\n");
    }
}

CSV_Line string_to_CSV_Line(char *line) {
    CSV_Line result = {0};
    const char delim[2] = ",";
    char *token;

    // DEBUG_STR(line);

    token = strtok(line, delim);
    while (token != NULL) {
        // DEBUG_STR(token);

        // dont worry about freeing stuff        
        char *new_string = calloc(strlen(token) + 1, sizeof(char));
        strcpy(new_string, token);
        da_append(&result, new_string);
        token = strtok(NULL, delim);
    }

    return result;
}

CSV_File csv_to_CSV_File(const char *input_file) {
    CSV_File result = {0};
    FILE *fptr;
    char str_buff[256];

    // TODO: check if the csv file is valid

    fptr = fopen(input_file, "r+");
    if (fptr == NULL) {
        printf("file can't be opened\n");
        exit(-1);
    }

    // get headers
    fgets(str_buff, 256, fptr);
    str_buff[strlen(str_buff) - 1] = '\0';
    result.header = string_to_CSV_Line(str_buff);
    DEBUG_CSV_LINE(result.header);


    while (fgets(str_buff, 256, fptr) != NULL) {
        assert(strlen(str_buff) < 256 && "csv line length longer than buffer");
        assert(str_buff[strlen(str_buff) - 1] == '\n' && "csv line separated by tabs");

        // trim whitespace
        str_buff[strlen(str_buff) - 1] = '\0';

        CSV_Line line = string_to_CSV_Line(str_buff);
        // DEBUG_CSV_LINE(line);
        da_append(&result, line);
    }

    fclose(fptr);

    return result;
}

void CSV_File_to_csv(CSV_File file, const char *out_path) {
    FILE *fptr;
    const char *buff;
    const char *delim = ",";

    fptr = fopen(out_path, "w");
    assert(fptr != NULL && "Could not create file");

    // put header
    buff = CSV_Line_to_string(file.header, delim);
    fprintf(fptr, "%s\n", buff);

    buff = CSV_Line_to_string(file.items[0], delim);
    fprintf(fptr, "%s\n", buff);

    for (size_t i = 1; i < file.count; i++) {
        buff = CSV_Line_to_string(file.items[i], delim);
        fprintf(fptr, "%s\n", buff);
    }
    

    fclose(fptr);
}
