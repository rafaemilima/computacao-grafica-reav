from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
import math
import numpy
from PIL import Image as Image

# Global aux vars

pi_value = 3.1415                       # Pi value aprox
coord_text_airplane = 1.0               # coordinate value for place texture on the airplane
WIDTH = 900                             # window width
HEIGHT = 600                            # window height
tetaxz = 0                              # rotation ang from watch point
raioxz = 6                              # distance between the watcher and the origin
airplane_vel = 1                        # airplane move velocity var
ground_color = [0.3, 0.3, 0.9, 1.0]     # the ground color
airplane_color = [0.4, 0.4, 0.4, 1.0]   # the airplane color
position = [0.0, 2.0, - 3.0]            # initial position of the airplane
ang = [0.0, 1.0, 0.0, 0.0]              # initial angle of the airplane
obs = [0.0, 7.0, 0.0]                   # watcher position coordinates
look = [0.0, 3.0, 0.0]                  # watcher lookat coordinates
luz = True                              # light control bool variable
autopilot = False                       # autopilot control bool variable
texture_ground = None                   # var for save ground's texture id
texture_airplane = None                 # var for save airplane's texture id
quadric = GLUquadricObj()               # data structure for save our quadric surfaces
airplane = GLuint                       # airplane list id
moon = GLuint                           # moon list id
# matrix with the coords for place the texture along all the airplane
airplane_texture_coordinates = [[-coord_text_airplane, -coord_text_airplane],
                                [+coord_text_airplane, -coord_text_airplane],
                                [+coord_text_airplane, +coord_text_airplane],
                                [-coord_text_airplane, +coord_text_airplane]]


# Reshape function
def reshape(width, height):
    global WIDTH, HEIGHT
    WIDTH = width
    HEIGHT = height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70.0, width / height, 0.1, 30.0)
    glMatrixMode(GL_MODELVIEW)


# Light funcion
def light():
    glEnable(GL_LIGHTING)        # Enables Lighting
    glEnable(GL_COLOR_MATERIAL)  # Enables Color_Material
    glEnable(GL_LIGHT0)
    global_amb = [0.5, 0.5, 0.5, 1.0]
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_amb)
    light0 = [[0.1, 0.1, 0.1, 1.0],
              [0.8, 0.8, 0.8, 1.0],
              [1.0, 1.0, 1.0, 1.0],
              [0.0, 0.0, 1.0, 1.0]]
    glLightfv(GL_LIGHT0, GL_AMBIENT, light0[0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light0[1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, light0[2])
    glLightfv(GL_LIGHT0, GL_POSITION, light0[3])


# Function that shapes the airplane and makes its list
def makeAirplane():
    global airplane, quadric
    if luz:
        light()
    asa = [[-2.0, 0.0, 0.0], [2.0, 0.0, 0.0], [0.0, 0.0, 1.5]]
    cauda = [[0.0, 0.0, 0.0], [0.0, 1.0, -1.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]

    airplane = glGenLists(1)
    glNewList(airplane, GL_COMPILE)


    glBegin(GL_TRIANGLES)
    glTexCoord2fv(airplane_texture_coordinates[0])
    glVertex3fv(asa[0])
    glTexCoord2fv(airplane_texture_coordinates[1])
    glVertex3fv(asa[1])
    glTexCoord2fv(airplane_texture_coordinates[3])
    glVertex3fv(asa[2])
    glEnd()
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluCylinder(quadric, 0.25, 0.25, 2, 12, 3)
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    glPushMatrix()
    glTranslatef(0, 0, 2)
    gluCylinder(quadric, 0.25, 0.0, 0.75, 12, 3)
    glPopMatrix()

    glBegin(GL_POLYGON)
    glTexCoord2fv(airplane_texture_coordinates[0])
    glVertex3fv(cauda[0])
    glTexCoord2fv(airplane_texture_coordinates[1])
    glVertex3fv(cauda[1])
    glTexCoord2fv(airplane_texture_coordinates[2])
    glVertex3fv(cauda[2])
    glTexCoord2fv(airplane_texture_coordinates[3])
    glVertex3fv(cauda[3])
    glEnd()

    glTranslatef(0, 0.15, 1.75)
    glPushMatrix()
    glScalef(0.4, 0.4, 1.0)
    quadric = gluNewQuadric()
    glColor3f(0.3, 0.5, 1)

    glDisable(GL_TEXTURE_2D)
    gluSphere(quadric, 0.5, 12, 12)
    glPopMatrix()


    glEndList()


# Function that shapes the moon and makes its list
def makeMoon():
    global moon
    moon = glGenLists(1)
    glNewList(moon, GL_COMPILE)
    glPushMatrix()
    glColor4f(0.6, 0.6, 0.5, 1.0)
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.2, 0.2, 0.2, 1])

    glTranslatef(2, 10, 3)
    glutSolidSphere(1, 100, 100)
    glPopMatrix()
    glEndList()


# Display Function
def display():

    glEnable(GL_DEPTH_TEST)
    global airplane, texture_ground, texture_airplane
    glDepthMask(GL_TRUE)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()

    obs[0] = raioxz * math.cos(2 * pi_value * tetaxz / 360)
    obs[2] = raioxz * math.sin(2 * pi_value * tetaxz / 360)
    gluLookAt(obs[0], obs[1], obs[2], look[0], look[1], look[2], 0.0, 1.0, 0.0)
    glCallList(moon)
    glEnable(GL_TEXTURE_2D)

    glColor4f(ground_color[0], ground_color[1], ground_color[2], ground_color[3])
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glBindTexture(GL_TEXTURE_2D, texture_ground)

    glBegin(GL_QUADS)

    glTexCoord2fv([0, 0])
    glVertex3f(-20, 0, 20)
    glTexCoord2fv([0, 1])
    glVertex3f(20, 0, 20)
    glTexCoord2fv([1, 1])
    glVertex3f(20, 0, -20)
    glTexCoord2fv([1, 0])
    glVertex3f(-20, 0, -20)
    glEnd()

    glTranslatef(position[0], position[1], position[2])
    glRotatef(ang[3], ang[0], ang[1], ang[2])
    #glScalef(0.3, 0.3, 0.3)

    glColor4f(airplane_color[0], airplane_color[1], airplane_color[2], airplane_color[3])
    glBindTexture(GL_TEXTURE_2D, texture_airplane)
    glCallList(airplane)


    glPopMatrix()

    glutSwapBuffers()


# Special keyboard function for use the special keys
def specialKeyboard(key, x, y):
    global tetaxz

    if key == GLUT_KEY_UP:
        obs[1] = obs[1] + 1
        glutPostRedisplay()

    elif key == GLUT_KEY_DOWN:
        obs[1] = obs[1] - 1
        glutPostRedisplay()

    elif key == GLUT_KEY_LEFT:
        tetaxz += 2
        glutPostRedisplay()

    elif key == GLUT_KEY_RIGHT:
        tetaxz -= 2
        glutPostRedisplay()


# Keyboard function
def keyboard(key, x, y):
    global raioxz, luz, key_press, autopilot, airplane_vel

    if key == b'w':
        move()
        makeAirplane()
        glutPostRedisplay()

    elif key == b'p':
        autopilot = not autopilot
        makeAirplane()
        glutPostRedisplay()

    elif key == b'a':
        ang[3] += 1
        makeAirplane()
        glutPostRedisplay()
        key_press = True

    elif key == b'd':
        ang[3] -= 1
        makeAirplane()
        glutPostRedisplay()
        key_press = True

    elif key == b'l':
        luz = not luz
        if not luz:
            glDisable(GL_LIGHTING)

        makeAirplane()
        glutPostRedisplay()
        key_press = True

    elif key == b'-':
        raioxz = raioxz + 1
        glutPostRedisplay()


    elif key == b'+':
        raioxz = raioxz - 1
        if (raioxz == 0):
            raioxz = 1
        glutPostRedisplay()

    elif key == b'V':
        airplane_vel += 1

    elif key == b"v":
        if airplane_vel > 1:
            airplane_vel -= 1


# Function that will load and build the textures
def loadTextures():
    global texture_ground, texture_airplane

    # Ground texture

    # Accessing the image file and building its data
    img1 = Image.open("vista-aerea-maceio-noturno.jpg")
    img1_data = numpy.array(list(img1.getdata()), numpy.int8)

    texture_ground = glGenTextures(1)             # Generates one texture name for the ground's texture
    glBindTexture(GL_TEXTURE_2D, texture_ground)  # Loads the texture associated to the texture_ground ID
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, img1.size[0], img1.size[1], GL_RGB, GL_UNSIGNED_BYTE, img1_data)
    # defines the directions the texture will be repeated in the object
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # defines the filters  that will be used when the texture got min or mag
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # specifies how texture values are interpreted when a fragment is textured
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


    # Airplane texture

    # Accessing the image file and building its data
    img2 = Image.open("textura-metal.jpg")
    img2_data = numpy.array(list(img2.getdata()), numpy.int8)

    texture_airplane = glGenTextures(1)              # Generates one texture name for the airplane's texture
    glBindTexture(GL_TEXTURE_2D, texture_airplane)   # Loads the texture associated to the texture_airplane ID
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, img2.size[0], img2.size[1], GL_RGB, GL_UNSIGNED_BYTE, img2_data)
    # defines the directions the texture will be repeated in the object
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # defines the filters  that will be used when the texture got min or mag
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # specifies how texture values are interpreted when a fragment is textured
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


# Function that moves the airplane horizontally
def move():
    global airplane_vel
    quad = ((ang[3] % 360) // 90) + 1
    d = ((ang[3] % 90) * 100)/900000

    if quad == 4:
        position[2] += d * airplane_vel
        position[0] -= (0.01 - d) * airplane_vel
    elif quad == 3:
        position[2] -= (0.01 - d) * airplane_vel
        position[0] -= d * airplane_vel
    elif quad == 2:
        position[2] -= d * airplane_vel
        position[0] += (0.01 - d) * airplane_vel
    elif quad == 1:
        position[0] += d * airplane_vel
        position[2] += (0.01 - d) * airplane_vel
    print(airplane_vel)


# Airplane animation function
def airplaneFlight(value):
    global key_press, autopilot
    glutPostRedisplay()
    glutTimerFunc(20, airplaneFlight, 1)
    if autopilot:
        move()


# Init function
def init():
    loadTextures()              # Loading and building textures
    makeAirplane()               # Modelling the airplane and associating to the airplane list id var
    makeMoon()                      # Modelling the moon and associating to the moon list id var
    glShadeModel(GL_FLAT)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)


# Main function
def main():

    glutInitWindowPosition(0, 0)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)

    if (not glutCreateWindow("Airplane Flights MCZ")) :
        print("Error: Could not open the window.\n")

    init()                             # Call of the init func
    glutKeyboardFunc(keyboard)         # Sets the keyboard callback for the current window
    glutSpecialFunc(specialKeyboard)   # Sets the special keyboard callback for the current window
    glutDisplayFunc(display)           # Sets the display callback for the current window
    glutReshapeFunc(reshape)           # Sets the reshape callback for the current window
    glutTimerFunc(20, airplaneFlight, 1)      # Sets a function will be called after 5ms for the airplane animation
    glutMainLoop()


main()  # Call of the main function
