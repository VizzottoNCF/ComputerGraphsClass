import pygame  
from pygame.locals import *  
from OpenGL.GL import *  
from OpenGL.GLUT import * 
from OpenGL.GLU import * 

# global variables
global_control = False
automatic_control = False
running = True
r = 0

# cube var
cxPos = -0.5
cyPos = 0
czPos = 0
cxRot = cyRot = 0

# triangle var
txPos = tyPos = 0
tzPos = 0
txRot = tyRot = 0

# pyramid var
pxPos = 0.5
pyPos = 0
pzPos = 0
pxRot = pyRot = 0

# animation vars
# velocity
cube_vel = [0.01, 0.0, 0.0]       # Cube moves left/right
tri_vel = [0.0, 0.015, 0.0]       # Triangle moves up/down
pyr_vel = [0.0, 0.0, 0.02]        # Pyramid moves front/back

# direction multiplyer
cube_dir = [1, 1, 1]
tri_dir = [1, 1, 1]
pyr_dir = [1, 1, 1]



def init_vars(option):
    global global_control, automatic_control, running

    if option == 6 or option == 7:
        global_control = False
    else:
        global_control = True


    if option == 7:
        automatic_control = True
    else:
        automatic_control = False
    
    running = True


def main():
    print("-------MENU------")
    print("Opcao 1 - Cubo")
    print("Opcao 2 - Triangulo")
    print("Opcao 3 - Cubo + Triangulo")
    print("Opcao 4 - Piramide")
    print("Opcao 5 - Cubo + Triangulo + Piramide")
    print("Opcao 6 - Controle Individual")
    print("Opcao 7 - Animacao Automatica dos Objetos")
    option = int(input("Escolha seu modo: "))

    pygame.init()
    pygame.display.set_mode((1280, 720), DOUBLEBUF | OPENGL)

    # global vars
    global global_control, automatic_control, running, r

    # define global vars depending on option
    init_vars(option)

    # init local variables
    xPos = yPos = zPos = 0
    x2Pos = y2Pos = z2Pos = 0
    x3Pos = y3Pos = z3Pos = 0
    xRot = yRot = 0
    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  
                    running = False
                
                if not automatic_control:
                    # afastar / aproximar
                    if event.key == K_z: 
                        zPos += 0.2 # frente
                    if event.key == K_x:
                        zPos -= 0.2 # trás
                        
                    # rotacionar
                    if event.key == K_q:
                        xRot += 1
                    if event.key == K_e:
                        xRot -= 1

                    if event.key == K_r:
                        yRot += 1
                    if event.key == K_f:
                            yRot -= 1

                    # if all objects should receive same input
                    if global_control == True:
                        # movimentação 2D
                        if event.key == K_a:  
                            xPos += -0.2  # esquerda
                        if event.key == K_d:  
                            xPos += 0.2  # direita
                        if event.key == K_w:  
                            yPos += 0.2  # cima
                        if event.key == K_s: 
                            yPos += -0.2  # baixo
                        
                    
                    
                    # if individual control is active
                    elif global_control == False:
                        # cube
                        if event.key == K_j:  
                            xPos += -0.2  # esquerda
                        if event.key == K_l:  
                            xPos += 0.2  # direita
                        if event.key == K_i:  
                            yPos += 0.2  # cima
                        if event.key == K_k: 
                            yPos += -0.2  # baixo
                        
                        # triangle
                        if event.key == K_v:  
                            x2Pos += -0.2  # esquerda
                        if event.key == K_n:  
                            x2Pos += 0.2  # direita
                        if event.key == K_g:  
                            y2Pos += 0.2  # cima
                        if event.key == K_b: 
                            y2Pos += -0.2  # baixo

                        # pyramid
                        if event.key == K_LEFT:  
                            x3Pos += -0.2  # esquerda
                        if event.key == K_RIGHT:  
                            x3Pos += 0.2  # direita
                        if event.key == K_UP:  
                            y3Pos += 0.2  # cima
                        if event.key == K_DOWN: 
                            y3Pos += -0.2  # baixo


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        r += 1

        # call draw functions on switch case
        match option:
            case 1:
                draw_cube(xPos, yPos, zPos, xRot, yRot)
            case 2:
                draw_triangle(xPos, yPos, zPos, xRot, yRot)
            case 3:
                draw_cube(xPos, yPos,zPos, xRot, yRot)
                draw_triangle(xPos, yPos, zPos, xRot, yRot)
            case 4:
                draw_pyramid(xPos, yPos, zPos, xRot, yRot)
            case 5:
                draw_cube(xPos, yPos,zPos, xRot, yRot)
                draw_triangle(xPos, yPos, zPos, xRot, yRot)
                draw_pyramid(xPos, yPos, zPos, xRot, yRot)
            case 6:
                draw_cube(xPos, yPos,zPos, xRot, yRot)
                draw_triangle(x2Pos, y2Pos, z2Pos, xRot, yRot)
                draw_pyramid(x3Pos, y3Pos, z3Pos, xRot, yRot)
            case 7: 
                # import globals
                global cxPos, cube_vel,  cube_dir
                global tyPos, tri_vel,  tri_dir
                global pzPos, pyr_vel,  pyr_dir

                # Cube - left/right
                cxPos += cube_vel[0] * cube_dir[0]
                if abs(cxPos) > 1:
                    cube_dir[0] *= -1  

                # Triangle - up/down
                tyPos += tri_vel[1] * tri_dir[1]
                if abs(tyPos) > 1:
                    tri_dir[1] *= -1

                # Pyramid - front/back (z axis)
                pzPos += pyr_vel[2] * pyr_dir[2]
                if abs(pzPos) > 1:
                    pyr_dir[2] *= -1

                # Draw everything with continuos rotation
                draw_cube(0, 0, 0, 1, 1)
                draw_triangle(0, 0, 0, 1, 1)
                draw_pyramid(0, 0, 0, 1, 1)
        
        # restart variables
        xPos = yPos = zPos = 0
        x2Pos = y2Pos = z2Pos = 0
        x3Pos = y3Pos = z3Pos = 0
        xRot = yRot = 0

        # update screen
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()

# draw cube
def draw_cube(_xPos, _yPos, _zPos, _xRot, _yRot):
    glLoadIdentity()
    global cxPos, cyPos, czPos, cxRot, cyRot, r

    # manipulate global position vars with temps
    cxPos += _xPos
    cyPos += _yPos
    czPos += _zPos
    cxRot += _xRot
    cyRot += _yRot

    glTranslatef(cxPos, cyPos, czPos)

    if cxRot != 0 or cyRot != 0:
        glRotatef(r, cxRot, cyRot, 0)
    else:
        glRotatef(0, cxRot, cyRot, 0)
    glScalef(0.2, 0.2, 0.2)

    glBegin(GL_QUADS)
    glColor3f(1, 0, 0)  # Red - Front face
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)

    glColor3f(0, 1, 0)  # Green - Back face
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)

    glColor3f(0, 0, 1)  # Blue - Left face
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)

    glColor3f(1, 1, 0)  # Yellow - Right face
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)

    glColor3f(1, 0, 1)  # Magenta - Top face
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)

    glColor3f(0, 1, 1)  # Cyan - Bottom face
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glEnd()


# draw triangle
def draw_triangle(_xPos, _yPos, _zPos, _xRot, _yRot):
    glLoadIdentity() 
    global txPos, tyPos, tzPos, txRot, tyRot, r

    # manipulate global position vars with temps
    txPos += _xPos
    tyPos += _yPos
    tzPos += _zPos
    txRot += _xRot
    tyRot += _yRot

    glTranslatef(txPos, tyPos, tzPos)
    if txRot != 0 or tyRot != 0:
        glRotatef(r, txRot, tyRot, 0)
    else:
        glRotatef(0, txRot, tyRot, 0)
    glScalef(0.2, 0.2, 0.2)

    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 0)  
    glVertex3f(0, 1, 0)  
    glVertex3f(-1, -1, 0)  
    glVertex3f(1, -1, 0) 
    glEnd()  

# draw pyramid
def draw_pyramid(_xPos, _yPos, _zPos, _xRot, _yRot):
    glLoadIdentity()
    global pxPos, pyPos, pzPos, pxRot, pyRot, r

    # manipulate global position vars with temps
    pxPos += _xPos
    pyPos += _yPos
    pzPos += _zPos
    pxRot += _xRot
    pyRot += _yRot

    glTranslatef(pxPos, pyPos, pzPos)

    if pxRot != 0 or pyRot != 0:
        glRotatef(r, pxRot, pyRot, 0)
    else:
        glRotatef(0, pxRot, pyRot, 0)
    glScalef(0.2, 0.2, 0.2)

    # Base color
    glBegin(GL_QUADS)
    glColor3f(1, 1, 0)  # Yellow
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)
    glEnd()

    # Pyramid faces (triangles)
    glBegin(GL_TRIANGLES)

    glColor3f(1, 0, 0)  # Front
    glVertex3f(0, 1, 0)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)

    glColor3f(0, 1, 0)  # Right
    glVertex3f(0, 1, 0)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, -1)

    glColor3f(0, 0, 1)  # Back
    glVertex3f(0, 1, 0)
    glVertex3f(1, -1, -1)
    glVertex3f(-1, -1, -1)

    glColor3f(1, 0, 1)  # Left
    glVertex3f(0, 1, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)

    glEnd()

if __name__ == '__main__':
    main()