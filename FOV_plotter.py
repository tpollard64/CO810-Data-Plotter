import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate


#**********************************#
#           UPDATE THESE           #
# === CONFIGURABLE PARAMETERS  === #
#**********************************#
img_path = 'put_your_file_path_here'
yaw_deg = 0     # Horizontal rotation in degrees  (negative for right)
pitch_deg = 0  # Vertical rotation in degrees (negative for up)
roll_deg = 0     # Clockwise image rotation in degrees

img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
height, width, _ = img.shape

yaw_pixels = int((yaw_deg / 360.0) * width)
img = np.roll(img, shift=-yaw_pixels, axis=1)  

pitch_pixels = int((pitch_deg / 180.0) * height)
img = np.roll(img, shift=-pitch_pixels, axis=0) 

img = rotate(img, angle=roll_deg, reshape=False, mode='wrap')

azimuth_ticks = np.linspace(-180, 180, 37)
elevation_ticks = np.linspace(-90, 90, 19)

fig, ax = plt.subplots(figsize=(16, 9))

#**********************************#
#           UPDATE THESE           #
# ===    HEADER PARAMETERS  === #
#**********************************#

fig.text(0.5, 0.98, "MODEL: AW109S Helicopter", ha='center', fontsize=14, fontweight='bold', family="Times New Roman")
fig.text(0.5, 0.96, "BuNo: XXXXXX", ha='center', fontsize=12, family="Times New Roman")

# === Left Side (Aircraft Configuration) === #
aircraft_config = """Aircraft Configuration:
    Doors On, Windows Closed
    No external stores (clean)
    AP1/AP2: ON
    VARTOMS – NORM
Airspeed source: Instrumentation boom (calibrated)
Mech. Char. Measurement Source: USNTPS
Method: Trimmed Free Flight, Linear curve fits"""

fig.text(0.1, 0.85, aircraft_config, ha='left', fontsize=10, family="Times New Roman")

# === Right Side (Test Conditions) === #
test_conditions = """Rotor Speed: 97.9%
Test Day Conditions:
    Outside Air Temperature: -9 ºC
    Pressure Altitude: 2,600 ft
    Turbulence Rating: Occasional Light
Gross Weight: 6450 lbs
Center of Gravity: 173.6 in"""



# Dont touch these
fig.text(0.65, 0.86, test_conditions, ha='left', fontsize=10, family="Times New Roman")
fig.text(0.5, 0.83, "Reproduce in color", ha='center', fontsize=12, family="Times New Roman")
ax.imshow(img)
ax.set_xticks([(t + 180) / 360 * width for t in azimuth_ticks])
ax.set_xticklabels([f"{int(t)}°" for t in azimuth_ticks])
ax.set_yticks([(90 - t) / 180 * height for t in elevation_ticks])
ax.set_yticklabels([f"{int(t)}°" for t in elevation_ticks])


# Change grid color here
ax.grid(True, color='black', linestyle='-', linewidth=0.5)
ax.set_xlim(0, width)
ax.set_ylim(height, 0)


# Stop touching stuff
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout(rect=[0, 0, 1, 0.84])
plt.savefig("FOR_overlay_rotated.jpg", dpi=300)
plt.show()
