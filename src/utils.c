#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include "utils.h"

static bool keyState[256];
static int keyDownCount = 0;

void addKeyDown(int key) {
    if (!keyState[key]) {
        keyState[key] = true;
        keyDownCount++;
    }
}

void addKeyUp(int key){
    if (keyState[key]) {
        keyState[key] = false;
        keyDownCount--;
        if (keyDownCount < 0)
            keyDownCount = 0;
    }
}

void addController(int cont, int value)
{
    if (!hasStarted) {
        if (cont == 67 && value == 0) {
            playlast();
        }
    }
}
  
bool areKeysDown() {
    return keyDownCount>0;
}

double timediff(struct timespec* begin, struct timespec* end) {
    double diff = (end->tv_nsec - begin->tv_nsec) / 1000000000.0 +
            (double)(end->tv_sec  - begin->tv_sec);
    return diff;
}

void ledon(bool on) {
    char buf[10];
    sprintf(buf, "ledon %d", on);
    system(buf);
}

void playlast() {
    system("playlast.sh");
}
