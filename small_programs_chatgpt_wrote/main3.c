#include <GL/glut.h>

void display()
{
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glMatrixMode(GL_MODELVIEW);
  
  glLoadIdentity();
  gluLookAt(3.0f, 3.0f, 3.0f, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f, 0.0f);
  
  glBegin(GL_QUADS);
  // Front face
  glColor3f(1.0f, 0.0f, 0.0f); // Red
  glVertex3f(-1.0f, -1.0f,  1.0f);
  glVertex3f( 1.0f, -1.0f,  1.0f);
  glVertex3f( 1.0f,  1.0f,  1.0f);
  glVertex3f(-1.0f,  1.0f,  1.0f);
  // Back face
  glColor3f(0.0f, 1.0f, 0.0f); // Green
  glVertex3f(-1.0f, -1.0f, -1.0f);
  glVertex3f(-1.0f,  1.0f, -1.0f);
  glVertex3f( 1.0f,  1.0f, -1.0f);
  glVertex3f( 1.0f, -1.0f, -1.0f);
  // Top face
  glColor3f(0.0f, 0.0f, 1.0f); // Blue
  glVertex3f(-1.0f,  1.0f, -1.0f);
  glVertex3f(-1.0f,  1.0f,  1.0f);
  glVertex3f( 1.0f,  1.0f,  1.0f);
  glVertex3f( 1.0f,  1.0f, -1.0f);
  // Bottom face
  glColor3f(1.0f, 1.0f, 0.0f); // Yellow
  glVertex3f(-1.0f, -1.0f, -1.0f);
  glVertex3f( 1.0f, -1.0f, -1.0f);
  glVertex3f( 1.0f, -1.0f,  1.0f);
  glVertex3f(-1.0f, -1.0f,  1.0f);
  // Right face
  glColor3f(1.0f, 0.0f, 1.0f); // Magenta
  glVertex3f( 1.0f, -1.0f, -1.0f);
  glVertex3f( 1.0f,  1.0f, -1.0f);
  glVertex3f( 1.0f,  1.0f,  1.0f);
  glVertex3f( 1.0f, -1.0f,  1.0f);
  // Left face
  glColor3f(0.0f, 1.0f, 1.0f); // Cyan
  glVertex3f(-1.0f, -1.0f, -1.0f);
  glVertex3f(-1.0f, -1.0f,  1.0f);
  glVertex3f(-1.0f,  1.0f,  1.0f);
  glVertex3f(-1.0f,  1.0f, -1.0f);
  glEnd();
  
  glutSwapBuffers();
}

void reshape(int width, int height)
{
  glViewport(0, 0, width, height);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  
  gluPerspective(60.0f, ((float)width / (float)height), 0.1f, 10.0f);
  
  glMatrixMode(GL_MODELVIEW);
}

int main(int argc, char **argv)
{
  glutInit(&argc, argv);
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
  glutInitWindowSize(500, 500);
  glutCreateWindow("Cube Example");
  
  glEnable(GL_DEPTH_TEST);
  
  glutDisplayFunc(display);
  glutReshapeFunc(reshape);
  
  glutMainLoop();
  
  return 0;
}

