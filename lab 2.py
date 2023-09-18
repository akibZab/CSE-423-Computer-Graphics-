from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw(x, y):
    glPointSize(8)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def FindZone(dx, dy):
    dx1, dy1 = abs(dx), abs(dy)
    if dx >= 0 and dy >= 0 and dy1 <= dx1:
        return 0
    elif dx >= 0 and dy >= 0 and dy1 >= dx1:
        return 1
    elif dx < 0 and dy > 0 and dy1 >= dx1:
        return 2
    elif dx < 0 and dy > 0 and dy1 <= dx1:
        return 3
    elif dx < 0 and dy < 0 and dx1 >= dy1:
        return 4
    elif dx < 0 and dy < 0 and dy1 >= dx1:
        return 5
    elif dx > 0 and dy < 0 and dy1 >= dx1:
        return 6
    elif dx > 0 and dy < 0 and dy1 <= dx1:
        return 7

def ConvertToZone0(x1, y1, x2, y2, zone):
    if zone == 0:
        return x1, y1, x2, y2
    elif zone == 1:
        return y1, x1, y2, x2
    elif zone == 2:
        return y1, -x1, y2, -x2
    elif zone == 3:
        return -x1, y1, -x2, y2
    elif zone == 4:
        return -x1, -y1, -x2, -y2
    elif zone == 5:
        return -y1, -x1, -y2, -x1
    elif zone == 6:
        return -y1, x1, -y2, x2
    elif zone == 7:
        return x1, -y1, x2, -y2


def OriginalZone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def MidPointLine(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = FindZone(dx, dy)
    x1, y1, x2, y2 = ConvertToZone0(x1, y1, x2, y2, zone)
    nx = []
    ny = []
    d = []
    dx = x2 - x1
    dy = y2 - y1
    d_init = 2 * dy - dx
    d += [d_init]
    NE = 2 * dy - 2 * dx
    E = 2 * dy
    x = x1
    y = y1
    while x <= x2:
        nx += [x]
        ny += [y]
        sx, ex = OriginalZone(x, y, zone)
        draw(sx, ex)
        x = x + 1
        if d_init > 0:
            y = y + 1
            d_init = d_init + NE
        else:
            d_init = d_init + E
            d += [d_init]

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(0.0, 0.0, 2.0)

    # Drawing the number 1
    MidPointLine(150, 100, 150, 400)

    # Drawing the number 3
    MidPointLine(370, 100, 370, 400) #one punch man
    MidPointLine(240, 400, 370, 400) #upper line
    MidPointLine(240, 100, 370, 100) #lower line
    MidPointLine(240, 250, 370, 250) #midline
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500,500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Lab 2 - 20101113")
glutDisplayFunc(showScreen)

glutMainLoop()