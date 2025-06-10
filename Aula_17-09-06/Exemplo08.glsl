#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;

float plota(vec2 st, float pct) {
    // A função smoothstep cria uma transição suave entre dois valores.
    // Aqui, v1 faz a transição de 0 para 1 quando st.yestá próximo de pct-0.02.
    float v1 = smoothstep(pct - 0.02, pct, st.y);
    // E v2 faz a transição de 0 para 1 quando st.yestá próximo de pct+0.02.
    float v2 = smoothstep(pct, pct + 0.02, st.y);
    // Subtraindo v2 de v1, obtemos um valor que é 1 apenas quando st.yestá próximo de pct.
    return v1 - v2;
}


void main() {
    // Normalizamos a posição do pixel em relação à resolução da tela,
    // para que ambas as coordenadas fiquem na mesma faixa de valores (entre 0 e 1).
    vec2 st = gl_FragCoord.xy / u_resolution;
    // Desenha uma linha ao longo do eixo x.
    // A variável 'valor' será 1 apenas quando st.yestiver próximo de st.x.
    float valor = plota(st, st.x);
    // Define a cor do fragmento como verde (0,1,0) quando 'valor' é 1,
    // e preto (0,0,0) quando 'valor' é 0.
    vec3 color = valor * vec3(0.0, 1.0, 0.0);
    // Define a cor final do fragmento com base na cor calculada e define a transparência como 1.0 (completamente opaco).
    gl_FragColor= vec4(color, 1.0);
}