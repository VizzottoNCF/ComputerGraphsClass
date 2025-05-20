
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

Window = None
Shader_programm = None
Vao = None
WIDTH = 1000
HEIGHT = 800

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
    Window = glfw.create_window(WIDTH, HEIGHT, "Exemplo - renderização de um triângulo", None, None)

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

def inicializaObjetos():
    
    # VAO unifies and represents all buffers in a single identifier
    # each object must have one VAO
    global Vao
    
    # generates VAO and defines an identifier with glGenVertexArrays
    Vao = glGenVertexArrays(1) # returns array with every id
    # vao[0] - First Triangle
    # vao[1] - Second Triangle
    # vao[2] - 

    # only one VAO can be bound at a time
    # everything a VAO is supposed to do needs to be called before changing VAO
    glBindVertexArray(Vao)


    # defines triangle vertices VBO
    # - defines float positions of the vertices
    # - creates copy of this data in the GPU through VBO
    # create empty buffer with glGenBuffers() and 


	# Para isso, nós geramos primeiramente um buffer vazio, através da função glGenBuffers, e então setamos esse buffer como buffer 
	# atual na máquina de estados do OpenGL através de glBindBuffer,e por fim copiamos os pontos para esse buffer através do glBufferData.
    points = [
        # Triangle 1
        #X    Y    Z
		0.0, 0.5, 0.0, #cima
		0.5, -0.5, 0.0, #direita
		-0.5, -0.5, 0.0, #esquerda
        
        # Triangle 2
        #X    Y    Z
		0.6, -0.5, 0.0, #cima
		1.1, 0.5, 0.0, #direita
		0.1, 0.5, 0.0 #esquerda
	]

    # converts python array to NumPy array
    points = np.array(points, dtype=np.float32)


    # each VAO needs their own PVBO
    pvbo = glGenBuffers(1) 
    #Vertex Buffer Object (VBO):
    #Propósito: O VBO é usado para armazenar os dados dos vértices.
    #Funcionalidade: Ele armazena os dados do vértice, como posições, cores, normais, etc., em um buffer de memória na GPU.
    #Uso Típico: Carrega os dados do vértice para a GPU usando glBufferData ou glBufferSubData. 
    #O VBO é, então, associado ao VAO usando glBindBuffer para que o VAO saiba de onde obter os dados.

    glBindBuffer(GL_ARRAY_BUFFER, pvbo) #coloca o pvbo no topo da pilha/maquina de estados
    glBufferData(GL_ARRAY_BUFFER, points, GL_STATIC_DRAW) #copia os dados do python para dentro do VBO
    # Ativamos o primeiro atributo do VAO (índice 0), que é o atributo referente ao buffer das posições dos vértices.
    glEnableVertexAttribArray(0)
    # E então definimos o layout do buffer de vértices:
	# - o primeiro parâmetro (0) significa que estamos definido o layout do atributo 0 (buffer de vértices)
	# - o segundo parâmetro (3) significa que esse buffer é formado por 3 variáveis (x,y, e z),
	# - o terceiro parâmetro, indica que as variáveis são do tipo float
	# - o quarto parâmetro indica que nós desejamos normalizar os valores
    # - o quinto parâmetro é o byte offset entre os atributos, caso tenha sido especificado um único VBO para mais de um tipo de informação
    # - o sexto parâmetro é o offset do primeiro elemento, que no nosso caso, é 0, pois queremos todos os elementos do array
    #   -- Devido a um bug da biblioteca, precisamos passar None ao invés de 0
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)


    # Definição de um VBO para as cores do triângulo. Observe que passamos como parâmetro o valor 1
	# na chamada ao "glEnableVertexAttribArray", pois estamos ativando o segundo atributo deste VAO,
	# que são as cores dos vértices. Além disso, também passamos o parâmetro 1 na chamada ao "glVertexAttribPointer", 
	# pois estamos definindo o layout do segundo atributo.
    cores = [
        # Triangle 1
        #R    G    B
		1.0, 0.0, 0.0, #vermelho
		0.0, 1.0, 0.0, #verde
		0.0, 1.0, 1.0,  #azul
        
        # Triangle 2
        #X    Y    Z
		0.0, 0.0, 1.0, #cima
		0.0, 1.0, 0.0, #direita
		1.0, 1.0, 0.0 #esquerda
	]
    cores = np.array(cores, dtype=np.float32) #converte o array para numpy
    cvbo = glGenBuffers(1) #gera o vbo para as cores
    glBindBuffer(GL_ARRAY_BUFFER, cvbo) #da um bind no vbo das cores
    glBufferData(GL_ARRAY_BUFFER, cores, GL_STATIC_DRAW) #copia os dados para a memória de vídeo
    glEnableVertexAttribArray(1) #ativa o índice 1 para o vbo das cores
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None) #configura o vbo das cores


def inicializaShaders():
    global Shader_programm
    # Especificação do Vertex Shader:
    # - O Vertex Shader é responsável por processar cada vértice individualmente na GPU.
    # - A primeira linha especifica a versão da linguagem GLSL que estamos utilizando (4.0.0).
    # - `layout(location = 0) in vec3 vertex_posicao`:
    #     Essa variável de entrada (in) representa a posição de cada vértice,
    #     que é enviada pela CPU via VBO (vertex buffer object).
    # - `layout(location = 1) in vec3 vertex_cores`:
    #     Essa variável de entrada representa a cor associada a cada vértice.
    # - `out vec3 cores`:
    #     Esta é uma variável de saída do vertex shader. 
    #     Ela serve para **passar a cor do vértice para o fragment shader**.
    #     O OpenGL irá automaticamente interpolar esse valor entre os vértices ao longo da superfície.
    # - Dentro da função `main()`, atribuímos a posição final do vértice à variável especial `gl_Position`,
    #   que é obrigatória e define onde o vértice aparecerá na tela.
    #   `gl_Position` deve ser um `vec4`, então adicionamos 1.0 como o componente `w` (homogêneo).
    vertex_shader = """
        #version 400
        layout(location = 0) in vec3 vertex_posicao; //Vem do Python (IN), do VBO 0 (POSIÇÕES)
        layout(location = 1) in vec3 vertex_cores; //Vem do Python (IN), do VBO 1 (CORES)
        out vec3 cores;
        void main () {
            cores = vertex_cores;
            gl_Position = vec4 (vertex_posicao.x, vertex_posicao.y, vertex_posicao.z, 1.0);
        }
    """
    # Como os shaders são um programa "a parte", precisamos compilá-lo e verificar se não houve nenhum erro de compilação
    vs = OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER)
    if not glGetShaderiv(vs, GL_COMPILE_STATUS):
        infoLog = glGetShaderInfoLog(vs, 512, None)
        print("Erro no vertex shader:\n", infoLog)

    # Especificação do Fragment Shader:
# - O Fragment Shader é executado para cada fragmento (pixel potencial) gerado durante a rasterização do objeto.
    # - A primeira linha especifica a versão da linguagem GLSL utilizada (4.0.0).
    # - `in vec3 cores`:
    #     Essa variável de entrada recebe a **cor interpolada** dos vértices, vinda do vertex shader através da variável `out vec3 cores`.
    #     O OpenGL automaticamente interpola os valores das cores ao longo dos fragmentos da superfície do triângulo.
    # - `out vec4 frag_colour`:
    #     Essa é a variável de saída do fragment shader. Ela define a **cor final** do pixel que será desenhado na tela.
    #     Deve ser do tipo `vec4`, representando (R, G, B, A) — sendo `A` o canal de opacidade (alpha).
    # - Dentro da função `main()`, atribuimos à `frag_colour` o valor da cor recebida, adicionando o valor de alpha como 1.0 (totalmente opaco).	
    fragment_shader = """
        #version 400
        in vec3 cores;
		out vec4 frag_colour;
		void main () {
		    frag_colour = vec4 (cores.r, cores.g, cores.b, 1.0);
		}
    """
    # Do mesmo modo que o vertex shader, precisamos compilar o fragment shader e verificar se não houve nenhum erro de compilação
    fs = OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    if not glGetShaderiv(fs, GL_COMPILE_STATUS):
        infoLog = glGetShaderInfoLog(fs, 512, None)
        print("Erro no fragment shader:\n", infoLog)

    # Especificação do Shader Programm:
	# Após compilarmos os shaders, precisamos combiná-los em um único programa, denominado GPU Shader Program.
	# Para isso, chamamos a função compileProgram passando os dois shaders que irão formar o nosso shader program
    # e testamos se não houve nenhum erro de linkagem
    Shader_programm = OpenGL.GL.shaders.compileProgram(vs, fs)
    if not glGetProgramiv(Shader_programm, GL_LINK_STATUS):
        infoLog = glGetProgramInfoLog(Shader_programm, 512, None)
        print("Erro na linkagem do shader:\n", infoLog)

    glDeleteShader(vs) #depois de copiados para GPU com shader podemos liberar a memoria com 'vs e 'fs'
    glDeleteShader(fs)

def inicializaRenderizacao():
    global Window, Shader_programm, Vao, WIDTH, HEIGHT

    # triangle is redrawn every frame inside while loop
    while not glfw.window_should_close(Window):
        # clear color buffers
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.2, 0.3, 0.3, 1.0) # background color

        # redefines viewport size for window size, so that triangle scales with window
        glViewport(0, 0, WIDTH, HEIGHT)

        # Especificamos qual Shader Programm vamos utilizar
        glUseProgram(Shader_programm)
        # Setamos o objeto Vao como sendo o VAO atual na máquina de estados do OpenGL
        glBindVertexArray(Vao)
        
        # Desenhamos o triângulo especificado no vao
        glDrawArrays(GL_TRIANGLES, 0, 6) #a partir do primeiro vértice, desenha 3 vértices

        # Atualizamos outros eventos, tais como entradas pelo teclado, mouse, etc, caso ocorram
        glfw.poll_events()

        # Renderizamos na tela tudo aquilo que foi desenhado logo acima
        glfw.swap_buffers(Window)

        # Verificamos se a tecla ESC foi pressionada. Caso positivo, definimos que a tela deve ser
		# fechada na próxima volta do laço.
		# Para testar se outras teclas foram pressionadas, verifique o seguinte link:
		# http://www.glfw.org/docs/latest/group__input.html
        if (glfw.PRESS == glfw.get_key(Window, glfw.KEY_ESCAPE)):
            glfw.set_window_should_close(Window, True)
    
    glfw.terminate()

# main function
def main():
    inicializaOpenGL() # set ups OpenGL
    inicializaObjetos() # models the objects and sends them to the gpu
    inicializaShaders() # programs shaders, specifying objects to be rendered
    inicializaRenderizacao() # renders the model objects

if __name__ == "__main__":
    main()