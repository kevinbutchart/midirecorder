#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include "utils.h"

#define DAMPER_PEDAL 64
#define SOSTENATU_PEDAL 66
#define SOFT_PEDAL 67

#define NELEMS(x)  (sizeof(x) / sizeof((x)[0]))

static bool keyState[256];
static int pedalControllers[3] = { DAMPER_PEDAL, SOSTENATU_PEDAL, SOFT_PEDAL };
static bool pedalState[3] = { false, false, false};
static int keyDownCount = 0;
static int pedalDownCount = 0;
static bool isPlaying = false;

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

int getControllerIndex(int controllerNumber) {

    for (int i = 0; i < NELEMS(pedalControllers); ++i) {
        if (pedalControllers[i] == controllerNumber) {
            return i;
        }
    }
    return -1;
}

void setPedalState(int controller, int value) {
    int cindex = getControllerIndex(controller);
    if (cindex != -1) {
        bool pedalDown = value != 0;

        if (pedalDown != pedalState[cindex]) {
            pedalDown? pedalDownCount++ : pedalDownCount--;
            if (pedalDownCount < 0) pedalDownCount=0; // this would be bug!
            pedalState[cindex] = pedalDown;
        }
    }
}


void addController(int cont, int value)
{
    printf("controller: %d value: %d\n", cont, value);
    if (!hasStarted) {
        if (cont == SOSTENATU_PEDAL && value == 0) {
            if (!isPlaying) {
                playlast();
                isPlaying = true;
            } else {
                stopPlayback();
                isPlaying = false;
            }
        }
    }
    setPedalState(cont, value);
}
  
bool areKeysDown() {
    return keyDownCount>0;
}

bool areKeysOrPedalsDown() {
    return keyDownCount>0 || pedalDownCount>0;
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
    system("playlast.sh&");
}
void stopPlayback() {
    system("stopplayback.sh");
}
