import numpy as np
import matplotlib.colors as mcolors
import pandas as pd

# Plot graph
def plot_graph(ax, coefficients, lower_bounds, upper_bounds, p_values=None, variable_names=None,
               standardize=False, xlabel='Coefficients',
               title='Regression Analysis',
               show_yticks=True,  # Control yticks label
               negative_bar_colour='#c4c4fc', positive_bar_colour='#fcb4b4', input_X=None):

    # If standardize=True
    if standardize and input_X is not None:
        std_X = np.std(input_X)
        coefficients = coefficients * std_X
        lower_bounds = lower_bounds * std_X
        upper_bounds = upper_bounds * std_X

    for i, (low, high, p_value) in enumerate(zip(lower_bounds, upper_bounds, p_values)):
        saturation = np.clip(1 - np.array(p_values), 0, 1) if p_values is not None else 0.5
        transparency = saturation[i].item() if p_values is not None else 0.5
        color = mcolors.to_rgba(positive_bar_colour if coefficients[i] < 0 else negative_bar_colour, alpha=transparency)
        bar_style = ax.barh(i, high - low, left=low, color=color, edgecolor='black', linewidth=1.2)
        coordinates = (low + high) / 2
        ax.plot([coordinates, coordinates], [bar_style[0].get_y(), bar_style[0].get_y() + bar_style[0].get_height()], color='black', linewidth=1)

    for idx in range(len(coefficients)):
        ax.axhline(idx, color='lightgrey', linestyle='--', alpha=0.6, zorder=0)

    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)

    # If show_yticks is true argument
    if show_yticks:
        ax.set_yticks(range(len(variable_names)))
        ax.set_yticklabels(variable_names)
    else:
        ax.set_yticks([])
        ax.set_yticklabels([])

    ax.set_xlabel(xlabel)
    ax.set_title(title)

# Create table
def create_table(ax, data, dependent_variable='y', loc='right', cell_loc='left', font_size=10, bbox=[0, 0, 1, 1], col_widths=None,
                 label_cell_loc='center', label_bbox=[0, 0, 1, 1]):

    numeric_data = data.select_dtypes(include=[np.number])
    
    # Check if dependent variable is present in the data
    if dependent_variable in data.columns:
        # Exclude the dependent variable from the table
        numeric_data = numeric_data.drop(columns=[dependent_variable])

    mean = np.mean(numeric_data, axis=0)
    std = np.std(numeric_data, axis=0)

    # Table information 
    table_info = list(zip(numeric_data.columns, np.round(mean, 2), np.round(std, 2)))

    # Reverse the order of rows
    table_info = list(reversed(table_info))

    # Use customizable options with defaults
    if table_info:
        # Set default values if parameters are not provided
        col_widths = col_widths or [0.2] * (len(numeric_data.columns) + 1)
        loc = loc or 'right'
        bbox = bbox or [0, 0, 1, 1]

        # Original table
        table = ax.table(cellText=table_info, loc=loc, cellLoc=cell_loc, colWidths=col_widths, bbox=bbox)
        table.auto_set_font_size(False)
        table.set_fontsize(font_size)
        ax.axis('off')

        # Add labels directly above the table
        bbox_x, bbox_y, bbox_width, bbox_height = bbox
        label_y = bbox_y + bbox_height + 0.02  # Adjust this value to fine-tune the vertical position

        # Additional labels table without borders
        labels_table_info = [('Variable', 'Mean', 'STD')]
        labels_table = ax.table(cellText=labels_table_info, loc='center', cellLoc=label_cell_loc, colWidths=col_widths, bbox=label_bbox)
        labels_table.auto_set_font_size(False)
        labels_table.set_fontsize(10)
        ax.axis('off')

        # Remove borders from the table cells
        for cell in labels_table._cells:
            labels_table._cells[cell].set_edgecolor('none')

            
# Getting values from regression result
def extract_data(model_result=None, coefficients=None, lower_bounds=None, upper_bounds=None,
                            p_values=None, variable_names=None, input_data=None, input_X=None,
                            standardize=False, figsize=(12, 8), xlabel='Coefficients',
                            title='Coefficients with Confidence Intervals',
                            positive_bar_colour='#c4c4fc', negative_bar_colour='#fcb4b4',
                            table_kwargs=None, **kwargs):
    
    if model_result is not None:
        # statsmodels implementation
        if hasattr(model_result, 'params') and hasattr(model_result, 'conf_int'):
            coefficients = model_result.params
            conf_int = model_result.conf_int()
            try:
                lower_bounds, upper_bounds = conf_int.iloc[:, :2].values.T
            except AttributeError:
                conf_int_df = pd.DataFrame(conf_int, columns=['lower', 'upper'])
                lower_bounds, upper_bounds = conf_int_df.iloc[:, :2].values.T
            p_values = model_result.pvalues
        else:
            raise ValueError("Unsupported model result, please use statsmodels")

        return coefficients, lower_bounds, upper_bounds, p_values

    else:
        raise ValueError("Model result is required.")

# Calls function on input value
def regression_plot(ax, model_result=None, coefficients=None, lower_bounds=None, upper_bounds=None,
                                     p_values=None, variable_names=None, input_data=None, input_X=None,
                                     standardize=False, xlabel='Coefficients',
                                     title='Regression Analysis',
                                     positive_bar_colour='#c4c4fc', negative_bar_colour='#fcb4b4',
                                     table_kwargs=None, ax_table=None, **kwargs):
    # If standardize=True
    if standardize and input_X is None:
        raise ValueError("If standardized=True, an independent variable (x) must be provided.")

    # Regression model called   
    if model_result is not None:
        # If a model_result is provided, call extract_data
        coefficients, lower_bounds, upper_bounds, p_values = \
            extract_data(model_result, variable_names=variable_names, input_data=input_data,
                                    input_X=input_X, standardize=standardize)

    # Pass the extracted data to plot_graph function
    plot_graph(ax, coefficients, lower_bounds, upper_bounds, p_values, variable_names=variable_names,
               standardize=standardize, xlabel=xlabel, title=title,
               positive_bar_colour=positive_bar_colour, negative_bar_colour=negative_bar_colour, input_X=input_X, **kwargs)

    # Use the provided ax_table only if it is provided
    if ax_table is not None:
        create_table(ax_table, input_data, **table_kwargs)
