#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;
#define PI 3.14159265358979323846

// Função para rotacionar um ponto 2D em torno da origem
vec2 rotate2D(vec2 st, float angle) {
    // Translada o ponto para a origem
    st-= 0.5;

    // Aplica a rotação usando uma matriz de rotação
    st= mat2(cos(angle), -sin(angle),
    sin(angle), cos(angle)) * st;

    // Translada o ponto de volta
    st+= 0.5;
    return st;
}

// Função para desenhar um quadrado com bordas suaves
float drawSquare(vec2 st, vec2 size, float smoothEdges) {
    // Calcula o tamanho do quadrado
    vec2 halfSize= vec2(0.5) -size* 0.5;

    // Calcula as bordas suaves
    vec2 edgeSmoothness= vec2(smoothEdges* 0.5);

    // Aplica a suavização nas bordas
    vec2 uv= smoothstep(halfSize, halfSize+ edgeSmoothness, st);
    uv *= smoothstep(halfSize, halfSize+ edgeSmoothness, vec2(1.0) -st);

    return uv.x* uv.y;
}

// Função para repetir o espaço com um fator de zoom
vec2 tileSpace(vec2 st, float zoomFactor) {
    st *= zoomFactor;
    return fract(st);
}


void main() {
    // Normaliza as coordenadas do fragmento para o intervalo [0, 1]
    vec2 fragCoordNorm = gl_FragCoord.xy / u_resolution.xy;

    // Inicializa a cor como preto
    vec3 color = vec3(0.0);

    // Divide o espaço em 4 quadrantes
    vec2 tiledCoords = tileSpace(fragCoordNorm, 4.0);

    // Rotaciona os quadrantes em 45 graus
    vec2 rotatedCoords = rotate2D(tiledCoords, PI * 0.25);

    // Desenha um quadrado com bordas suaves
    color = vec3(drawSquare(rotatedCoords, vec2(0.7), 0.01));

    // Define a cor final do fragmento
    gl_FragColor= vec4(color, 1.0);
}