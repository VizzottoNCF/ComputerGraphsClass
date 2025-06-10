#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;

void main() {
    // Normaliza as coordenadas do fragmento para o intervalo [0, 1]
    vec2 st = gl_FragCoord.xy/ u_resolution;

    // Inicializa a cor como preto
    vec3 color = vec3(0.0);

    // Aplicamos uma escala de 3x no espaço
    st *= 3.0;
    
    // Pegamos a parte fracionária das coordenadas
    st = fract(st);

    // Agora temos 9 espaços que vão de 0 a 1, então podemos usar as coordenadas diretamente como cores
    color= vec3(st, 0.0);

    // Define a cor final do fragmento
    gl_FragColor= vec4(color, 1.0);
}