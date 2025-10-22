#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define the size of the memory buffers in bytes.
#define BUFFER_SIZE 10000
// The pattern string to fill the buffer.
const char* PATTERN = "abcdef";
// The length of the pattern string.
const size_t PATTERN_LEN = 6;

int main() {
    // --- 1. Allocate memory for the two buffers ---
    // Using `malloc` to allocate memory on the heap for large buffers.
    char* source_buffer = (char*)malloc(BUFFER_SIZE * sizeof(char));
    char* dest_buffer = (char*)malloc(BUFFER_SIZE * sizeof(char));

    // Check if memory allocation was successful.
    if (source_buffer == NULL || dest_buffer == NULL) {
        perror("Failed to allocate memory");
        // Free any memory that was successfully allocated before exiting.
        free(source_buffer);
        free(dest_buffer);
        return 1;
    }

    // --- 2. Fill the source buffer with the repeating pattern ---
    printf("Filling source buffer with repeating \"%s\"...\n", PATTERN);
    
    // Use a loop to copy the pattern repeatedly until the buffer is full.
    // This is more explicit than using `memset` and then `memcpy`.
    for (int i = 0; i < BUFFER_SIZE; i += PATTERN_LEN) {
        // The number of characters to copy in this iteration.
        size_t chars_to_copy = PATTERN_LEN;
        // If we are at the end of the buffer, copy only the remaining bytes.
        if (i + PATTERN_LEN > BUFFER_SIZE) {
            chars_to_copy = BUFFER_SIZE - i;
        }
        memcpy(source_buffer + i, PATTERN, chars_to_copy);
    }
    printf("Source buffer filled.\n");

    // --- 3. Use memmove to copy data to the destination buffer ---
    printf("Using memmove to copy %d bytes from source to destination...\n", BUFFER_SIZE);
    
    // memmove is used here. It's a safer alternative to `memcpy` as it
    // correctly handles cases where the source and destination memory regions
    // might overlap. In this program, they do not, but it's good practice.
    memmove(dest_buffer, source_buffer, BUFFER_SIZE);
    
    printf("Copy complete.\n");

    // --- 4. Print parts of both buffers for verification ---
    printf("\n--- Verifying content ---\n");

    // Print the first 50 characters of the source buffer.
    printf("Source buffer (first 50 bytes): ");
    for (int i = 0; i < 50; ++i) {
        printf("%c", source_buffer[i]);
    }
    printf("\n");

    // Print the first 50 characters of the destination buffer.
    printf("Destination buffer (first 50 bytes): ");
    for (int i = 0; i < 50; ++i) {
        printf("%c", dest_buffer[i]);
    }
    printf("\n");

    // --- 5. Clean up allocated memory ---
    free(source_buffer);
    free(dest_buffer);
    printf("\nMemory freed. Program finished.\n");

    return 0;
}
#include <stdio.h>
#include <string.h>

int main2() {
    // A character array (string) to store the number.
    // 10 characters is more than enough for a number up to 100 and the null terminator.
    char numberAsString[10];

    // Loop from 1 to 100
    for (int i = 1; i <= 100; i++) {
        // Use sprintf to print the integer 'i' into the string 'numberAsString'.
        // This is a standard and portable way to convert an int to a string.
        // It's similar to printf, but it writes to a string instead of the console.
        sprintf(numberAsString, "%d", i);

        // Print both the integer and its string representation to the console.
        printf("Integer: %d, String: %s\n", i, numberAsString);
    }

    return 0;
}
