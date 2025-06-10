#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;
#define PI 3.14159265358979323846

// Função para gerar números pseudoaleatórios com base em uma posição
float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233)) + u_time) * 43758.5453123);
}

void main() {
    // Normaliza as coordenadas do fragmento para o intervalo [0, 1]
    vec2 st = gl_FragCoord.xy / u_resolution.xy;

    // Calcula um valor aleatório com base nas coordenadas do fragmento e no tempo
    float rnd = random(st) * u_time

    // Define a cor final do fragmento usando o valor aleatório multiplicado pelo tempo
    gl_FragColor= vec4(vec3(rnd), 1.0);
}