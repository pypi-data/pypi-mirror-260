import ipywidgets as widgets

# Function to apply theme and cell width
def apply_changes(theme, cell):
    !jt -t {theme.lower()} -cellw {int(cell)}% -N -T -kl
    print("Themes have been changed. Please refresh this page (press F5).")
        
# Dropdown widget for selecting themes
theme = widgets.Dropdown(
    options=['chesterish', 'grade3', 'gruvboxl', 'monokai', 'oceans16', 'onedork', 'solarizedd', 'solarizedl'],
    value='grade3',
    description='Theme:'
)

# Slider widget for setting cell width
cell = widgets.IntSlider(
    value=100,
    min=60,
    max=120,
    step=10,
    description='Cell Width:'
)

# Button to apply changes
apply_bt = widgets.Button(description="Apply Changes")

# Event handler for button click
def on_apply_bt_click(b):
    apply_changes(theme.value, cell.value)
    
apply_bt.on_click(on_apply_bt_click)

# Display widgets horizontally
display(widgets.HBox([theme, cell, apply_bt]))
