import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define Vertices of the Cube
P1 = (-0.5, -0.5, -0.5)
P2 = (-0.5, -0.5, 0.5)
P3 = (-0.5, 0.5, -0.5)
P4 = (-0.5, 0.5, 0.5)
P5 = (0.5, -0.5, -0.5)
P6 = (0.5, -0.5, 0.5)
P7 = (0.5, 0.5, -0.5)
P8 = (0.5, 0.5, 0.5)

# Define edges
arestas = [(P1, P2), (P2, P4), (P4, P3), (P3, P1), (P5, P6), (P6, P8), (P8, P7), (P7, P5), (P1, P5), (P2, P6), (P3, P7), (P4, P8)]

# Plot the cube
fig = plt.figure()
ax = fig.add_subplot(projection='3d') #add an aditional subplot for 3 dimensional figure

# plot cube edges
for aresta in arestas:
    # obtain coords of 1st and 2nd vertice that form the edge (x,y,z)
    ponto1 = aresta[0]
    ponto2 = aresta[1]

    # plot line between points
    ax.plot([ponto1[0], ponto2[0]], [ponto1[1], ponto2[1]], [ponto1[2], ponto2[2]], 'b') # 3d coords

# configs
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Cube in 3D')

# axes limits
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-0.5, 0.5)
ax.set_zlim(-0.5, 0.5)
# Adicionando manualmente uma legenda para o eixo Z
ax.text(0.7, 0.5, 0.6, 'Z', color='black') # Adicionando o texto 'Z' na posição desejada


# show graph
plt.show()
