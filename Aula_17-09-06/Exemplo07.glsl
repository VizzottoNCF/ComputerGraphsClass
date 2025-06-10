#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;

float plota() {
    // A função smoothstep cria uma transição suave entre dois valores,
    // retornando 0 para valores menores que 0.2, 1 para valores maiores que 0.8,
    // e uma interpolação linear entre 0.2 e 0.8.
    return smoothstep(0.2, 0.9, st.x);
}
void main() {
// Normalizamos a posição do pixel em relação à resolução da tela,
// para que ambas as coordenadas fiquem na mesma faixa de valores (entre 0 e 1).
vec2 st=gl_FragCoord.xy/u_resolution;

// Calcula a porcentagem de visibilidade (pct) da linha utilizando a função plota.
float pct = plota(st);

// Define a cor do fragmento como uma interpolação entre verde (0,1,0) e preto (0,0,0)
// com base na porcentagem de visibilidade da linha calculada anteriormente.
vec3 color = pct * vec3(0.0, 1.0, 0.0);

// Define a cor final do fragmento com base na cor calculada e define a transparência como 1.0 (completamente opaco).
gl_FragColor = vec4(color, 1.0);
}