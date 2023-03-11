//#include <stdio.h>
//#include <stdlib.h>
#include <GL/gl.h>
//#include <GL/glu.h>
#include <SDL2/SDL.h>
//#include <time.h>


//void offset_x_vertices_by(float offset) ;
//void offset_y_vertices_by(float offset) ;
//void offset_z_vertices_by(float offset) ;
//void reset_vertices2() ;
//void random_color() ;
//void draw_cube(GLfloat *vertices, GLushort *indices) ;
//void reset_vertices2_x() ;
//void reset_vertices2_y() ;
//void reset_vertices2_z() ;


//int frame_count_threshold = 60;
//int color_frame_count = 1;
//float r = 1.0f;
//float g = 1.0f;
//float b = 1.0f;





// Cube vertex data
//

// a second cube's vertex data but cut in half to make it smaller
// also offset to the left by 2.0f
// also with some distance between the cubes so they are not touching
//GLfloat vertices2[] = {
    // Front face
//    -0.5f, -0.5f,  0.5f, // top left
//     0.5f, -0.5f,  0.5f, // top right
//     0.5f,  0.5f,  0.5f, // bottom right
//    -0.5f,  0.5f,  0.5f, // bottom left
    // Back face
//    -0.5f, -0.5f, -0.5f, // top left
//     0.5f, -0.5f, -0.5f, // top right
//     0.5f,  0.5f, -0.5f, // bottom right
//    -0.5f,  0.5f, -0.5f // bottom left
//};

// Cube index data


//void random_color() {
//    r = (float)random()/(float)(RAND_MAX);
//    g = (float)random()/(float)(RAND_MAX);
//    b = (float)random()/(float)(RAND_MAX);
//}


//void draw_cube(GLfloat *vertices, GLushort *indices) {
//    glVertexPointer(3, GL_FLOAT, 0, vertices); 
//    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_SHORT, indices); // indices is a pointer to the index data
//}


//void reset_vertices2() {
//    for (int i = 0; i < 24; i++) {
//        vertices2[i] = vertices[i];
//    }
//}


//void reset_vertices2_x() {
//    for (int i = 0; i < 24; i+=3) {
//        vertices2[i] = vertices[i];
//    }
//}


//void reset_vertices2_y() {
//    for (int i = 1; i < 24; i+=3) {
//        vertices2[i] = vertices[i];
//    }
//}


//void reset_vertices2_z() {
//    for (int i = 2; i < 24; i+=3) {
//        vertices2[i] = vertices[i];
//    }
//}


//void offset_x_vertices_by(float offset) {
//    for (int i = 0; i < 24; i+=3) {
//        vertices2[i] += offset;
//    }
//}


//void offset_y_vertices_by(float offset) {
//    for (int i = 1; i < 24; i+=3) {
//        vertices2[i] += offset;
//    }
//}


//void offset_z_vertices_by(float offset) {
//    for (int i = 2; i < 24; i+=3) {
//        vertices2[i] += offset;
//    }
//}









int main(int argc, char* argv[]) {
    //srand(time(NULL));
GLfloat x = 0.5;
GLfloat xx = -0.5;

//GLfloat *v = malloc(24 * sizeof(GLfloat));
//memset(v, x, 24 * sizeof(GLfloat));
//v[0] = v[1] = v[4] = v[9] = v[12] = v[13] = v[14] = v[16] = v[17] = v[20] = v[21] = v[23] = xx;



GLfloat v[] = {
    // Front face
    -x, -x, x, // top left
     x, -x,  x, // top right
     x,  x,  x, // bottom right
    -x,  x,  x, // bottom left
    // Back face
    -x, -x, -x, // top left
     x, -x, -x, // top right
     x,  x, -x, // bottom right
    -x,  x, -x // bottom left
};

GLushort * indices = malloc(36 * sizeof(GLushort));
//memset(indices, 0, 36 * sizeof(GLushort));

memset(indices, 1, 36 * sizeof(GLushort));
int p = 1;
int q = 2;
indices[0] = 0;
indices[5] = 0;
indices[18] = 0;
indices[23] = 0;
indices[30] = 0;
indices[35] = 0;

indices[2] += p;
indices[3] += p;
indices[13] += p;
indices[28] += p;

indices[4] += 2;
indices[12] += 2;
indices[17] += 2;
indices[34] += 2;

indices[6] += 3;
indices[22] += 3;
indices[31] += 3;

indices[7] += 4;
indices[20] += 4;
indices[21] += 4;
indices[25] += 4;

indices[8] += 5;
indices[9] += 5;
indices[11] += 5;
indices[14] += 5;
indices[15] += 5;
indices[26] += 5;
indices[27] += 5;

indices[10] += 6;
indices[16] += 6;
indices[32] += 6;
indices[33] += 6;







        
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
    //glTranslatef(0.0f, 0.0f, -5.0f);
    glTranslatef(0.0f, 0.0f, -20.0f); // Move 5 units into the screen
    glShadeModel(GL_SMOOTH);
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LEQUAL);
    glEnableClientState(GL_VERTEX_ARRAY);

    // Game loop
    SDL_Event event;
    int running = 1;

    float rotational_speed = 0.5f;
//    float max_zoom = -50.0f;
    float current_zoom = -20.0f;
//    float zoom_direction = -0.1f;
    float angle = 0.0f;

    while (running) {
        //reset_vertices2();

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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glLoadIdentity();
        glTranslatef(0.0f, 0.0f, current_zoom); // Move 5 units into the screen
        glRotatef(angle, 1.0f, 1.0f, 0.0f); // Rotate around the y-axis

        //if (color_frame_count > frame_count_threshold) {
            //random_color();
            //color_frame_count = 0;
        //}

        glColor3f(1,1,1); 
        //draw_cube(vertices, indices);       
        glVertexPointer(3, GL_FLOAT, 0, v);
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_SHORT, indices); // indices is a pointer to the index data
        
        //reset_vertices2();
        //for (float i = -20; i <= 20; i+=2) {
        //    offset_x_vertices_by(i);
        //    draw_cube(vertices2, indices);       
        //    reset_vertices2();
        //    offset_y_vertices_by(i);
        //    draw_cube(vertices2, indices);       
        //    reset_vertices2();
        //}

        //reset_vertices2();
        //for (int i = 0; i < 10; i++) {
        //    offset_z_vertices_by( -2.0f);
        //    draw_cube(vertices2, indices2);       
        //}
        //reset_vertices2();
        //for (int i = 0; i < 10; i++) {
        //    offset_z_vertices_by( 2.0f);
        //    draw_cube(vertices2, indices2);       
        //}


        //offset_z_vertices_by( -2.0f);
        //offset_y_vertices_by( -2.0f);
        //offset_x_vertices_by( -2.0f);
        //draw_cube(vertices2, indices2);       

        SDL_GL_SwapWindow(window);
        angle += rotational_speed;
        //current_zoom += zoom_direction;
        //if (current_zoom < max_zoom) {
        //    current_zoom = max_zoom;
        //    zoom_direction = -zoom_direction;
        //}
        //else if (current_zoom > 0) {
        //    current_zoom = 0;
        //    zoom_direction = -zoom_direction;
        //}
        //angle += 0.5f;
        //color_frame_count++;
    }
    glDisableClientState(GL_VERTEX_ARRAY);
    SDL_GL_DeleteContext(context);
    SDL_DestroyWindow(window);
    SDL_Quit();

    //free(v);

    return 0;
}



