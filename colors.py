import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# --- Load CSV ---
df = pd.read_csv("colours.csv")  # Replace with your file path if needed

# Convert HEX to RGB
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

df[['r', 'g', 'b']] = df['hex'].apply(lambda x: pd.Series(hex_to_rgb(x)))

# Sidebar sliders
st.sidebar.header("Color Adjustments by Skin Tone")

st.sidebar.subheader("🍂 Autumn for Dark Skin (คล้ำ)")
st.sidebar.write("Make autumn colors brighter and more vibrant for people with dark skin")
autumn_brightness = st.sidebar.slider("Autumn Brightness", 0, 100, 30, help="Higher = brighter autumn colors")
autumn_saturation = st.sidebar.slider("Autumn Saturation", 0, 100, 60, help="Higher = more vibrant autumn colors")

st.sidebar.subheader("☀️ Summer for White Skin (ขาว)")
st.sidebar.write("Make summer colors deeper and richer for people with white skin") 
summer_darkness = st.sidebar.slider("Summer Darkness", 0, 80, 10, help="Higher = deeper summer colors")
summer_saturation = st.sidebar.slider("Summer Saturation", 0, 100, 70, help="Higher = more vibrant summer colors")

# Helper function to adjust brightness and saturation
def adjust_brightness_saturation(rgb, brightness_factor, saturation_factor):
    r, g, b = rgb
    
    # Convert to HSV-like adjustment
    # Brightness adjustment
    if brightness_factor > 0:
        # Make brighter by moving towards white
        r = r + (255 - r) * (brightness_factor / 100)
        g = g + (255 - g) * (brightness_factor / 100)
        b = b + (255 - b) * (brightness_factor / 100)
    
    # Saturation adjustment
    if saturation_factor > 0:
        # Increase saturation by enhancing color differences
        avg = (r + g + b) / 3
        r = avg + (r - avg) * (1 + saturation_factor / 100)
        g = avg + (g - avg) * (1 + saturation_factor / 100)
        b = avg + (b - avg) * (1 + saturation_factor / 100)
    
    return np.clip([r, g, b], 0, 255)

def adjust_darkness_saturation(rgb, darkness_factor, saturation_factor):
    r, g, b = rgb
    
    # Darkness adjustment
    if darkness_factor > 0:
        # Make darker by reducing RGB values
        r = r * (1 - darkness_factor / 100)
        g = g * (1 - darkness_factor / 100)
        b = b * (1 - darkness_factor / 100)
    
    # Saturation adjustment
    if saturation_factor > 0:
        # Increase saturation by enhancing color differences
        avg = (r + g + b) / 3
        r = avg + (r - avg) * (1 + saturation_factor / 100)
        g = avg + (g - avg) * (1 + saturation_factor / 100)
        b = avg + (b - avg) * (1 + saturation_factor / 100)
    
    return np.clip([r, g, b], 0, 255)

# Process autumn-dark (for people with dark skin - make colors brighter and more vibrant)
autumn_dark = df[df['season'] == 'autumn'].copy()
autumn_dark['season'] = 'autumn-dark'
# Apply brightness and saturation adjustments for dark skin
autumn_dark[['r', 'g', 'b']] = autumn_dark[['r', 'g', 'b']].apply(
    lambda x: pd.Series(adjust_brightness_saturation(x, autumn_brightness, autumn_saturation)), axis=1
)
autumn_dark['hex'] = autumn_dark[['r', 'g', 'b']].apply(
    lambda row: '#{:02x}{:02x}{:02x}'.format(int(row['r']), int(row['g']), int(row['b'])), axis=1
)

# Process summer-white (for people with white skin - make colors deeper and more vibrant)
summer_white = df[df['season'] == 'summer'].copy()
summer_white['season'] = 'summer-white'
# Apply darkness and saturation adjustments for white skin
summer_white[['r', 'g', 'b']] = summer_white[['r', 'g', 'b']].apply(
    lambda x: pd.Series(adjust_darkness_saturation(x, summer_darkness, summer_saturation)), axis=1
)
summer_white['hex'] = summer_white[['r', 'g', 'b']].apply(
    lambda row: '#{:02x}{:02x}{:02x}'.format(int(row['r']), int(row['g']), int(row['b'])), axis=1
)

# Append transformed data
df_full = pd.concat([df, autumn_dark, summer_white], ignore_index=True)

# Plotting
def plot_palette(season1, season2):
    colors1 = df_full[df_full['season'] == season1]['hex'].tolist()
    colors2 = df_full[df_full['season'] == season2]['hex'].tolist()

    def draw(ax, hex_list, title):
        max_per_row = 10
        n = len(hex_list)
        rows = (n - 1) // max_per_row + 1
        ax.set_xlim(0, max_per_row)
        ax.set_ylim(0, rows)
        ax.set_title(title)
        ax.axis("off")
        for i, hex_color in enumerate(hex_list):
            col = i % max_per_row
            row = rows - 1 - (i // max_per_row)
            rect = Rectangle((col, row), 1, 1, color=hex_color, edgecolor='black')
            ax.add_patch(rect)

    fig, axs = plt.subplots(2, 1, figsize=(10, 3))
    draw(axs[0], colors1, season1)
    draw(axs[1], colors2, season2)
    st.pyplot(fig)

st.subheader("Autumn vs Autumn-Dark")
plot_palette("autumn", "autumn-dark")

st.subheader("Summer vs Summer-White")
plot_palette("summer", "summer-white")