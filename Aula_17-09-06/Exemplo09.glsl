#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;

// Função para plotar uma linha suave entre duas posições especificadas.
float plota(vec2 st, float pct) {
// A função smoothstepcria uma transição suave entre dois valores.
// v1 faz a transição de 0 para 1 quando st.yestá próximo de pct-0.02.
float v1= smoothstep(pct-0.02, pct, st.y);
// v2 faz a transição de 1 para 0 quando st.yestá próximo de pct+0.02.
float v2= smoothstep(pct, pct+ 0.02, st.y);
// Retorna o valor que será 1 no centro da linha e 0 fora dela.
return v1-v2;
}

void main() {
    // Normalizamos a posição do pixel em relação à resolução da tela,
    // para que ambas as coordenadas fiquem na mesma faixa de valores (entre 0 e 1).
    vec2 st = (gl_FragCoord.xy/ u_resolution);

    // Define y como uma função da coordenada x elevada à quinta potência (y = x^5).
    // float y= pow(st.x, 2.0);
    float y = sin(10.0 * st.x);

    // Calcula o valor da linha suave em stutilizando a função plota.
    float valor= plota(st, y);

    // Define a cor da linha como verde (0.0, 1.0, 0.0).
    vec3 color= valor* vec3(0.0, 1.0, 0.0);

    // Define a cor final do fragmento com base na cor calculada e define a transparência como 1.0 (completamente opaco).
    gl_FragColor= vec4(color, 1.0);
}