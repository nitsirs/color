# Color Palette Adjuster by Skin Tone

A Streamlit application that adjusts seasonal color palettes based on skin tone for better color matching.

## Features

- **Autumn for Dark Skin (คล้ำ)**: Makes autumn colors brighter and more vibrant
- **Summer for White Skin (ขาว)**: Makes summer colors deeper and richer
- Interactive sliders to adjust brightness and saturation
- Visual comparison of original vs adjusted color palettes

## How to Use

1. Use the sidebar sliders to adjust:
   - **Autumn Brightness**: Make autumn colors brighter for people with dark skin
   - **Autumn Saturation**: Enhance autumn color vibrancy
   - **Summer Darkness**: Make summer colors deeper for people with white skin  
   - **Summer Saturation**: Enhance summer color richness

2. View the visual comparisons:
   - Autumn vs Autumn-Dark
   - Summer vs Summer-White

## Requirements

- streamlit
- pandas
- numpy
- matplotlib

## Data

The app requires a `colours.csv` file with columns:
- `season`: Season type (autumn, summer, etc.)
- `hex`: Hex color codes
