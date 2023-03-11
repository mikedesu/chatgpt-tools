#include <stdio.h>
#include <stdlib.h>
#include <GL/gl.h>
#include <SDL2/SDL.h>

// Cube vertex data
GLfloat vertices[] = {
    // Front face
    -0.5f, -0.5f,  0.5f,
     0.5f, -0.5f,  0.5f,
     0.5f,  0.5f,  0.5f,
    -0.5f,  0.5f,  0.5f,
    // Back face
    -0.5f, -0.5f, -0.5f,
     0.5f, -0.5f, -0.5f,
     0.5f,  0.5f, -0.5f,
    -0.5f,  0.5f, -0.5f
};

// Cube index data
GLushort indices[] = {
    0, 1, 2, 2, 3, 0,  // Front face
    4, 5, 6, 6, 7, 4,  // Back face
    3, 2, 6, 6, 7, 3,  // Top face
    0, 1, 5, 5, 4, 0,  // Bottom face
    1, 5, 6, 6, 2, 1,  // Right face
    0, 4, 7, 7, 3, 0   // Left face
};

int main(int argc, char* argv[])
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window* window = SDL_CreateWindow("Cube Renderer", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_OPENGL |
SDL_WINDOW_SHOWN);
    SDL_GLContext context = SDL_GL_CreateContext(window);

    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0f, (float)800 / (float)600, 0.1f, 100.0f);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, -5.0f);

    glShadeModel(GL_SMOOTH);

    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LEQUAL);

    glEnableClientState(GL_VERTEX_ARRAY);
    glVertexPointer(3, GL_FLOAT, 0, vertices);

    // Game loop
        SDL_Event event;
    int running = 1;
    while (running) {
        // Handle events
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
            case SDL_QUIT:
                running = 0;
                break;
            default:
                break;
            }
        }

        // Render the cube
        // Rotate the cube
        static float angle = 0.0f;
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glLoadIdentity();
        glTranslatef(0.0f, 0.0f, -5.0f);
        glRotatef(angle, 1.0f, 1.0f, 1.0f); // Rotate around the y-axis
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_SHORT, indices);
        SDL_GL_SwapWindow(window);
        angle += 0.5f;
    }

    glDisableClientState(GL_VERTEX_ARRAY);

    SDL_GL_DeleteContext(context);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
