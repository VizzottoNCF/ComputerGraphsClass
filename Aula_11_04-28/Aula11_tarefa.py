import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image


# Variáveis globais de posição e rotação da câmera
camera_x, camera_y, camera_z = 0, 0, -10  # Define a posição inicial da câmera (afastada no eixo Z)
rot_x, rot_y = 0, 0                       # Ângulos de rotação da câmera (x para inclinar, y para girar)

# Função que carrega uma imagem e a transforma em textura OpenGL
def load_texture(filename):
    img = Image.open(filename)                           # Abre a imagem com Pillow
    img = img.transpose(Image.FLIP_TOP_BOTTOM)           # Inverte verticalmente (OpenGL considera origem no canto inferior)
    img_data = img.convert("RGBA").tobytes()             # Converte a imagem para bytes RGBA
    width, height = img.size                             # Obtém tamanho da imagem

    tex_id = glGenTextures(1)                            # Gera um novo ID de textura
    glBindTexture(GL_TEXTURE_2D, tex_id)                 # Ativa o ID gerado para as próximas operações
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)  # Cria a textura no OpenGL

    # Define como a textura será tratada:
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)      # Repetir horizontalmente
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)      # Repetir verticalmente
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # Suavizar ao ampliar
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # Suavizar ao reduzir

    return tex_id  # Retorna o ID da textura para uso posterior



# Função que desenha um cubo com textura aplicada, face por face
def draw_textured_cube(xPos = 0, yPos = 0, zPos = 0, xRot= 0, yRot = 0, zRot = 0, xSca = 1, ySca = 1, zSca = 1):
    #saves matrix
    glPushMatrix()

    glTranslatef(xPos, yPos, zPos)
    glRotatef(1,xRot, yRot, zRot)
    glScalef(xSca,ySca,zSca)

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

    glEnd()  
    #restores matrix
    glPopMatrix() 

def draw_floor_plane(xPos = 0, yPos = 0, zPos = 0, xRot= 0, yRot = 0, zRot = 0, size = 1):
    #saves current matrix
    glPushMatrix()
    glTranslate(xPos,yPos,zPos)
    glRotatef(1, xRot,yRot,zRot)
    
    glBegin(GL_QUADS)

    # setting plane in XZ axis (y = 0)
    glTexCoord2f(0, 0); glVertex3f(-size, 0, -size)
    glTexCoord2f(1, 0); glVertex3f(size, 0, -size)
    glTexCoord2f(1, 1); glVertex3f(size, 0, size)
    glTexCoord2f(0, 1); glVertex3f(-size, 0, size)

    glEnd()

    # restores matrix
    glPopMatrix()

def draw_wall_plane(xPos = 0, yPos = 0, zPos = 0, xRot= 0, yRot = 0, zRot = 0, size = 1):
    #saves current matrix
    glPushMatrix()
    glTranslate(xPos,yPos,zPos)
    glRotatef(90, xRot,yRot,zRot)

    glBegin(GL_QUADS)

    # setting plane in YZ axis (vertical)
    glTexCoord2f(0, 0); glVertex3f(-size, -size, 0)
    glTexCoord2f(1, 0); glVertex3f(size, -size, 0)
    glTexCoord2f(1, 1); glVertex3f(size, size, 0)
    glTexCoord2f(0, 1); glVertex3f(-size, size, 0)

    glEnd()

    # restores matrix
    glPopMatrix()


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

# Função para configurar o ambiente OpenGL (chamada uma vez no início)
def init_opengl(display):
    glEnable(GL_DEPTH_TEST)                 # Ativa o teste de profundidade (necessário para renderização 3D correta)
    glEnable(GL_TEXTURE_2D)                 # Ativa o uso de texturas 2D

    # Define iluminação ambiente básica
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (1.0, 1.0, 1.0, 1.0))  # Luz ambiente leve (cinza)

    # Configura uma luz pontual (GL_LIGHT0)
    glEnable(GL_LIGHTING)                   # Ativa o sistema de iluminação do OpenGL
    glEnable(GL_LIGHT0)                     # Ativa a luz 0
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 5, 5, 1))          # Posição da luz no espaço 3D
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1))     # Componente difusa (cor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1))    # Componente especular (brilho)

    # Define propriedades do material aplicado ao cubo
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))  # Reflexão ambiente e difusa
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))             # Reflexão especular (brilho branco)
    glMaterialf(GL_FRONT, GL_SHININESS, 80)                               # Fator de brilho

    # Define projeção de perspectiva (campo de visão, proporção, plano próximo e distante)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Função principal do programa
def main():
    pygame.init()                                          # Inicializa o Pygame
    display = (800, 600)                                   # Define tamanho da janela
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)   # Cria janela com OpenGL e buffer duplo

    init_opengl(display)                                   # Chama configuração do ambiente OpenGL

    # carrega as duas texturas
    tex_id = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_11_04-28/textura.jpg")
    tex2_id = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_11_04-28/careca.png")
    tex3_id = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_11_04-28/grass.jpg")
    tex4_id = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_11_04-28/brick.jpg")
    # tex5_id = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_11_04-28/")
    # tex6_id = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_11_04-28/")
    # tex7_id = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_11_04-28/")
    # tex8_id = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_11_04-28/")
    # tex9_id = load_texture("C:/Users/T-GAMER/Pictures/Faculdade/ComputerGraphics/Aula_11_04-28/")

    clock = pygame.time.Clock()                            # Relógio para limitar FPS
    global camera_x, camera_y, camera_z, rot_x, rot_y      # Acessa variáveis globais da câmera

    running = True
    while running:
        clock.tick(60)                                     # Limita a 60 frames por segundo

        for event in pygame.event.get():                   # Captura eventos (ex: fechar a janela)
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()                    # Captura teclas pressionadas

        # Translação da câmera com teclas WASD e profundidade com W/S
        if keys[K_w]: camera_z += 0.1                      # Move para frente
        if keys[K_s]: camera_z -= 0.1                      # Move para trás
        if keys[K_a]: camera_x += 0.1                      # Move para a esquerda
        if keys[K_d]: camera_x -= 0.1                      # Move para a direita

        # Rotação da cena com teclas Q/E (giro Y) e R/F (inclinação X)
        if keys[K_q]: rot_y -= 1                           # Gira cena para esquerda (eixo Y)
        if keys[K_e]: rot_y += 1                           # Gira para direita
        if keys[K_r]: rot_x -= 1                           # Inclina para cima (eixo X)
        if keys[K_f]: rot_x += 1                           # Inclina para baixo


        # target point for camera
        target_x = camera_x
        target_y = camera_y
        target_z = camera_z + 1

        glLoadIdentity()
        
        
        gluLookAt(camera_x, camera_y, camera_z,  # posição da câmera no mundo 3D (olho)
                  target_x, target_y, target_z,  # ponto para onde a câmera está olhando, vai virar a lente nesta direção
                  0, 1, 0)                       # vetor 'para cima' (eixo Y positivo) Isso evita que a imagem fique de cabeça para baixo.
        
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        # Limpa buffers de cor e profundidade para novo frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # apply textures and render
        #cubes
        glBindTexture(GL_TEXTURE_2D, tex_id)
        draw_textured_cube()

        glBindTexture(GL_TEXTURE_2D, tex2_id)
        draw_textured_cube(3)

        # floor
        glBindTexture(GL_TEXTURE_2D, tex3_id)
        draw_floor_plane(0,-2,0,0,0,0,20)

        # walls
        glBindTexture(GL_TEXTURE_2D, tex4_id)
        draw_wall_plane(0,2,4,0,0,0,5)
        draw_wall_plane(10,2,-5,0,1,0,5)

        pygame.display.flip()

    pygame.quit()  # Finaliza o Pygame

# Inicia o programa
main()