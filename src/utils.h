#include <stdbool.h>
#include <time.h>

void addKeyDown(int key);
void addKeyUp(int key);
bool areKeysDown();

double timediff(struct timespec * begin, struct timespec * end);
void ledon(bool on);
