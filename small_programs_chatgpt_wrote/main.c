#include <stdio.h>
#include <SDL2/SDL.h>

int main(int argc, char* argv[])
{
   SDL_Init(SDL_INIT_VIDEO);

   SDL_Window* win = SDL_CreateWindow("Red Square", 0, 0, 800, 600, SDL_WINDOW_SHOWN);
   SDL_Renderer* ren = SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED);

   SDL_SetRenderDrawColor(ren, 255, 0, 0, 255);

   SDL_Rect r = {300, 200, 200, 200};
   SDL_RenderFillRect(ren, &r);

   SDL_RenderPresent(ren);

   SDL_Delay(5000);

   SDL_DestroyRenderer(ren);
   SDL_DestroyWindow(win);

   SDL_Quit();

   return 0;
}

