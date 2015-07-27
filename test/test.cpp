#include <stdio.h>

int main()
{
  char cmd[10];
  printf("CONNECTED\n");
  fflush(stdout);
  while (scanf("%s", cmd) != EOF) {
    if (cmd[0] == 'R')
      printf("TEST\n");
    else if (cmd[0] == 'E')
      break;
    fflush(stdout);
  }
  return 0;
}
