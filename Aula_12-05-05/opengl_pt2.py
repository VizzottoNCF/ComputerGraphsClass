# Importação das bibliotecas necessárias

import pyglet
pyglet.options['shadow_window'] = False
pyglet.window.Window(visible=False)

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image
import math


# Importação do módulo pywavefront para carregar e desenhar o modelo OBJ
from pywavefront import Wavefront
#from pywavefront.visualization import draw  # agora encontrará GL_V3F corretamente




# Variáveis globais de posição e rotação da câmera
camera_x, camera_y, camera_z = 0, 0, -5  # Câmera posicionada de frente para o cubo
yaw = 0                            # Ângulo de rotação horizontal (inicialmente olhando para Z positivo)
pitch = 0                              # Ângulo de rotação vertical
sensitivity = 0.02                        # Sensibilidade do mouse para rotação
rot_x, rot_y = 0, 0                       # Ângulos de rotação da câmera (x para inclinar, y para girar)



# Atualiza a direção de visão da câmera com base em yaw e pitch
def update_camera_direction():
    rad_yaw = math.radians(yaw)
    rad_pitch = math.radians(pitch)
    dir_x = math.cos(rad_pitch) * math.sin(rad_yaw)
    dir_y = math.sin(rad_pitch)
    dir_z = math.cos(rad_pitch) * math.cos(rad_yaw)
    return dir_x, dir_y, dir_z

# Função que carrega imagem como textura
def load_texture(filename):
    img = Image.open(filename)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGBA").tobytes()
    width, height = img.size
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    return tex_id

# Função que desenha um cubo com textura aplicada, face por face
def draw_textured_cube():
    glBegin(GL_QUADS)  # Inicia desenho de quadriláteros

    #Explicação:
    # glTexCoord2f(0, 0)
    #→ Indica a coordenada da textura (posição do pixel da imagem que será aplicada no vértice).
    #→ Neste caso, 0,0 representa o canto inferior esquerdo da imagem.
    #--------------------------------
    #glVertex3fv(cube_vertices[0])
    #→ Indica a posição do vértice no espaço 3D onde essa parte da textura será aplicada.

    # FACE TRASEIRA (fundo do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])  # inferior esquerdo
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1])  # inferior direito
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[2])  # superior direito
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[3])  # superior esquerdo

    # FACE FRONTAL (frente do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[4])  # inferior esquerdo
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[5])  # inferior direito
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])  # superior direito
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7])  # superior esquerdo

    # FACE INFERIOR (base)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])  # traseira esquerda
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1])  # traseira direita
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[5])  # frontal direita
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[4])  # frontal esquerda

    # FACE SUPERIOR (tampa)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[3])  # traseira esquerda
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2])  # traseira direita
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])  # frontal direita
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7])  # frontal esquerda

    # FACE DIREITA (lado direito do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[1])  # inferior traseiro
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2])  # superior traseiro
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])  # superior frontal
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[5])  # inferior frontal

    # FACE ESQUERDA (lado esquerdo do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])  # inferior traseiro
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[3])  # superior traseiro
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[7])  # superior frontal
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[4])  # inferior frontal

    glEnd()  # Finaliza o desenho


# Lista de coordenadas 3D dos vértices do cubo
# Cada vértice é representado por uma tupla (x, y, z)
# Observação: o cubo tem 8 vértices no total
cube_vertices = [
    (-1, -1, -1),  # 0 - canto inferior esquerdo traseiro
    ( 1, -1, -1),  # 1 - canto inferior direito traseiro
    ( 1,  1, -1),  # 2 - canto superior direito traseiro
    (-1,  1, -1),  # 3 - canto superior esquerdo traseiro

    (-1, -1,  1),  # 4 - canto inferior esquerdo frontal
    ( 1, -1,  1),  # 5 - canto inferior direito frontal
    ( 1,  1,  1),  # 6 - canto superior direito frontal
    (-1,  1,  1)   # 7 - canto superior esquerdo frontal
]

# Índices que definem as 6 faces do cubo com 4 vértices cada
cube_faces = [
    (0, 1, 2, 3),  # Traseira
    (4, 5, 6, 7),  # Frontal
    (0, 1, 5, 4),  # Inferior
    (2, 3, 7, 6),  # Superior
    (1, 2, 6, 5),  # Lateral direita
    (0, 3, 7, 4)   # Lateral esquerda
]

# Coordenadas 2D da textura (mapeamento)
cube_texcoords = [
    (0, 0), # canto inferior esquerdo,
    (1, 0), # inferior direito,
    (1, 1), # superior direito,
    (0, 1)  # superior esquerdo
]


# usa glInterleavedArrays para desenhar tudo de uma vez
def draw_obj_model(scene, tex_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    for mat in scene.materials.values():
        verts = mat.vertices  # [x,y,z,nx,ny,nz,u,v, x,y,z, …]
        count = len(verts) // 8
        array_type = (GLfloat * len(verts))(*verts)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        # T2F_N3F_V3F == texcoord (2 floats), normal (3), vertex (3)
        glInterleavedArrays(GL_T2F_N3F_V3F, 0, array_type)
        glDrawArrays(GL_TRIANGLES, 0, count)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)




# Configura o OpenGL (textura, profundidade, iluminação)
def init_opengl(display):
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.3, 0.2, 0.1, 1.0)) #laranja

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 5, 5, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1))
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, 80)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    #gluPerspective(fov, aspect, near, far) define uma matriz de projeção em perspectiva, onde:
    #fov: Campo de visão vertical (em graus). Ex: 45 → visão razoavelmente aberta.
    #aspect: Proporção da tela (largura / altura).
    #near: Distância mínima visível (objetos mais próximos são cortados).
    #far: Distância máxima visível (objetos mais distantes são cortados).
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0) #
    glMatrixMode(GL_MODELVIEW)


def second_light(display):
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.3, 0.2, 0.1, 1.0)) #laranja

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (6, 5, 5, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1))
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, 80)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0) #
    glMatrixMode(GL_MODELVIEW)

def draw_floor_plane(xPos = 0, yPos = 0, zPos = 0, xRot= 0, yRot = 0, zRot = 0, size = 1):
    glTranslate(xPos,yPos,zPos)
    glRotatef(1, xRot,yRot,zRot)
    
    glBegin(GL_QUADS)

    # setting plane in XZ axis (y = 0)
    glTexCoord2f(0, 0); glVertex3f(-size, 0, -size)
    glTexCoord2f(1, 0); glVertex3f(size, 0, -size)
    glTexCoord2f(1, 1); glVertex3f(size, 0, size)
    glTexCoord2f(0, 1); glVertex3f(-size, 0, size)

    glEnd()



# Função principal
def main():
    global camera_x, camera_y, camera_z, yaw, pitch, rot_x, rot_y # Variáveis globais
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    init_opengl(display)
    second_light(display)

    # load textures
    cat_tex  = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_12-05-05/Cat_v1/Cat_diffuse.jpg")
    # benz_tex = load_texture()
    tex_id = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_12-05-05/textura.jpg")
    box_tex = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_12-05-05/Cardboard box/Models and Textures/6857659-light-brown-wallpaper.jpg")
    grass_tex = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_12-05-05/grass.jpg")

    # load objects
    cat_obj = Wavefront("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_12-05-05/Cat_v1/12221_Cat_v1_l3.obj", collect_faces=True, parse=True)
    # benz_obj = Wavefront("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_12-05-05/MercedesBenzGLS580.obj", collect_faces=True, parse=True)
    tree_obj = Wavefront("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_12-05-05/low_poly_tree/Lowpoly_tree_sample.obj", collect_faces=True, parse=True)
    box_obj = Wavefront("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_12-05-05/Cardboard box/Models and Textures/Cardboard box.obj")

    #configuração do relógio para limitar FPS
    clock = pygame.time.Clock()
    running = True

    # Carregar objeto
    #objeto = Wavefront('modelo.obj', collect_faces=True)
    #objeto = Wavefront('OBJS/MercedezB/Mercedez.obj', collect_faces=True)


    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        # ROTAÇÃO COM O MOUSE
        dx, dy = pygame.mouse.get_rel()
        yaw += dx * sensitivity     # Rotação horizontal com o mouse
        pitch += dy * sensitivity   # Inclinação vertical com o mouse

        # Vetor de direção atualizado com base em yaw/pitch
        dir_x, dir_y, dir_z = update_camera_direction()

        keys = pygame.key.get_pressed()

        # MOVIMENTO COM TECLAS
        if keys[K_w]:
            camera_x += dir_x * 0.2
            camera_y += dir_y * 0.2
            camera_z += dir_z * 0.2
        if keys[K_s]:
            camera_x -= dir_x * 0.2
            camera_y -= dir_y * 0.2
            camera_z -= dir_z * 0.2
        if keys[K_a]:
            camera_x += dir_z * 0.2
            camera_z -= dir_x * 0.2
        if keys[K_d]:
            camera_x -= dir_z * 0.2
            camera_z += dir_x * 0.2
        if keys[K_PAGEUP]:
            camera_y += 0.2
        if keys[K_PAGEDOWN]:
            camera_y -= 0.2

         # Rotação da cena com teclas Q/E (giro Y) e R/F (inclinação X)
        if keys[K_q]: rot_y -= 1                           # Gira cena para esquerda (eixo Y)
        if keys[K_e]: rot_y += 1                           # Gira para direita
        if keys[K_r]: rot_x -= 1                           # Inclina para cima (eixo X)
        if keys[K_f]: rot_x += 1                           # Inclina para baixo


        # POSIÇÃO E DIREÇÃO DA CÂMERA (gluLookAt)
        glLoadIdentity()
        gluLookAt(camera_x, camera_y, camera_z,
                  camera_x + dir_x, camera_y + dir_y, camera_z + dir_z,
                  0, 1, 0)

        glRotatef(rot_x, 1, 0, 0)                                # Rotação vertical
        glRotatef(rot_y, 0, 1, 0)                                # Rotação horizontal


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Desenha o cubo original
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glPushMatrix()
        glTranslatef(1.3, -100, 0)  # Cubo no centro
        draw_textured_cube()
        glPopMatrix()
        
        #draw grass
        glBindTexture(GL_TEXTURE_2D, grass_tex)
        glPushMatrix()
        draw_floor_plane(0,-3,0,0,0,0,10)
        glPopMatrix()

        # draw cat
        glPushMatrix() # Salva a matriz de transformações atual (empilha no stack)
        glTranslatef(4, -1.2, 0)  # Muda posição ao lado do cubo
        glRotatef(180, 0, 1, 0)  # Rotaciona o objeto no Eixo X as coordenadas iniciais deixam o gato virado
        glRotatef(-90, 1, 0, 0)  # Rotaciona o objeto no Eixo X as coordenadas iniciais deixam o gato virado
        glRotatef(45,0,0,1)
        glScalef(0.02, 0.02, 0.02)  # Reduz o tamanho do objeto se for muito grande
        #glBindTexture(GL_TEXTURE_2D, cat_tex)   # <-- vincula a textura do gato
        draw_obj_model(cat_obj, cat_tex)
        glPopMatrix() # Restaura a matriz de transformações anterior (desempilha)

        # draw tree
        glPushMatrix()
        glTranslatef(4,-2,0)
        glRotatef(180,0,1,0)
        glScalef(0.2, 0.2, 0.2)

        draw_obj_model(tree_obj, tex_id)
        glPopMatrix()

        # draw cardboard box
        glPushMatrix()
        glTranslatef(3,-2.5,0)
        glRotate(45,0,1,0)
        glScalef(0.5,0.5,0.5)

        draw_obj_model(box_obj,box_tex)
        glPopMatrix()
        
        pygame.display.flip()

    pygame.quit()

# Inicia o programa
main()
