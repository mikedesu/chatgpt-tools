#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

//#include <SDL.h>
#include <SDL2/SDL.h>
#include <SDL_opengl.h>

bool init();
void render();

SDL_Window* gWindow = NULL;
SDL_GLContext gContext;

int main( int argc, char* args[] )
{
    if ( !init() )
    {
        printf( "Failed to initialize!\n" );
        return -1;
    }
    bool quit = false;
    SDL_Event e;
    while (!quit)
    {
        while (SDL_PollEvent(&e))
        {
            if (e.type == SDL_QUIT)
            {
                quit = true;
            }
        }
        render();
    }
    SDL_DestroyWindow(gWindow);
    gWindow = NULL;
    SDL_Quit();
    return 0;
}

bool init()
{
    bool success = true;
    if ( SDL_Init( SDL_INIT_VIDEO ) < 0 )
    {
        printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        success = false;
    }
    else
    {
        SDL_GL_SetAttribute( SDL_GL_CONTEXT_MAJOR_VERSION, 2 );
        SDL_GL_SetAttribute( SDL_GL_CONTEXT_MINOR_VERSION, 1 );
        SDL_GL_SetAttribute( SDL_GL_DOUBLEBUFFER, 1 );
        gWindow = SDL_CreateWindow( "cube example", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 640,
480, SDL_WINDOW_OPENGL | SDL_WINDOW_SHOWN );
        if ( gWindow == NULL )
        {
            printf( "Window could not be created! SDL_Error: %s\n", SDL_GetError() );
            success = false;
        }
        else
        {
            gContext = SDL_GL_CreateContext(gWindow);
            if (gContext == NULL)
            {
                printf("Failed to create OpenGL context! SDL Error: %s\n", SDL_GetError());
                success = false;
            }
            else
            {
                GLenum error = GL_NO_ERROR;
                glClearColor(0.f, 0.f, 0.f, 1.f);
                glMatrixMode(GL_PROJECTION);
                glLoadIdentity();
                glViewport(0, 0, 640, 480);
                gluPerspective(45.0f, (GLfloat)640/(GLfloat)480, 0.1f, 100.0f);
                glMatrixMode(GL_MODELVIEW);
                glLoadIdentity();
                glShadeModel(GL_SMOOTH);
                glEnable(GL_DEPTH_TEST);
                glEnable(GL_CULL_FACE);
                glCullFace(GL_BACK);
                glEnableClientState(GL_VERTEX_ARRAY);
                glEnableClientState(GL_COLOR_ARRAY);
            }
        }
    }
    return success;
}

void render()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    gluLookAt(5.0,5.0,5.0,0.0,0.0,0.0,0.0,1.0,0.0);
    glBegin(GL_QUADS);
    // Front face (red)
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex3f(-1.0f, -1.0f,  1.0f);
    glVertex3f( 1.0f, -1.0f,  1.0f);
    glVertex3f( 1.0f,  1.0f,  1.0f);
    glVertex3f(-1.0f,  1.0f,  1.0f);
    // Back face (green)
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex3f(-1.0f, -1.0f, -1.0f);
    glVertex3f(-1.0f,  1.0f, -1.0f);
    glVertex3f( 1.0f,  1.0f, -1.0f);
    glVertex3f( 1.0f, -1.0f, -1.0f);
    // Top face (blue)
    glColor3f(0.0f, 0.0f, 1.0f);
    glVertex3f(-1.0f,  1.0f, -1.0f);
    glVertex3f(-1.0f,  1.0f,  1.0f);
    glVertex3f( 1.0f,  1.0f,  1.0f);
    glVertex3f( 1.0f,  1.0f, -1.0f);
    // Bottom face (yellow)
    glColor3f(1.0f, 1.0f, 0.0f);
    glVertex3f(-1.0f, -1.0f, -1.0f);
    glVertex3f( 1.0f, -1.0f, -1.0f);
    glVertex3f( 1.0f, -1.0f,  1.0f);
    glVertex3f(-1.0f, -1.0f,  1.0f);
    // Right face (magenta)
    glColor3f(1.0f, 0.0f, 1.0f);
    glVertex3f( 1.0f, -1.0f, -1.0f);
    glVertex3f( 1.0f,  1.0f, -1.0f);
    glVertex3f( 1.0f,  1.0f,  1.0f);
    glVertex3f( 1.0f, -1.0f,  1.0f);
    // Left face (cyan)
    glColor3f(0.0f, 1.0f, 1.0f);
    glVertex3f(-1.0f, -1.0f, -1.0f);
    glVertex3f(-1.0f, -1.0f,  1.0f);
    glVertex3f(-1.0f,  1.0f,  1.0f);
    glVertex3f(-1.0f,  1.0f, -1.0f);
    glEnd();
    SDL_GL_SwapWindow(gWindow);
}

