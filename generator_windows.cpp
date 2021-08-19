#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>
#include <sysinfoapi.h>
#include <timezoneapi.h>


/* FILETIME of Jan 1 1970 00:00:00. */
static const unsigned __int64 epoch = ((unsigned __int64)116444736000000000ULL);


typedef struct {
    int width;
    int height;
    int size;
    int start;
    int* next;
} Model;

typedef struct {
    int width;
    int height;
    int size;
    int* data;
} Grid;

typedef struct {
    int start;
    int end;
} Group;



int rand_int(int n) {
    int result;
    while (n <= (result = rand() / (RAND_MAX / n)));
    return result;
}

double rand_double() {
    return (double)rand() / (double)RAND_MAX;
}

int rand_neighbor(int width, int height, int index) {
    int x = index % width;
    int y = index / width;
    while (1) {
        int dx = rand_int(3) - 1;
        int dy = rand_int(3) - 1;
        if (dx == 0 && dy == 0) {
            continue;
        }
        int nx = x + dx;
        int ny = y + dy;
        if (nx < 0 || nx >= width) {
            continue;
        }
        if (ny < 0 || ny >= height) {
            continue;
        }
        return ny * width + nx;
    }
}

void display(int width, int height, int* grid) {
    int size = width * height;
    for (int i = 0; i < size; i++) {
        printf("%d,", grid[i]);
    }
}

void gen_init(Model* model, int width, int height) {
    int size = width * height;
    model->width = width;
    model->height = height;
    model->size = size;
    model->start = rand_int(size);
    model->next = (int *) calloc(size, sizeof(int));
}

void gen_randomize(Model* model) {
    for (int i = 0; i < model->size; i++) {
        model->next[i] = rand_neighbor(model->width, model->height, i);
    }
}

void gen_uninit(Model* model) {
    free(model->next);
}

int gen_extract(Model* model, int* grid) {
    for (int i = 0; i < model->size; i++) {
        grid[i] = 0;
    }
    int index = model->start;
    int number = 1;
    int result = 0;
    while (grid[index] == 0) {
        result++;
        grid[index] = number++;
        index = model->next[index];
    }
    return result;
}


int gen_energy(Model* model) {
    int* grid = (int*)calloc(model->size, sizeof(int));
    int count = gen_extract(model, grid);
    return model->size - count;
}

int gen_do_move(Model* model) {
    int index = rand_int(model->size);
    int before = model->next[index];
    int after;
    do {
        after = rand_neighbor(model->width, model->height, index);
    } while (after == before);
    model->next[index] = after;
    return (index << 16) | before;
}

void gen_undo_move(Model* model, int undo_data) {
    int index = (undo_data >> 16) & 0xffff;
    int value = undo_data & 0xffff;
    model->next[index] = value;
}

void gen_copy(Model* dst, Model* src) {
    dst->width = src->width;
    dst->height = src->height;
    dst->size = src->size;
    dst->start = src->start;
    for (int i = 0; i < src->size; i++) {
        dst->next[i] = src->next[i];
    }
}

int gen_anneal(Model* model, double max_temp, double min_temp, int steps) {
    Model _best;
    Model* best = &_best;
    gen_init(best, model->width, model->height);
    gen_copy(best, model);
    double factor = -log(max_temp / min_temp);
    int energy = gen_energy(model);
    int previous_energy = energy;
    int best_energy = energy;
    for (int step = 0; step < steps; step++) {
        double temp = max_temp * exp(factor * step / steps);
        int undo_data = gen_do_move(model);
        energy = gen_energy(model);
        double change = energy - previous_energy;
        if (change > 0 && exp(-change / temp) < rand_double()) {
            gen_undo_move(model, undo_data);
        }
        else {
            previous_energy = energy;
            if (energy < best_energy) {
                best_energy = energy;
                gen_copy(best, model);
                if (energy <= 0) {
                    break;
                }
            }
        }
    }
    gen_copy(model, best);
    gen_uninit(best);
    return best_energy;
}

void gen(int width, int height, int* output) {
    Model _model;
    Model* model = &_model;
    while (1) {
        gen_init(model, width, height);
        gen_randomize(model);
        int energy = gen_anneal(model, 10, 0.1, 100000);
        if (energy == 0) {
            gen_extract(model, output);
        }
        gen_uninit(model);
        if (energy == 0) {
            break;
        }
    }
}


void solver_lookup(Grid* grid, int* lookup) {
    for (int i = 0; i < grid->size + 1; i++) {
        lookup[i] = -1;
    }
    for (int i = 0; i < grid->size; i++) {
        lookup[grid->data[i]] = i;
    }
}

void solver_copy(Grid* dst, Grid* src) {
    dst->width = src->width;
    dst->height = src->height;
    dst->size = src->size;
    for (int i = 0; i < src->size; i++) {
        dst->data[i] = src->data[i];
    }
}

int solver_helper(
    Grid* grid, Grid* output, int* lookup, Group* groups,
    int n_groups, int index) {
    if (index == n_groups) {
        int done = 1;
        for (int i = 0; i < n_groups; i++) {
            Group* group = groups + i;
            if (group->start <= group->end) {
                done = 0;
                break;
            }
        }
        if (done) {
            int count = grid->size;
            for (int i = 0; i < grid->size; i++) {
                if (grid->data[i]) {
                    count--;
                }
            }
            if (count) {
                return 0;
            }
            else {
                solver_copy(output, grid);
                return 1;
            }
        }
        else {
            int * new_lookup = (int *) calloc(grid->size + 1, sizeof(int));
            solver_lookup(grid, new_lookup);
            return solver_helper(grid, output, new_lookup, groups, n_groups, 0);
        }
    }
    Group* group = groups + index;
    if (group->start > group->end) {
        return solver_helper(grid, output, lookup, groups, n_groups, index + 1);
    }
    else {
        int result = 0;
        int i = lookup[group->start - 1];
        group->start++;
        int x = i % grid->width;
        int y = i / grid->width;
        int k = lookup[group->start];
        int kx = -1;
        int ky = -1;
        if (k >= 0) {
            kx = k % grid->width;
            ky = k / grid->height;
        }
        for (int dy = -1; dy <= 1; dy++) {
            for (int dx = -1; dx <= 1; dx++) {
                if (dx == 0 && dy == 0) {
                    continue;
                }
                int nx = x + dx;
                int ny = y + dy;
                if (nx < 0 || nx >= grid->width) {
                    continue;
                }
                if (ny < 0 || ny >= grid->height) {
                    continue;
                }
                int j = ny * grid->width + nx;
                if (grid->data[j]) {
                    continue;
                }
                if (k >= 0) {
                    int kdx = abs(nx - kx);
                    int kdy = abs(ny - ky);
                    if (kdx > 1 || kdy > 1) {
                        continue;
                    }
                }
                grid->data[j] = group->start - 1;
                result += solver_helper(
                    grid, output, lookup, groups, n_groups, index + 1);
                grid->data[j] = 0;
                if (result > 1) {
                    break;
                }
            }
        }
        group->start--;
        return result;
    }
}

int
gettimeofday(struct timeval* tp, struct timezone* tzp)
{
    FILETIME    file_time;
    SYSTEMTIME  system_time;
    ULARGE_INTEGER ularge;

    GetSystemTime(&system_time);
    SystemTimeToFileTime(&system_time, &file_time);
    ularge.LowPart = file_time.dwLowDateTime;
    ularge.HighPart = file_time.dwHighDateTime;

    tp->tv_sec = (long)((ularge.QuadPart - epoch) / 10000000L);
    tp->tv_usec = (long)(system_time.wMilliseconds * 1000);

    return 0;
}

int main(int argc, char** argv) {
    struct timeval tv;
    int width, height;

    if (argc != 3) {
        return -1;
    }
    else {
        width = (int)strtoul(argv[1], NULL, 10);
        height = (int)strtoul(argv[2], NULL, 10);
    }

    gettimeofday(&tv, NULL);
    srand((tv.tv_sec * 1000) + (tv.tv_usec / 1000));

    int * output = (int *) calloc(width * height, sizeof(int));
    gen(width, height, output);
    display(width, height, output);
    return 0;
}
