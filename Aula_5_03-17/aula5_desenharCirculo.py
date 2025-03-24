import math
import matplotlib.pyplot as plt
# Defina o raio do círculo
raio = 4
# Inicialize a coordenada x
x = 0.0
# Lista para armazenar os pontos
pontos = []
# Calcule o limite para a varredura no eixo x
limite = raio * math.cos(math.radians(45))
# Loop enquanto x for menor que o limite  
while x <= limite:
    # Calcule a coordenada y correspondente usando a equação do círculo
    y = round(math.sqrt(raio * raio - x * x), 2)
    # Adicione os pontos à lista considerando a simetria do círculo
    pontos.extend([(round(x, 2), y), (y, round(x, 2)), (y, -round(x, 2)), (round(x, 2), -y),(-round(x, 2), -y), (-y, -round(x, 2)), (-y, round(x, 2)), (-round(x, 2), y)])
    # Incremente x para avançar na varredura
    x += 0.1


# Separe as coordenadas x e y para plotagem
coordenadas_x, coordenadas_y = zip(*pontos)

# Plote os pontos
plt.figure(figsize=(6,6))
plt.plot(coordenadas_x, coordenadas_y, 'bo', markersize=2) # Pontos menores para melhor visualização

# Ajuste os limites dos eixos para -7 a 7
plt.xlim(-7, 7)
plt.ylim(-7, 7)

# Adicione grade e rótulos
plt.grid(True)
plt.title("Círculo Rasterizado com Decimais")
plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")

# Mostre o gráfico
plt.show()