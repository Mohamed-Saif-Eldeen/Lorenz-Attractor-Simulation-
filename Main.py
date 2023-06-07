import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

def lorenz(xyz, *, s=10, r=28, b=2.667):
    x, y, z = xyz
    x_dot = s * (y - x)
    y_dot = r * x - y - x * z
    z_dot = x * y - b * z
    return np.array([x_dot, y_dot, z_dot])

dt = 0.01
num_steps = 10000

xyzs = np.empty((num_steps + 1, 3))
xyzs[0] = (0., 1., 1.05)

fig = plt.figure(figsize=(10, 5))
ax_system = fig.add_subplot(122, projection='3d')
ax_sliders = fig.add_subplot(121)

line, = ax_system.plot([], [], [], lw=0.5)

def init():
    ax_system.set_xlim(-30, 30)
    ax_system.set_ylim(-30, 30)
    ax_system.set_zlim(0, 50)
    ax_system.set_xlabel("X Axis")
    ax_system.set_ylabel("Y Axis")
    ax_system.set_zlabel("Z Axis")
    ax_system.set_title("")
    return line,

def update(i):
    xyzs[i + 1] = xyzs[i] + lorenz(xyzs[i], s=s_val, r=r_val, b=b_val) * dt
    line.set_data(xyzs[:i, 0], xyzs[:i, 1])
    line.set_3d_properties(xyzs[:i, 2])
    line.set_color(plt.cm.viridis(i / num_steps))  # Update color based on time
    return line,

ani_speed = 1.0  # Initial speed of the animation
s_val = 10  # Initial value for parameter s
r_val = 28  # Initial value for parameter r
b_val = 2.667  # Initial value for parameter b

def update_speed(val):
    global ani_speed
    ani_speed = val

def update_parameters(val):
    global s_val, r_val, b_val
    s_val = slider_s.val
    r_val = slider_r.val
    b_val = slider_b.val

ani = FuncAnimation(fig, update, frames=num_steps, init_func=init, blit=True)

# Create a slider axes for speed
slider_ax_speed = fig.add_axes([0.1, 0.15, 0.3, 0.03])
# Add a slider widget for speed
slider_speed = Slider(slider_ax_speed, 'Speed', 0.1, 5.0, valinit=ani_speed, valfmt='%1.1f')
# Set the update function for the speed slider
slider_speed.on_changed(update_speed)

# Create slider axes for parameters
slider_ax_s = fig.add_axes([0.1, 0.25, 0.3, 0.03])
slider_ax_r = fig.add_axes([0.1, 0.35, 0.3, 0.03])
slider_ax_b = fig.add_axes([0.1, 0.45, 0.3, 0.03])

# Add slider widgets for parameters
slider_s = Slider(slider_ax_s, 'Sigma', 0, 30, valinit=s_val, valfmt='%1.1f')
slider_r = Slider(slider_ax_r, 'Rho', 0, 50, valinit=r_val, valfmt='%1.1f')
slider_b = Slider(slider_ax_b, 'Beta', 0, 10, valinit=b_val, valfmt='%1.1f')

# Set the update function for the parameter sliders
slider_s.on_changed(update_parameters)
slider_r.on_changed(update_parameters)
slider_b.on_changed(update_parameters)

plt.tight_layout()
plt.show()
