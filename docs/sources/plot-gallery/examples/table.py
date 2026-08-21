"""
Table Plots
===========
"""

# %%
# Table plots are simply plots of descriptive tables, with optional formatting, and can be generated using the :py:func:`~isaricanalytics.visualisation.fig_table` function, which returns a :py:class:`Plotly Go Figure <plotly.graph_objs._figure.Figure>` object.
#
# The plot below was generated using a synthetic dataset of selected patient treatment complications for Dengue.
#
# The dataset is given below as a table (but can also be loaded from the static :file:`examples/csv/table.csv` file).
#
# .. list-table:: Dengue patient treatment complications (selection)
#    :header-rows: 1
#    :widths: auto
#
#    * - Complication / Outcome Variable
#      - Patient Count
#      - Discharged
#      - Death
#      - Censored
#    * - All / Any
#      - 1000
#      - 219
#      - 326
#      - 455
#    * - Seizure
#      - 665 (81.7%, N=814)
#      - 148 (80.9%, N=183)
#      - 207 (79.6%, N=260)
#      - 310 (83.6%, N=371)
#    * - Focal neurological signs
#      - 702 (74.8%, N=938)
#      - 156 (75.4%, N=207)
#      - 231 (75.5%, N=306)
#      - 315 (74.1%, N=425)
#    * - Encephalitis
#      - 481 (52.6%, N=914)
#      - 102 (52.0%, N=196)
#      - 161 (53.5%, N=301)
#      - 218 (52.3%, N=417)
#    * - Meningitis
#      - 781 (90.2%, N=866)
#      - 173 (88.7%, N=195)
#      - 252 (91.0%, N=277)
#      - 356 (90.4%, N=394)
#    * - Cardiac arrhythmia
#      - 241 (26.7%, N=901)
#      - 64 (32.0%, N=200)
#      - 70 (24.1%, N=291)
#      - 107 (26.1%, N=410)
#
# The :py:func:`~isaricanalytics.visualisation.fig_table` function does not expect a dataframe in any particular format, except that it should correspond to the kind of table shown in the example above. If the cell values require **formatting** then formatting should be applied either to the dataframe or the source file from which it was loaded. Here are the Python steps you need to generate the plot using the :py:func:`~isaricanalytics.visualisation.fig_table` function:
import pandas as pd
from isaricanalytics.visualisation import fig_table

# Load the CSV data from a string buffer
data = pd.read_csv("./csv/table.csv")

# Create and display the figure
fig = fig_table(
   data,
   table_key="Descriptive Table of Synthetic Dengue Patient Complications",
)
fig.update_layout(autosize=True)
fig

# %%
#
# .. note::
#
#    In the example above, most cell values contain formatting to make the
#    rendered table more readable. These can be omitted if formatting is not
#    required.
#
# .. note::
#
#    Any dataframe or CSV column names, or dictionary field labels, in the
#    example above that are not specific to the dataset must be as given,
#    otherwise the function may throw an exception or return an incorrect figure.
#
#    The figure height and width parameters can be set using the ``height``
#    and ``width`` parameters, but it may be more convenient to let Plotly handle
#    this using the figure layout `autosize <https://plotly.com/python/reference/layout/#layout-autosize>`_
#    parameter. Refer to the :py:func:`~isaricanalytics.visualisation.fig_table`
#    function docstring for more information.
