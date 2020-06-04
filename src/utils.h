#include <stdbool.h>
#include <time.h>

void addKeyDown(int key);
void addKeyUp(int key);
void addController(int cont, int value);
bool areKeysDown();

double timediff(struct timespec * begin, struct timespec * end);
void ledon(bool on);
void playlast();
void stopPlayback();

bool hasStarted;
