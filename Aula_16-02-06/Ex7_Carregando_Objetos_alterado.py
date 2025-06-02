# Ex7_Carregando_Objeto.py
# Renderiza um modelo OBJ com textura usando OpenGL moderno (VAO/VBO, shaders).
# Simplificado: carrega apenas vértices e UVs (sem normais) para facilitar o entendimento.
#
# Arquivos necessários na mesma pasta:
#   - chibi.obj          : modelo 3D
#   - chibi.png          : textura PNG
#   - Camera.py          : classe Camera (yaw/pitch, get_view_matrix, process_keyboard)
#   - TextureLoader.py   : função load_texture(path, texture_id)
#   - ObjLoaderSimple.py : função load_obj(path) → (vertex_buffer, num_vertices)

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from TextureLoader import load_texture      # Carrega imagens PNG como textura OpenGL
from Camera import Camera                   # Gera a view matrix a partir de yaw/pitch
from ObjLoaderSimple import ObjLoaderSimple # Loader simples que retorna (buffer, num_vertices)
import pyrr
from pyrr import matrix44, Vector3    # ← adicione esta linha
import ctypes

# --- Parâmetros da janela ---
WIDTH, HEIGHT = 800, 600

# --- Variáveis globais ---
Window = None           # Handle da janela GLFW
Shader_programm = None  # ID do programa de shaders
vao_objeto = None       # ID do VAO do objeto
num_vertices = 0        # Quantidade de vértices a desenhar
obj_textura = None      # ID da textura UV

# Instância da câmera para controle WASD
cam = Camera()

# ----------------------------------------
# Configurações de GLFW e OpenGL
# ----------------------------------------

def redimensiona_callback(window, w, h):
    """
    Chamado quando a janela é redimensionada.
    Ajusta as variáveis WIDTH e HEIGHT para manter a proporção.
    """
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = w, h
    glViewport(0, 0, WIDTH, HEIGHT)

def teclado_callback(window, key, scancode, action, mods):
    """
    Fechar a janela ao pressionar ESC.
    """
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)



# Guarda a última posição do mouse
first_mouse = True
lastX, lastY = WIDTH/2, HEIGHT/2

def mouse_callback(window, xpos, ypos):
    global first_mouse, lastX, lastY
    if first_mouse:
        lastX, lastY = xpos, ypos
        first_mouse = False

    # offset = nova posição – posição anterior
    xoffset = xpos - lastX
    yoffset = lastY - ypos      # invertendo y para que “pra cima” seja positivo

    lastX, lastY = xpos, ypos

    # chama o método da câmera
    cam.process_mouse_movement(xoffset, yoffset)




def inicializa_opengl():
    """
    Inicializa GLFW, cria a janela e configura callbacks.
    """
    global Window
    if not glfw.init():
        raise RuntimeError("Falha ao inicializar GLFW")
    Window = glfw.create_window(WIDTH, HEIGHT, "Ex7 - OBJ com Textura", None, None)
    if not Window:
        glfw.terminate()
        raise RuntimeError("Falha ao criar janela")
    
    # redimensiona e teclado continuam como antes…
    glfw.set_window_size_callback(Window, redimensiona_callback)  
    glfw.set_key_callback(Window, teclado_callback)
    glfw.make_context_current(Window)
    
    # esconde e captura o cursor para receber movimento contínuo
    glfw.set_input_mode(Window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    # registra nosso callback
    glfw.set_cursor_pos_callback(Window, mouse_callback)

    # Ativa teste de profundidade
    glEnable(GL_DEPTH_TEST) 

    print("OpenGL:", glGetString(GL_VERSION).decode())

# ----------------------------------------
# Carregamento de objeto e textura
# ----------------------------------------

def inicializa_chibi():
    """
    Carrega vértices e UVs via load_obj(),
    cria VAO/VBO e configura atributos de vértice.
    Também carrega a textura chibi.png.
    """
    global vao_chibi, num_vertices_chibi, obj_textura_chibi

    # load_obj retorna (vertex_buffer, num_vertices)
    buffer, num_vertices_chibi = ObjLoaderSimple.load_obj("Aula_16-02-06/meshes/chibi.obj")
    buffer = buffer.astype(np.float32)

    # Gera e vincula VAO
    vao_chibi = glGenVertexArrays(1)
    glBindVertexArray(vao_chibi)

    # Gera VBO e envia dados
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

    # Cada vértice: 5 floats → [x,y,z, u,v]
    stride = buffer.itemsize * 5
    # Posição (vec3) no location=0
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    # UV (vec2) no location=1
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(buffer.itemsize * 3))

    # Carrega textura
    obj_textura_chibi = glGenTextures(1)
    #load_texture("textures/chibi.png", obj_textura)
    load_texture("Aula_16-02-06/textures/chibi.png", obj_textura_chibi)

   
# ----------------------------------------
# Carregamento de objeto e textura
# ----------------------------------------

def inicializa_gato():
    """
    Carrega vértices e UVs via load_obj(),
    cria VAO/VBO e configura atributos de vértice.
    Também carrega a textura chibi.png.
    """
    global vao_gato, num_vertices_gato, obj_textura_gato

    # load_obj retorna (vertex_buffer, num_vertices)
    buffer, num_vertices_gato = ObjLoaderSimple.load_obj("Aula_16-02-06/meshes/Cat/Cat_blender2.obj")
    buffer = buffer.astype(np.float32)

    # Gera e vincula VAO
    vao_gato = glGenVertexArrays(1)
    glBindVertexArray(vao_gato)

    # Gera VBO e envia dados
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

    # Cada vértice: 5 floats → [x,y,z, u,v]
    stride = buffer.itemsize * 5
    # Posição (vec3) no location=0
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    # UV (vec2) no location=1
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(buffer.itemsize * 3))

    # Carrega textura
    obj_textura_gato = glGenTextures(1)
    #load_texture("textures/chibi.png", obj_textura)
    load_texture("Aula_16-02-06/textures/Cat_diffuse.jpg", obj_textura_gato)

def inicializa_grass():
    """
    Carrega vértices e UVs via load_obj(),
    cria VAO/VBO e configura atributos de vértice.
    Também carrega a textura chibi.png.
    """
    global vao_grass, num_vertices_grass, obj_textura_grass

    # load_obj retorna (vertex_buffer, num_vertices)
    buffer, num_vertices_grass = ObjLoaderSimple.load_obj("Aula_16-02-06/meshes/Grass_blender.obj")
    buffer = buffer.astype(np.float32)

    # Gera e vincula VAO
    vao_grass = glGenVertexArrays(1)
    glBindVertexArray(vao_grass)

    # Gera VBO e envia dados
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

    # Cada vértice: 5 floats → [x,y,z, u,v]
    stride = buffer.itemsize * 5
    # Posição (vec3) no location=0
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    # UV (vec2) no location=1
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(buffer.itemsize * 3))

    # Carrega textura
    obj_textura_grass = glGenTextures(1)
    #load_texture("textures/chibi.png", obj_textura)
    load_texture("Aula_16-02-06/textures/10450_Rectangular_Grass_Patch_v1_Diffuse.jpg", obj_textura_grass)

def inicializa_can():
    """
    Carrega vértices e UVs via load_obj(),
    cria VAO/VBO e configura atributos de vértice.
    Também carrega a textura chibi.png.
    """
    global vao_can, num_vertices_can, obj_textura_can

    # load_obj retorna (vertex_buffer, num_vertices)
    buffer, num_vertices_can = ObjLoaderSimple.load_obj("Aula_16-02-06/meshes/Can_blender.obj")
    buffer = buffer.astype(np.float32)

    # Gera e vincula VAO
    vao_can = glGenVertexArrays(1)
    glBindVertexArray(vao_can)

    # Gera VBO e envia dados
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

    # Cada vértice: 5 floats → [x,y,z, u,v]
    stride = buffer.itemsize * 5
    # Posição (vec3) no location=0
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    # UV (vec2) no location=1
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(buffer.itemsize * 3))

    # Carrega textura
    obj_textura_can = glGenTextures(1)
    #load_texture("textures/chibi.png", obj_textura)
    load_texture("Aula_16-02-06/textures/Coca-Cola01.jpg", obj_textura_can)

def inicializa_bird():
    """
    Carrega vértices e UVs via load_obj(),
    cria VAO/VBO e configura atributos de vértice.
    Também carrega a textura chibi.png.
    """
    global vao_bird, num_vertices_bird, obj_textura_bird

    # load_obj retorna (vertex_buffer, num_vertices)
    buffer, num_vertices_bird = ObjLoaderSimple.load_obj("Aula_16-02-06/meshes/Bird_blender.obj")
    buffer = buffer.astype(np.float32)

    # Gera e vincula VAO
    vao_bird = glGenVertexArrays(1)
    glBindVertexArray(vao_bird)

    # Gera VBO e envia dados
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

    # Cada vértice: 5 floats → [x,y,z, u,v]
    stride = buffer.itemsize * 5
    # Posição (vec3) no location=0
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    # UV (vec2) no location=1
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(buffer.itemsize * 3))

    # Carrega textura
    obj_textura_bird = glGenTextures(1)
    #load_texture("textures/chibi.png", obj_textura)
    load_texture("Aula_16-02-06/textures/12248_Bird_v1_diff.jpg", obj_textura_bird)

def inicializa_animal():
    """
    Carrega vértices e UVs via load_obj(),
    cria VAO/VBO e configura atributos de vértice.
    Também carrega a textura chibi.png.sa
    """
    global vao_animal, num_vertices_animal, obj_textura_animal

    # load_obj retorna (vertex_buffer, num_vertices)
    buffer, num_vertices_animal = ObjLoaderSimple.load_obj("Aula_16-02-06/meshes/Animal_blender.obj")
    buffer = buffer.astype(np.float32)

    # Gera e vincula VAO
    vao_animal = glGenVertexArrays(1)
    glBindVertexArray(vao_animal)

    # Gera VBO e envia dados
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

    # Cada vértice: 5 floats → [x,y,z, u,v]
    stride = buffer.itemsize * 5
    # Posição (vec3) no location=0
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    # UV (vec2) no location=1
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(buffer.itemsize * 3))

    # Carrega textura
    obj_textura_animal = glGenTextures(1)
    #load_texture("textures/chibi.png", obj_textura)
    load_texture("Aula_16-02-06/textures/11706_toy_dog_diffuse_v2.jpg", obj_textura_animal)

def inicializa_wall():
    """
    Carrega vértices e UVs via load_obj(),
    cria VAO/VBO e configura atributos de vértice.
    Também carrega a textura chibi.png.sa
    """
    global vao_wall, num_vertices_wall, obj_textura_wall

    # load_obj retorna (vertex_buffer, num_vertices)
    buffer, num_vertices_wall = ObjLoaderSimple.load_obj("Aula_16-02-06/meshes/Wall_blender.obj")
    buffer = buffer.astype(np.float32)

    # Gera e vincula VAO
    vao_wall = glGenVertexArrays(1)
    glBindVertexArray(vao_wall)

    # Gera VBO e envia dados
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

    # Cada vértice: 5 floats → [x,y,z, u,v]
    stride = buffer.itemsize * 5
    # Posição (vec3) no location=0
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    # UV (vec2) no location=1
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(buffer.itemsize * 3))

    # Carrega textura
    obj_textura_wall = glGenTextures(1)
    #load_texture("textures/chibi.png", obj_textura)
    load_texture("Aula_16-02-06/textures/CinderblockSloppy0005_1_S.jpg", obj_textura_wall)

# ----------------------------------------
# Compilação dos shaders
# ----------------------------------------

def inicializa_shaders():
    """
    Cria, compila e linka vertex e fragment shader simplificados:
    - Vertex shader recebe:
        • layout(location = 0) in vec3 in_pos;    → atributo de posição do vértice (x,y,z)
        • layout(location = 1) in vec2 in_uv;     → atributo de coordenada de textura (u,v)
        • uniform mat4 model;                     → matriz de modelo (transformação local do objeto)
        • uniform mat4 view;                      → matriz de visualização (posição/orientação da câmera)
        • uniform mat4 projection;                → matriz de projeção (perspectiva)
      e repassa in_uv para o fragment shader em out vec2 frag_uv.

    - Fragment shader recebe:
        • in vec2 frag_uv;                        → UV interpolada do vertex shader
        • uniform sampler2D texture1;             → sampler que indica a textura vinculada ao texture unit 0
      e gera a cor final em out vec4 FragColor.

    Após definir as fontes, compilamos e linkamos:
    - compileShader(source, type): compila um shader de tipo GL_VERTEX_SHADER ou GL_FRAGMENT_SHADER.
    - compileProgram(vs, fs): linka os shaders compilados em um programa executável pelo glUseProgram.
    """
    
    global Shader_programm

    vertex_src = """#version 400
        layout(location = 0) in vec3 in_pos;    // posição do vértice
        layout(location = 1) in vec2 in_uv;     // coordenada de textura
        uniform mat4 model;                     // matriz de modelo
        uniform mat4 view;                      // matriz de visualização
        uniform mat4 projection;                // matriz de projeção
        out vec2 frag_uv;                       // repassa UV
        void main() {
            frag_uv = in_uv;
            gl_Position = projection * view * model * vec4(in_pos, 1.0);
        }"""

    fragment_src = """#version 400
        in vec2 frag_uv;                         // UV interpolada
        uniform sampler2D texture1;              // textura vinculada
        out vec4 FragColor;
        void main() {
            FragColor = texture(texture1, frag_uv);
        }"""

    # Compila shaders
    vs = OpenGL.GL.shaders.compileShader(vertex_src, GL_VERTEX_SHADER)
    fs = OpenGL.GL.shaders.compileShader(fragment_src, GL_FRAGMENT_SHADER)
    Shader_programm = OpenGL.GL.shaders.compileProgram(vs, fs)

# ----------------------------------------
# Loop de renderização
# ----------------------------------------

def render_loop():
    """
    Loop principal que:
    - Processa movimento da câmera (WASD)
    - Limpa buffers
    - Atualiza matrizes uniformes
    - Renderiza objeto via glDrawArrays
    """

    # Inicializa a matriz de modelo como IDENTIDADE:
    # - A matriz identidade é o “elemento neutro” das transformações,
    #   ou seja, não altera posição, rotação ou escala do objeto.
    # - A partir dela, aplicamos translações, rotações ou escalas
    #   usando multiplcações ou substituições.
    # - Se fosse uma matriz de zeros, todas as coordenadas seriam zeradas
    #   e o objeto não apareceria na cena

    # Matriz de modelo fixa
    model = pyrr.matrix44.create_identity(dtype=np.float32)

    # Tempo da frame anterior
    last_time = glfw.get_time()
    # Velocidade da câmera em unidades do mundo por segundo
    base_speed = 10.0

    while not glfw.window_should_close(Window):
       
        # --- calcula deltaTime ---
        current_time = glfw.get_time()
        delta = current_time - last_time
        last_time = current_time

        # Movimento da câmera
        # --- movimenta a câmera usando deltaTime ---
        vel = base_speed * delta  # unidades por frame

        if glfw.get_key(Window, glfw.KEY_W) == glfw.PRESS:
            cam.process_keyboard("FORWARD", vel)
        if glfw.get_key(Window, glfw.KEY_S) == glfw.PRESS:
            cam.process_keyboard("BACKWARD", vel)
        if glfw.get_key(Window, glfw.KEY_A) == glfw.PRESS:
            cam.process_keyboard("LEFT", vel)
        if glfw.get_key(Window, glfw.KEY_D) == glfw.PRESS:
            cam.process_keyboard("RIGHT", vel)

        # Limpa a tela
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(Shader_programm)

        # Atualiza matrizes de view e projection
        view = cam.get_view_matrix()
        projection = pyrr.matrix44.create_perspective_projection_matrix(
            45.0, WIDTH/HEIGHT, 0.1, 100.0
        )

        # Sends Uniform - CHIBI
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "model"), 1, GL_FALSE, model)  
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "projection"), 1, GL_FALSE, projection)

        # Draws - CHIBI
        glBindVertexArray(vao_chibi)
        glBindTexture(GL_TEXTURE_2D, obj_textura_chibi)
        glDrawArrays(GL_TRIANGLES, 0, num_vertices_chibi)
        

        # ----------------------------------------
        # CAT

        # translate matrix pyrr.matrix44.create_from_translation(pyrr.Vector3([X, Y, Z]))
        # rotate matrix - pyrr.matrix44.create_from_(X/Y/Z)_rotation(np.radians(0))
        # scale matrix - pyrr.matrix44.create_from_scale(pyrr.Vector3([X, Y, Z]))
        rot_gato = pyrr.matrix44.create_from_x_rotation(np.radians(0))
        trans_gato = pyrr.matrix44.create_from_translation(pyrr.Vector3([30.0, 0.0, 0.0]))
        escala_gato = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.2, 0.2, 0.2]))

        # Applies matrix changes: (Translação * Rotação * Escala)
        model_gato = pyrr.matrix44.multiply(rot_gato, escala_gato)
        model_gato = pyrr.matrix44.multiply(trans_gato, model_gato)

        # Send Uniforms
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "model"), 1, GL_FALSE, model_gato)  
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "projection"), 1, GL_FALSE, projection)

        # Draws - CAT
        glBindVertexArray(vao_gato)
        glBindTexture(GL_TEXTURE_2D, obj_textura_gato)
        glDrawArrays(GL_TRIANGLES, 0, num_vertices_gato)

        # ----------------------------------------
        # GRASS

        # translate matrix pyrr.matrix44.create_from_translation(pyrr.Vector3([X, Y, Z]))
        # rotate matrix - pyrr.matrix44.create_from_(X/Y/Z)_rotation(np.radians(0))
        # scale matrix - pyrr.matrix44.create_from_scale(pyrr.Vector3([X, Y, Z]))
        rot_grass = pyrr.matrix44.create_from_x_rotation(np.radians(0))
        trans_grass = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, -10.0, 0.0]))
        escala_grass = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.2, 0.2, 0.2]))

        # Applies matrix changes: (Translação * Rotação * Escala)
        model_grass = pyrr.matrix44.multiply(rot_grass, escala_grass)
        model_grass = pyrr.matrix44.multiply(trans_grass, model_grass)

        # Send Uniforms
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "model"), 1, GL_FALSE, model_grass)  
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "projection"), 1, GL_FALSE, projection)

        # Draws - GRASS
        glBindVertexArray(vao_grass)
        glBindTexture(GL_TEXTURE_2D, obj_textura_grass)
        glDrawArrays(GL_TRIANGLES, 0, num_vertices_grass)

        # ----------------------------------------
        # CAN

        # translate matrix pyrr.matrix44.create_from_translation(pyrr.Vector3([X, Y, Z]))
        # rotate matrix - pyrr.matrix44.create_from_(X/Y/Z)_rotation(np.radians(0))
        # scale matrix - pyrr.matrix44.create_from_scale(pyrr.Vector3([X, Y, Z]))
        rot_can = pyrr.matrix44.create_from_x_rotation(np.radians(0))
        trans_can = pyrr.matrix44.create_from_translation(pyrr.Vector3([-250.0, 0.0, 0.0]))
        escala_can = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.02, 0.02, 0.02]))

        # Applies matrix changes: (Translação * Rotação * Escala)
        model_can = pyrr.matrix44.multiply(rot_can, escala_can)
        model_can = pyrr.matrix44.multiply(trans_can, model_can)

        # Send Uniforms
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "model"), 1, GL_FALSE, model_can)  
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "projection"), 1, GL_FALSE, projection)

        # Draws - CAN
        glBindVertexArray(vao_can)
        glBindTexture(GL_TEXTURE_2D, obj_textura_can)
        glDrawArrays(GL_TRIANGLES, 0, num_vertices_can)

        # ----------------------------------------
        # BIRD

        # translate matrix pyrr.matrix44.create_from_translation(pyrr.Vector3([X, Y, Z]))
        # rotate matrix - pyrr.matrix44.create_from_(X/Y/Z)_rotation(np.radians(0))
        # scale matrix - pyrr.matrix44.create_from_scale(pyrr.Vector3([X, Y, Z]))
        rot_bird = pyrr.matrix44.create_from_x_rotation(np.radians(0))
        trans_bird = pyrr.matrix44.create_from_translation(pyrr.Vector3([120.0, 0.0, 0.0]))
        escala_bird = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.1, 0.1, 0.1]))

        # Applies matrix changes: (Translação * Rotação * Escala)
        model_bird = pyrr.matrix44.multiply(rot_bird, escala_bird)
        model_bird = pyrr.matrix44.multiply(trans_bird, model_bird)

        # Send Uniforms
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "model"), 1, GL_FALSE, model_bird)  
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "projection"), 1, GL_FALSE, projection)

        # Draws - BIRD
        glBindVertexArray(vao_bird)
        glBindTexture(GL_TEXTURE_2D, obj_textura_bird)
        glDrawArrays(GL_TRIANGLES, 0, num_vertices_bird)


        # ----------------------------------------
        # ANIMAL

        # translate matrix pyrr.matrix44.create_from_translation(pyrr.Vector3([X, Y, Z]))
        # rotate matrix - pyrr.matrix44.create_from_(X/Y/Z)_rotation(np.radians(0))
        # scale matrix - pyrr.matrix44.create_from_scale(pyrr.Vector3([X, Y, Z]))
        rot_animal = pyrr.matrix44.create_from_x_rotation(np.radians(0))
        trans_animal = pyrr.matrix44.create_from_translation(pyrr.Vector3([-50.0, 0.0, 0.0]))
        escala_animal = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.2, 0.2, 0.2]))

        # Applies matrix changes: (Translação * Rotação * Escala)
        model_animal = pyrr.matrix44.multiply(rot_animal, escala_animal)
        model_animal = pyrr.matrix44.multiply(trans_animal, model_animal)

        # Send Uniforms
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "model"), 1, GL_FALSE, model_animal)  
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "projection"), 1, GL_FALSE, projection)

        # Draws - ANIMAL
        glBindVertexArray(vao_animal)
        glBindTexture(GL_TEXTURE_2D, obj_textura_animal)
        glDrawArrays(GL_TRIANGLES, 0, num_vertices_animal)


        # ----------------------------------------
        # WALL

        # translate matrix pyrr.matrix44.create_from_translation(pyrr.Vector3([X, Y, Z]))
        # rotate matrix - pyrr.matrix44.create_from_(X/Y/Z)_rotation(np.radians(0))
        # scale matrix - pyrr.matrix44.create_from_scale(pyrr.Vector3([X, Y, Z]))
        rot_wall = pyrr.matrix44.create_from_x_rotation(np.radians(0))
        trans_wall = pyrr.matrix44.create_from_translation(pyrr.Vector3([-0.5, 0.3, -1.0]))
        escala_wall = pyrr.matrix44.create_from_scale(pyrr.Vector3([20, 10, 10]))

        # Applies matrix changes: (Translação * Rotação * Escala)
        model_wall = pyrr.matrix44.multiply(rot_wall, escala_wall)
        model_wall = pyrr.matrix44.multiply(trans_wall, model_wall)

        # Send Uniforms
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "model"), 1, GL_FALSE, model_wall)  
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "projection"), 1, GL_FALSE, projection)

        # Draws - WALL
        glBindVertexArray(vao_wall)
        glBindTexture(GL_TEXTURE_2D, obj_textura_wall)
        glDrawArrays(GL_TRIANGLES, 0, num_vertices_wall)


        # ----------------------------------------
        # Troca buffers e coleta eventos
        glfw.swap_buffers(Window)
        glfw.poll_events()

    glfw.terminate()

# ----------------------------------------
# Função principal
# ----------------------------------------

def main():
    inicializa_opengl()
    inicializa_chibi()
    inicializa_gato()
    inicializa_grass()
    inicializa_can()
    inicializa_bird()
    inicializa_animal()
    inicializa_wall()
    inicializa_shaders()
    render_loop()

if __name__ == "__main__":
    main()
