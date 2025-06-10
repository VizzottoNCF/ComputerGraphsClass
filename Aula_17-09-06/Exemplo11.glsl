#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;

void main() {
    // Normaliza as coordenadas do fragmento para o intervalo [0, 1]
    vec2 st= gl_FragCoord.xy/ u_resolution;

    // Inicializa pctcomo 0.0
    float pct= 0.0;

    // Calcula a distância do fragmento até o centro do espaço (0.5, 0.5)
    // A função distance() retorna a distância euclidiana entre dois pontos em um plano 2D.
    // No caso, ela retorna a distância entre o ponto ste o ponto (0.5, 0.5), que representa o centro do espaço.
    // A distância euclidiana é calculada usando a fórmula: sqrt((x2 -x1)^2 + (y2 -y1)^2)
    // Isso significa que a função distance() retorna a magnitude do vetor formado pelos componentes (x, y).
    // Calcula a distância do fragmento até o centro do espaço (0.5, 0.5)
    pct = distance(st, vec2(0.5));

    // Se a distância for maior que 0.5, pctrecebe 1.0, caso contrário, 0.0
    pct = step(0.5, pct);

    // Define a cor com base em pct
    vec3 color= vec3(pct);

    // Define a cor final do fragmento
    gl_FragColor= vec4(color, 1.0);
}