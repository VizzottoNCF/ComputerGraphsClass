#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;

void main() {
    // Normalizamos a posição do pixel em relação à resolução da tela,
    // para que ambas as coordenadas fiquem na mesma faixa de valores (entre 0 e 1).
    vec2 st = gl_FragCoord.xy / u_resolution;

    // Utilizamos a função step para determinar se a coordenada x normalizada (st.x) é maior que 0.5.
    // step(0.5, st.x) retorna 0 caso st.x seja menor que 0.5, e retorna 1 caso seja maior ou igual a 0.5.
    float res = step(0.5, st.x);

    // Define uma cor baseada no valor calculado pela função step.
    // Se a coordenada x normalizada for maior ou igual a 0.5, a cor será branca (1.0),
    // caso contrário, será preta (0.0).
    vec3 color = vec3(res);

    // Define a cor final do fragmento com base na cor calculada e define a transparência como 1.0 (completamente opaco).
    gl_FragColor = vec4(color, 1.0);
}