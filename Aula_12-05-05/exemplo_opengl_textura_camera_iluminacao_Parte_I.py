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


# Variáveis globais de posição e rotação da câmera
camera_x, camera_y, camera_z = 0, 0, -5  # Câmera posicionada de frente para o cubo
yaw = 0                            # Ângulo de rotação horizontal (inicialmente olhando para Z positivo)
pitch = 0                          # Ângulo de rotação vertical
sensitivity = 0.02                 # Sensibilidade do mouse para rotação
rot_x, rot_y = 0, 0                # Ângulos de rotação da cena (x para inclinar, y para girar)


# Atualiza a direção de visão da câmera com base em yaw e pitch
def update_camera_direction():
    rad_yaw   = math.radians(yaw)
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
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    return tex_id

# function that draws cube with texture
def draw_textured_cube():
    glBegin(GL_QUADS)  


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



# Configura o OpenGL (textura, profundidade, iluminação)
def init_opengl(display):
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (1.0, 1.0, 1.0, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 5, 5, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1.0, 1.0, 1.0, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1))

    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR,            (1.0, 1.0, 1.0, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, 80)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Função principal
def main():
    global camera_x, camera_y, camera_z, yaw, pitch, rot_x, rot_y

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    init_opengl(display)
    tex_id = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_12-05-05/textura.jpg")  # cubo

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Captura movimento do mouse para yaw/pitch
        dx, dy = pygame.mouse.get_rel()
        yaw   += dx * sensitivity
        pitch += dy * sensitivity

        # Atualiza vetor de direção
        dir_x, dir_y, dir_z = update_camera_direction()

        keys = pygame.key.get_pressed()
        # W/S: mover para frente/trás
        if keys[K_w]:
            camera_x += dir_x * 0.05; 
            camera_y += dir_y * 0.05; 
            camera_z += dir_z * 0.05

        if keys[K_s]:
            camera_x -= dir_x * 0.05; 
            camera_y -= dir_y * 0.05; 
            camera_z -= dir_z * 0.05

        # A/D: movimentar lateralmente (strafe)
        if keys[K_a]:
            camera_x += dir_z * 0.05; 
            camera_z -= dir_x * 0.05
        if keys[K_d]:
            camera_x -= dir_z * 0.05; 
            camera_z += dir_x * 0.05

        # PAGEUP/PAGEDOWN: subir/descer
        if keys[K_PAGEUP]:
            camera_y += 0.05
        if keys[K_PAGEDOWN]:
            camera_y -= 0.05

        # Q/E e R/F: girar/inclinar cena
        if keys[K_q]: rot_y -= 1
        if keys[K_e]: rot_y += 1
        if keys[K_r]: rot_x -= 1
        if keys[K_f]: rot_x += 1

        # Ajusta view
        glLoadIdentity()
        gluLookAt(camera_x, camera_y, camera_z,
                  camera_x + dir_x, camera_y + dir_y, camera_z + dir_z,
                  0, 1, 0)
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        # Limpa e desenha o cubo texturizado
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glPushMatrix()
        glTranslatef(0, 0, 0)
        draw_textured_cube()
        glPopMatrix()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


