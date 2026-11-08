#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define ARRAY_SIZE 262144
#define ITERATIONS 20

int main(void)
{
    int *array = malloc(ARRAY_SIZE * sizeof(int));

    if (array == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }

    for (int i = 0; i < ARRAY_SIZE; i++) {
        array[i] = i % 100;
    }

    volatile uint64_t sum = 0;

    for (int iteration = 0; iteration < ITERATIONS; iteration++) {
        for (int i = 0; i < ARRAY_SIZE; i++) {
            sum += array[i];
        }
    }

    printf("Memory benchmark completed.\n");
    printf("Array size: %zu bytes\n",
           (size_t)ARRAY_SIZE * sizeof(int));
    printf("Iterations: %d\n", ITERATIONS);
    printf("Checksum: %llu\n",
           (unsigned long long)sum);

    free(array);
    return 0;
}
