#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/types.h>
#include <termios.h>
#include <unistd.h>

#define HEIGHT 27
#define WIDTH 82
#define rocketLeftX 5
#define rocketRightX 75
#define gameSpeed 150000

struct player {
  int x, y;
};
struct ball {
  int x, y, speedX, speedY;
};
static struct termios stored_settings;

struct ball moveball();
void field();
int trigger(struct player Player, struct ball Ball);
struct ball returnBallToSpawn(struct ball Ball);
struct player playerMove(struct player pl, int delta);
void set_keypress(void);
void reset_keypress(void);

int draw_racket();
int draw_count();
int draw_ball();
int draw_grid();
int draw_borders();

int main() {
  fd_set rfds;
  struct timeval tv;

  set_keypress();

  struct player player1;
  struct player player2;
  struct ball playerBall;

  playerBall.x = 40;
  playerBall.y = 12;
  playerBall.speedX = 1;
  playerBall.speedY = 1;

  player1.x = rocketLeftX;
  player1.y = 12;
  player2.x = rocketRightX;
  player2.y = 12;

  moveball(playerBall);

  int score_1 = 0;
  int score_2 = 0;
  field(playerBall, player1, player2, score_1, score_2);

  while (1) {
    int retval;
    FD_ZERO(&rfds);
    FD_SET(0, &rfds);
    tv.tv_sec = 0;
    tv.tv_usec = 0;

    retval = select(2, &rfds, NULL, NULL, &tv);

    // User input
    char userInput;

    if (retval) {
      userInput = getchar();
    } else {
      userInput = ' ';
    }
    if (userInput == 'a') {
      player1 = playerMove(player1, -1);
    } else if (userInput == 'z') {
      player1 = playerMove(player1, 1);
    } else if (userInput == 'k') {
      player2 = playerMove(player2, -1);
    } else if (userInput == 'm') {
      player2 = playerMove(player2, 1);
    }

    // Draw field
    field(playerBall, player1, player2, score_1, score_2);
    if (score_1 == 21 || score_2 == 21) {
      break;
    }
    // Border collision
    if (playerBall.y == 25 || playerBall.y == 1) {
      playerBall.speedY *= -1;
    } else if (trigger(player1, playerBall) || trigger(player2, playerBall)) {
      playerBall.speedX *= -1;
    }
    playerBall = moveball(playerBall);

    // Win condition
    if (playerBall.x < rocketLeftX - 5) {
      score_1++;
      playerBall = returnBallToSpawn(playerBall);
    } else if (playerBall.x > rocketRightX + 5) {
      score_2++;
      playerBall = returnBallToSpawn(playerBall);
    }
    usleep(gameSpeed);
  }
  printf("GAME OVER\n");
  if (score_1 == 21) {
    printf("THE WINNER IS PLAYER 2, congratulations!\n");
  } else if (score_2 == 21) {
    printf("THE WINNER IS PLAYER 1, congratulations!\n");
  }
  reset_keypress();
}

void field(struct ball plBall, struct player player1, struct player player2,
           int score_1, int score_2) {
  printf("\e[1;1H\e[2J");
  for (int y = 0; y < HEIGHT; y++) {
    for (int x = 0; x < WIDTH; x++) {
      // Draw ball
      if (plBall.x == x && plBall.y == y) {
        printf("@");
        // Draw rockets
      } else if (rocketLeftX == x &&
                 (player1.y + 1 == y || player1.y == y || player1.y - 1 == y)) {
        printf("l");
      } else if (rocketRightX == x &&
                 (player2.y + 1 == y || player2.y == y || player2.y - 1 == y)) {
        printf("x");
      } else if (x == 41) {
        printf("|");
      } else if (x == 0 || y == 0 || x == 81 || y == 26) {
        printf("*");
      } else if (x == 38 && y == 3) {
        printf("%d", score_2 / 10);
      } else if (x == 39 && y == 3) {
        printf("%d", score_2 % 10);
      } else if (x == 43 && y == 3) {
        printf("%d", score_1 / 10);
      } else if (x == 44 && y == 3) {
        printf("%d", score_1 % 10);
      } else {
        printf(" ");
      }
    }
    printf("\n");
  }
}

struct ball moveball(struct ball plBall) {
  plBall.x += 1 * plBall.speedX;
  plBall.y += 1 * plBall.speedY;

  return plBall;
}

int trigger(struct player Player, struct ball Ball) {
  if (Ball.x == Player.x && (Ball.y == Player.y || Ball.y == Player.y + 1 ||
                             Ball.y == Player.y - 1)) {
    return 1;
  } else {
    return 0;
  }
}

struct ball returnBallToSpawn(struct ball Ball) {
  Ball.x = 40;
  Ball.y = 11;
  return Ball;
}
void set_keypress(void) {
  struct termios new_settings;
  tcgetattr(0, &stored_settings);
  new_settings = stored_settings;
  new_settings.c_lflag &= (~ICANON);
  new_settings.c_lflag &= (~ECHO);
  new_settings.c_cc[VTIME] = 0;
  new_settings.c_cc[VMIN] = 1;

  tcsetattr(0, TCSANOW, &new_settings);
  return;
}
void reset_keypress(void) {
  tcsetattr(0, TCSANOW, &stored_settings);
  return;
}
struct player playerMove(struct player pl, int delta) {
  if (pl.y > 23 && delta == 1) {
    printf("%c", ' ');
  } else if (pl.y < 3 && delta == -1) {
    printf("%c", ' ');
  } else {
    pl.y += delta;
  }

  return pl;
}
