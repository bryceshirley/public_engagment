import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define a more highly non-convex function representing the surface
def non_convex_function(x, y):
    return np.sin(x) * np.cos(y) + np.cos(2 * x) * np.sin(2 * y) + 0.5 * np.sin(3 * x) * np.cos(3 * y)

# Generate hexagonal grid for surface
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
X[::2] += (x[1] - x[0]) / 2  # Offset every other row for hexagonal pattern
Z = non_convex_function(X, Y)

# Create the vertices for the surface mesh (X, Y, Z)
vertices = np.array([X.flatten(), Y.flatten(), Z.flatten()]).T

# Generate the faces (triangles) for the hexagonal grid
faces = []
for i in range(len(x) - 1):
    for j in range(len(y) - 1):
        if i % 2 == 0:  # Even rows
            if j < len(y) - 1:
                faces.append([i * len(y) + j, (i + 1) * len(y) + j, i * len(y) + j + 1])
            if j > 0:
                faces.append([(i + 1) * len(y) + j, (i + 1) * len(y) + j - 1, i * len(y) + j])
        else:  # Odd rows
            if j < len(y) - 1:
                faces.append([i * len(y) + j, (i + 1) * len(y) + j, (i + 1) * len(y) + j + 1])
            if j > 0:
                faces.append([i * len(y) + j, (i + 1) * len(y) + j - 1, i * len(y) + j - 1])

# Convert faces to a numpy array
faces = np.array(faces)

# Create the mesh using numpy-stl
surface_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

for i, f in enumerate(faces):
    for j in range(3):
        surface_mesh.vectors[i][j] = vertices[f[j]]

# Save the mesh as an STL file
surface_mesh.save('non_convex_surface.stl')

# Plotting the surface (for visualization)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Rolling Ball on Non-Convex Surface')

# Show plot
plt.show()
