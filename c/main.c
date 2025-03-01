#include <stddef.h>
#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>

#include <sys/time.h>
#include <unistd.h>

// Nonesense to make comile and intellisense work
#ifdef __USE_POSIX199309
    #include <time.h>
#else
    #include <linux/time.h>
#endif

const size_t num_deltas = 10000;

struct DeltaArgs {
    size_t index;
    unsigned long *data;
    double *sys_data;
};

unsigned long time_delta_nanos(struct timespec *start, struct timespec *end) {

    unsigned long seconds_delta = end->tv_sec - start->tv_sec;
    unsigned long nanos_delta = end->tv_nsec - start->tv_nsec;

    return seconds_delta * 1e9 + nanos_delta;
}

void *run_sleep(void* args) {
    struct DeltaArgs *d = (struct DeltaArgs*) args;

    struct timespec start, end;
    struct timespec sys_start, sys_end;

    clock_gettime(CLOCK_REALTIME, &sys_start);
    clock_gettime(CLOCK_MONOTONIC, &start);
    usleep(1000); // Sleep for 1 millisecond
    clock_gettime(CLOCK_MONOTONIC, &end);
    clock_gettime(CLOCK_REALTIME, &sys_end);

    *d->data = time_delta_nanos(&start, &end) - 1e6;
    //Sys time delta in milliseconds
    *d->sys_data = (time_delta_nanos(&sys_start, &sys_end) / 1e3) - 1000;

    free(d);
}

FILE* open_blank_file(char* path) {

    FILE* fd = fopen(path, "w");
    fclose(fd);

    fd = fopen(path, "a");
    return fd;
}

void create_deltas() {
    unsigned long deltas[num_deltas];
    double sys_deltas[num_deltas];

    pthread_t threads[num_deltas];

    for (size_t i = 0; i < num_deltas; i++)
    {

        struct DeltaArgs *d = malloc(sizeof(struct DeltaArgs));
        d->index = i;
        d->data = &deltas[i];
        d->sys_data = &sys_deltas[i];
        pthread_create(&threads[i], NULL, run_sleep, d);
    }

    for (size_t i = 0; i < num_deltas; i++)
    {
        pthread_join(threads[i], NULL);
    }

    FILE* fd = open_blank_file("../delta_outs/c_out.txt");
    FILE* sys_fd = open_blank_file("../delta_outs/c_out_sys.txt");
    for (size_t i = 0; i < num_deltas; i++)
    {
        fprintf(fd, "%ld\n", deltas[i]);
        fprintf(sys_fd, "%.4f\n", sys_deltas[i]);
    }
    fclose(fd);
    fclose(sys_fd);
}
unsigned long to_nanos(struct timespec *t) {
    return t->tv_sec * 1000000 + t->tv_nsec;
}
void arithmetic_deltas() {
        //     for (int i = 0; i < 100_000; i++) {
        //     var start = System.nanoTime();
        //     double sum = 0;
        //     sum += 12345000.5;
        //     sum *= 103.12;
        //     long si = (long) sum % Long.MAX_VALUE;
        //     si /= 543212345;
        //     var end = System.nanoTime();
        //     deltas.add(end - start); // Get Delta in Nano Time vs Expected
        // }

    unsigned long deltas[100000];

    for (size_t i = 0; i < 100000; i++)
    {
        struct timespec start, end;
        clock_gettime(CLOCK_MONOTONIC, &start);
        
        double sum = 0;
        sum += 12345000.5;
        sum *= 103.12;
        long si = (long) sum % __LONG_MAX__;
        si /= 543212345;

        clock_gettime(CLOCK_MONOTONIC, &end);

        deltas[i] = time_delta_nanos(&start, &end);

        if (abs(deltas[i]) > 500)
        {
            /* code */
            printf("-----------\nStart Nanos = %ld", to_nanos(&start));
            printf("\nEnd Nanos = %ld\n", to_nanos(&end));
        }
        
    }


    FILE* fd = open_blank_file("../delta_outs/c_out_arithmetic.txt");
    for (size_t i = 0; i < 100000; i++)
    {
        fprintf(fd, "%ld\n", deltas[i]);
    }
    fclose(fd);
}

int main(int argc, char** argv) {
    printf("Hello World!\n");

    arithmetic_deltas();
    // create_deltas();
    return 0;
}
