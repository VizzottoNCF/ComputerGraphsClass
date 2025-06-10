#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;

void main() {
    // Normaliza as coordenadas do fragmento para o intervalo [0, 1]
    vec2 st = gl_FragCoord.xy/ u_resolution.xy;
    
    // Inicializa a cor como preto
    vec3 color= vec3(0.0);

    // bottom-left
    vec2 bl= step(vec2(0.1), st); // Verifica se o ponto está no quadrante bottom-left

    // top-right
    vec2 tr= step(vec2(0.1), 1.0-st); // Verifica se o ponto está no quadrante top-right

    // Realiza a operação AND
    color = vec3(bl.x * bl.y * tr.x * tr.y);

    // Define a cor final do fragmento
    gl_FragColor= vec4(color, 1.0);
}