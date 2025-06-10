#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;

// Função para calcular a intensidade de um círculo
float circle(in vec2 _st, in float _radius) {
    // Calcula o vetor de distância do ponto para o centro do círculo
    vec2 l= _st-vec2(0.5);
    
    // Calcula a distância do ponto para o centro do círculo e suaviza a transição
    return 1.0-smoothstep(_radius-(_radius* 0.01),
                          _radius+ (_radius* 0.01), 
                           dot(l, l) * 4.0);
}

void main() {
    // Normaliza as coordenadas do fragmento para o intervalo [0, 1]
    vec2 st= gl_FragCoord.xy/ u_resolution;

    // Inicializa a cor como preto
    vec3 color= vec3(0.0);

    // Aplicamos uma escala de 3x no espaço
    st*= 3.0;

    // Pegamos a parte fracionária das coordenadas
    st= fract(st);

    // Calcula a intensidade do círculo centrado em (0.5, 0.5) com raio 0.5
    color= vec3(circle(st, 0.5));

    // Define a cor final do fragmento
    gl_FragColor= vec4(color, 1.0);
}