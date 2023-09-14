#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdbool.h>


#ifdef DEBUG
    #define DEBUG_STR(var) { printf("DEBUG STR %s: (%s)\n", #var, var) }
    #define DEBUG_CSV_LINE(var) { printf("DEBUG CSV-LINE %s: ", #var); print_CSV_Line(var); printf("\n"); }
    #define DEBUG_CSV_FILE(var) { printf("DEBUG CSV-FILE %s:\n", #var); print_CSV_File(var); }
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
    int count;
    int capacity;
} CSV_Line;

typedef struct CSV_File {
    CSV_Line header;
    CSV_Line *items;
    int count;
    int capacity;
} CSV_File;

void print_CSV_Line(CSV_Line line) {
    const char *delim = ", ";
    for (size_t i = 0; i < line.count; i++) {
        printf("%s%s", line.items[i], delim);
    }
    // remove final delim
    for (size_t i = 0; i < strlen(delim); i++) printf("\b");
    for (size_t i = 0; i < strlen(delim); i++) printf(" ");
}
void print_CSV_File(CSV_File file) {
    print_CSV_Line(file.header);
    // dont know why we need this. think the header is weird
    printf("\r");
    for (size_t i = 0; i < file.count; i++) {
        // line number
        printf("%d: ", i);
        print_CSV_Line(file.items[i]);
        printf("\n");
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
    FILE *ptr;
    char str_buff[256];

    // TODO: check if the csv file is valid

    ptr = fopen(input_file, "r+");
    if (ptr == NULL) {
        printf("file can't be opened\n");
        exit(-1);
    }

    // get headers
    fgets(str_buff, 256, ptr);
    result.header = string_to_CSV_Line(str_buff);
    DEBUG_CSV_LINE(result.header);


    while (fgets(str_buff, 256, ptr) != NULL) {
        assert(strlen(str_buff) < 256 && "csv line length longer than buffer");
        assert(str_buff[strlen(str_buff) - 1] == '\n' && "csv line separated by tabs");

        // trim whitespace
        str_buff[strlen(str_buff) - 1] = '\0';

        CSV_Line line = string_to_CSV_Line(str_buff);
        // DEBUG_CSV_LINE(line);
        da_append(&result, line);
    }

    fclose(ptr);

    return result;
}


int main() {
    printf("Hello, World!\n");

    // const char *file_path = "SampleVitalsLog1.csv";
    const char *file_path = "nathanhall1_vitals_2023-09-14_08-48-161.csv";
    
    // const char *output_path = "formatted.csv";

    CSV_File input_csv = csv_to_CSV_File(file_path);
    DEBUG_CSV_FILE(input_csv);

    return 0;
}