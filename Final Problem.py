from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw(x, y):
    glPointSize(1)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def mid_point_circle(radius):
    x = 0
    y = radius
    d_init = 1 - radius
    d = d_init
    pixel = []
    while x < y:
        pixel.append((x, y))
        if d >= 0:
            d += (2 * x) - (2 * y) + 5
            x += 1
            y -= 1
        else:
            d += (2 * x) + 3
            x += 1
    return pixel

# any point to zone-0
def convert_to_zone0(x, y, zone):
    if zone == '1':
        return (y, x)
    elif zone == '2':
        return (y, -x)
    elif zone == '3':
        return (-x, y)
    elif zone == '4':
        return (-x, -y)
    elif zone == '5':
        return (-y, -x)
    elif zone == '6':
        return (-y, x)
    elif zone == '7':
        return (x, -y)
    # return (x, y)

# zone-0 to any point
def convert_to_original(x, y, Nzone):
    if Nzone == '1':
        return (y, x)
    elif Nzone == '2':
        return (-y, x)
    elif Nzone == '3':
        return (-x, y)
    elif Nzone == '4':
        return (-x, -y)
    elif Nzone == '5':
        return (-y, -x)
    elif Nzone == '6':
        return (y, -x)
    elif Nzone == '7':
        return (x, -y)
    # return (x, y)

def draw_circle(x, y, radius):
    glPointSize(1)
    glBegin(GL_POINTS)

    zone_0 = []
    zone_1 = mid_point_circle(radius)
    zone_2 = []
    zone_3 = []
    zone_4 = []
    zone_5 = []
    zone_6 = []
    zone_7 = []

    for (i, j) in zone_1:
        zone_0.append(convert_to_zone0(i, j, '1'))

    for (i, j) in zone_0:
        zone_2.append(convert_to_original(i, j, '2'))
        zone_3.append(convert_to_original(i, j, '3'))
        zone_4.append(convert_to_original(i, j, '4'))
        zone_5.append(convert_to_original(i, j, '5'))
        zone_6.append(convert_to_original(i, j, '6'))
        zone_7.append(convert_to_original(i, j, '7'))

    for (i, j) in zone_0:
        glVertex2f(x+i, y+j)
    for (i, j) in zone_1:
        glVertex2f(x+i, y+j)
    for (i, j) in zone_2:
        glVertex2f(x+i, y+j)
    for (i, j) in zone_3:
        glVertex2f(x+i, y+j)
    for (i, j) in zone_4:
        glVertex2f(x+i, y+j)
    for (i, j) in zone_5:
        glVertex2f(x+i, y+j)
    for (i, j) in zone_6:
        glVertex2f(x+i, y+j)
    for (i, j) in zone_7:
        glVertex2f(x+i, y+j)

    glEnd()

#-------------line --------------------------------------------------

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
    glColor3f(1, 0, 0)
    #=============== BD flag ========================================
    #draw_circle(250, 250, 20)
    # for in range(2):
    h=int(input('Gimme : '))
    for i in range(h):

        MidPointLine(230-i*10,270+i*20,270+i*10,270+i*20)#upper
        MidPointLine(230-i*10, 230, 270+i*10, 230) #lower
        MidPointLine(270+i*10, 230, 270+i*10, 270+i*20)#right line
        MidPointLine(230-i*10, 230, 230-i*10, 270+i*20) #left line
        draw_circle(250, 250+i*10, 20+i*10)

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Lab 3 - Midpoint Circle - 9 Circles")
glutDisplayFunc(showScreen)

glutMainLoop()