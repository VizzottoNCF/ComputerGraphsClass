import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

Window = None
Shader_programm = None
Vao = None
cvbo = None
pvbo = None
WIDTH = 1000
HEIGHT = 800
points = [[] for _ in range(3)]
colors = [[] for _ in range(3)]

# callback function that is called when the window is resized
# saves the width and height of the window in the global variables
def redimensionaCallback(window, w, h):
    global WIDTH, HEIGHT
    WIDTH = w
    HEIGHT = h

def inicializaOpenGL():
    global Window, WIDTH, HEIGHT

    # initializes GLFW
    glfw.init()

    # creates a window
    Window = glfw.create_window(WIDTH, HEIGHT, "Atividade - Renderização", None, None)

    # if Window is not able to be created, exits code
    if not Window:
        glfw.terminate()
        exit()

    # sets window size with the callback function
    glfw.set_window_size_callback(Window, redimensionaCallback)

    # defines in what window OpenGL needs to run
    glfw.make_context_current(Window)

    # hardware info
    print("Placa de vídeo: ",OpenGL.GL.glGetString(OpenGL.GL.GL_RENDERER))
    print("Versão do OpenGL: ",OpenGL.GL.glGetString(OpenGL.GL.GL_VERSION))

# create variations of this function for any shapes
def inicializaObjetos():
    # VAO unifies and represents all buffers in a single identifier
    # each object must have one VAO
    global Vao, pvbo, cvbo
    
    # generates VAOs (one for each object)
    Vao = glGenVertexArrays(3) # returns array with every id

    # generates VBOs (position + color buffers)
    pvbo = glGenBuffers(3) # point
    cvbo = glGenBuffers(3) # color

    inicializaTriangulos()
    inicializaQuadrados()
    
    # unbinds VAO
    glBindVertexArray(0)

def inicializaTriangulos():
    global Vao, pvbo, cvbo

    # Triangle 1 
    points[0] = [
        #X    Y    Z
		0.0, 0.5, 0.0,   #cima
		0.5, -0.5, 0.0,  #direita
		-0.5, -0.5, 0.0, #esquerda
	]
    colors[0] = [
        # Triangle 1
        #R    G    B
		1.0, 0.0, 0.0, 
		0.0, 1.0, 0.0, 
		0.0, 1.0, 1.0  
	]
    # transform arrays into numpy
    points[0] = np.array(points[0], dtype=np.float32)
    colors[0] = np.array(colors[0], dtype=np.float32)


    # Triangle 2
    points[1] = [
        #X    Y    Z
		0.6, -0.5, 0.0, #cima
		1.1, 0.5, 0.0,  #direita
		0.1, 0.5, 0.0   #esquerda
	]
    colors[1] = [
        #R    G    B
		0.0, 0.0, 1.0, 
		0.0, 1.0, 0.0, 
		1.0, 1.0, 0.0  
	]
    # transform arrays into numpy
    points[1] = np.array(points[1], dtype=np.float32)
    colors[1] = np.array(colors[1], dtype=np.float32)
    
    
    # only one VAO can be bound at a time. Everything a VAO is supposed to do needs to be called before changing VAO
    # Configs Triangle 1 (VAO 0)
    glBindVertexArray(Vao[0])
    # Points VBO (Triangle 1)
    glBindBuffer(GL_ARRAY_BUFFER, pvbo[0]) # binds pvbo to be manipd
    glBufferData(GL_ARRAY_BUFFER, points[0], GL_STATIC_DRAW) # copies data into VBO 
    glEnableVertexAttribArray(0) # sets information type as "Vertex Position"
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None) # setup vertices buffer layout
    # Color VBO (Triangle 1)
    glBindBuffer(GL_ARRAY_BUFFER, cvbo[0]) # binds cvbo to be manipd
    glBufferData(GL_ARRAY_BUFFER, colors[0], GL_STATIC_DRAW) # copies data into VBO
    glEnableVertexAttribArray(1) # sets information type as "Vertex Colors"
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None) # setup vertice color buffer


    # Configs Triangle 2 (VAO 1)
    glBindVertexArray(Vao[1])
    # Points VBO (Triangle 2)
    glBindBuffer(GL_ARRAY_BUFFER, pvbo[1]) # binds pvbo to be manipd
    glBufferData(GL_ARRAY_BUFFER, points[1], GL_STATIC_DRAW) # copies data into VBO 
    glEnableVertexAttribArray(0) # sets information type as "Vertex Position"
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None) # setup vertices buffer layout
    # Color VBO (Triangle 2)
    glBindBuffer(GL_ARRAY_BUFFER, cvbo[1]) # binds cvbo to be manipd
    glBufferData(GL_ARRAY_BUFFER, colors[1], GL_STATIC_DRAW) # copies data into VBO
    glEnableVertexAttribArray(1) # sets information type as "Vertex Colors"
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None) # setup vertice color buffer

    # unbinds vao
    glBindVertexArray(0)


def inicializaQuadrados():
    # Square 1 (made of two triangles)
    points[0] = [
        # Triangle 1
        #X    Y    Z
		-0.8, 1.0, 0.0, #cima
		-0.1, 1.0, 0.0, #direita
		-0.8, 0.0, 0.0, #esquerda
        
        # Triangle 2
        #X    Y    Z
		-0.1, 1.0, 0.0, #cima
		-0.1, 0.0, 0.0, #direita
		-0.8, 0.0, 0.0 #esquerda
	]
    colors[0] = [
        # Triangle 1
        #R    G    B
		0.0, 0.0, 1.0, 
		0.0, 1.0, 0.0, 
		1.0, 1.0, 0.0,

        # Triangle 2
        #R    G    B
		0.0, 0.0, 1.0, 
		0.0, 1.0, 0.0, 
		1.0, 1.0, 0.0  
	]
    # transform arrays into numpy
    points[0] = np.array(points[0], dtype=np.float32)
    colors[0] = np.array(colors[0], dtype=np.float32)

    # Configs Square (VAO 2)
    glBindVertexArray(Vao[2])
    # Points VBO (Square 1)
    glBindBuffer(GL_ARRAY_BUFFER, pvbo[2]) # binds pvbo to be manipd
    glBufferData(GL_ARRAY_BUFFER, points[0], GL_STATIC_DRAW) # copies data into VBO 
    glEnableVertexAttribArray(0) # sets information type as "Vertex Position"
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None) # setup vertices buffer layout
    # Color VBO (Triangle 2)
    glBindBuffer(GL_ARRAY_BUFFER, cvbo[2]) # binds cvbo to be manipd
    glBufferData(GL_ARRAY_BUFFER, colors[0], GL_STATIC_DRAW) # copies data into VBO
    glEnableVertexAttribArray(1) # sets information type as "Vertex Colors"
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None) # setup vertice color buffer

    # unbinds vao
    glBindVertexArray(0)


# def inicializaShaders():
#     global Shader_programm
#     # Especificação do Vertex Shader:
#     # - O Vertex Shader é responsável por processar cada vértice individualmente na GPU.
#     # - A primeira linha especifica a versão da linguagem GLSL que estamos utilizando (4.0.0).
#     # - `layout(location = 0) in vec3 vertex_posicao`:
#     #     Essa variável de entrada (in) representa a posição de cada vértice,
#     #     que é enviada pela CPU via VBO (vertex buffer object).
#     # - `layout(location = 1) in vec3 vertex_cores`:
#     #     Essa variável de entrada representa a cor associada a cada vértice.
#     # - `out vec3 cores`:
#     #     Esta é uma variável de saída do vertex shader. 
#     #     Ela serve para **passar a cor do vértice para o fragment shader**.
#     #     O OpenGL irá automaticamente interpolar esse valor entre os vértices ao longo da superfície.
#     # - Dentro da função `main()`, atribuímos a posição final do vértice à variável especial `gl_Position`,
#     #   que é obrigatória e define onde o vértice aparecerá na tela.
#     #   `gl_Position` deve ser um `vec4`, então adicionamos 1.0 como o componente `w` (homogêneo).
#     vertex_shader = """
#         #version 400
#         layout(location = 0) in vec3 vertex_posicao; //Vem do Python (IN), do VBO 0 (POSIÇÕES)
#         layout(location = 1) in vec3 vertex_cores; //Vem do Python (IN), do VBO 1 (CORES)
#         out vec3 cores;
#         void main () {
#             cores = vertex_cores;
#             gl_Position = vec4 (vertex_posicao.x, vertex_posicao.y, vertex_posicao.z, 1.0);
#         }
#     """
#     # Como os shaders são um programa "a parte", precisamos compilá-lo e verificar se não houve nenhum erro de compilação
#     vs = OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER)
#     if not glGetShaderiv(vs, GL_COMPILE_STATUS):
#         infoLog = glGetShaderInfoLog(vs, 512, None)
#         print("Erro no vertex shader:\n", infoLog)

#     # Especificação do Fragment Shader:
#     # - O Fragment Shader é executado para cada fragmento (pixel potencial) gerado durante a rasterização do objeto.
#     # - A primeira linha especifica a versão da linguagem GLSL utilizada (4.0.0).
#     # - `in vec3 cores`:
#     #     Essa variável de entrada recebe a **cor interpolada** dos vértices, vinda do vertex shader através da variável `out vec3 cores`.
#     #     O OpenGL automaticamente interpola os valores das cores ao longo dos fragmentos da superfície do triângulo.
#     # - `out vec4 frag_colour`:
#     #     Essa é a variável de saída do fragment shader. Ela define a **cor final** do pixel que será desenhado na tela.
#     #     Deve ser do tipo `vec4`, representando (R, G, B, A) — sendo `A` o canal de opacidade (alpha).
#     # - Dentro da função `main()`, atribuimos à `frag_colour` o valor da cor recebida, adicionando o valor de alpha como 1.0 (totalmente opaco).	
#     fragment_shader = """
#         #version 400
#         in vec3 cores;
# 		out vec4 frag_colour;
# 		void main () {
# 		    frag_colour = vec4 (cores.r, cores.g, cores.b, 1.0);
# 		}
#     """
#     # Do mesmo modo que o vertex shader, precisamos compilar o fragment shader e verificar se não houve nenhum erro de compilação
#     fs = OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
#     if not glGetShaderiv(fs, GL_COMPILE_STATUS):
#         infoLog = glGetShaderInfoLog(fs, 512, None)
#         print("Erro no fragment shader:\n", infoLog)

#     # Especificação do Shader Programm:
# 	# Após compilarmos os shaders, precisamos combiná-los em um único programa, denominado GPU Shader Program.
# 	# Para isso, chamamos a função compileProgram passando os dois shaders que irão formar o nosso shader program
#     # e testamos se não houve nenhum erro de linkagem
#     Shader_programm = OpenGL.GL.shaders.compileProgram(vs, fs)
#     if not glGetProgramiv(Shader_programm, GL_LINK_STATUS):
#         infoLog = glGetProgramInfoLog(Shader_programm, 512, None)
#         print("Erro na linkagem do shader:\n", infoLog)

#     glDeleteShader(vs) #depois de copiados para GPU com shader podemos liberar a memoria com 'vs e 'fs'
#     glDeleteShader(fs)

def inicializaShaderTriangulo():
    global Shader_programm_triangulo
    
    vertex_shader = """
        #version 400
        layout(location = 0) in vec3 vertex_posicao;
        layout(location = 1) in vec3 vertex_cores;
        out vec3 cores;
        void main () {
            cores = vertex_cores;
            gl_Position = vec4(vertex_posicao, 1.0);
        }
    """
    
    fragment_shader = """
        #version 400
        in vec3 cores;
        out vec4 frag_colour;
        void main () {
            frag_colour = vec4(cores, 1.0);
        }
    """
    
    vs = OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER)
    fs = OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    
    Shader_programm_triangulo = OpenGL.GL.shaders.compileProgram(vs, fs)
    glDeleteShader(vs)
    glDeleteShader(fs)

def inicializaShaderQuadrado():
    global Shader_programm_quadrado
    
    # Shader diferente para demonstrar a diferença
    vertex_shader = """
        #version 400
        layout(location = 0) in vec3 vertex_posicao;
        layout(location = 1) in vec3 vertex_cores;
        out vec3 cores;
        void main () {
            cores = vertex_cores * 0.8; // Escurece um pouco as cores
            gl_Position = vec4(vertex_posicao, 1.0);
        }
    """
    
    fragment_shader = """
        #version 400
        in vec3 cores;
        out vec4 frag_colour;
        void main () {
            frag_colour = vec4(cores, 1.0);
        }
    """
    
    vs = OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER)
    fs = OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    
    Shader_programm_quadrado = OpenGL.GL.shaders.compileProgram(vs, fs)
    glDeleteShader(vs)
    glDeleteShader(fs)

def inicializaRenderizacao():
    global Window, Shader_programm_triangulo, Shader_programm_quadrado, Vao, WIDTH, HEIGHT

    # triangle is redrawn every frame inside while loop
    while not glfw.window_should_close(Window):
        # clear color buffers
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.2, 0.3, 0.3, 1.0) # background color

        # sets viewport
        glViewport(0, 0, WIDTH, HEIGHT)

        # activates shader program
        glUseProgram(Shader_programm_triangulo)

        # draws Triangle 1 (VAO 0)
        glBindVertexArray(Vao[0])
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        # draws Triangle 2 (VAO 1)
        glBindVertexArray(Vao[1])
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        # activates shader program
        glUseProgram(Shader_programm_quadrado)

        # draws Square 1 (VAO 2)
        glBindVertexArray(Vao[2])
        glDrawArrays(GL_TRIANGLES, 0, 6)

        # handle events and swap buffers
        glfw.poll_events()
        glfw.swap_buffers(Window) # renders screen 

        # closes if ESC is pressed
        if (glfw.PRESS == glfw.get_key(Window, glfw.KEY_ESCAPE)):
            glfw.set_window_should_close(Window, True)
    
    glfw.terminate()

# main function
def main():

    inicializaOpenGL() # set ups OpenGL
    inicializaObjetos() 
    # inicializaShaders() # programs shaders, specifying objects to be rendered
    inicializaShaderTriangulo()
    inicializaShaderQuadrado()
    inicializaRenderizacao() # renders the model objects

if __name__ == "__main__":
    main()