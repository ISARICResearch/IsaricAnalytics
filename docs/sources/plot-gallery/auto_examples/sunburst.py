"""
Sunburst Plots
==============
Sunburst Plot of Synthetic Patient Enrolment Data Organised by Site and Country
"""

# %%
# Sunburst plots, also known as `ring charts <https://en.wikipedia.org/wiki/Pie_chart#Ring_chart,_sunburst_chart,_and_multilevel_pie_chart>`_, can be generated using the :py:func:`~isaricanalytics.visualisation.fig_sunburst` function, which returns a :py:class:`Plotly Go Figure <plotly.graph_objs._figure.Figure>` object.
# 
#
# The synthetic dataset used for this plot is given as a table (which can easily be converted to a CSV).
#
# .. list-table:: Synthetic dataset for patient enrolment at clinical sites filtered by country
#   :header-rows: 1
#   :widths: auto
#
#   * - Site
#     - Country
#     - Subject Id
#   * - 0
#     - COL
#     - 21
#   * - 2
#     - COL
#     - 25
#   * - 3
#     - GBR
#     - 199
#   * - 5
#     - CAN
#     - 31
#   * - 6
#     - BRA
#     - 156
#   * - 7
#     - BRA
#     - 27
#   * - 8
#     - BRA
#     - 8
#   * - 9
#     - FRA
#     - 174
#   * - 10
#     - POL
#     - 89
#   * - 11
#     - POL
#     - 30
#   * - 13
#     - RWA
#     - 121
#   * - 14
#     - KEN
#     - 1
#   * - 15
#     - KEN
#     - 15
#   * - 16
#     - KEN
#     - 1
#   * - 18
#     - NLD
#     - 102
#
# The data source can be in any appropriate form, such as, typically, a CSV. Here are the Python steps you need to generate the plot above using the :py:func:`~isaricanalytics.visualisation.fig_sunburst` function:


import io, pandas as pd
from isaricanalytics.visualisation import fig_sunburst

# Load the CSV data from a string buffer
data = pd.read_csv(io.StringIO(
   """Site,Country,SubjectID\n
      0,COL,21\n2,COL,25\n
      3,GBR,199\n
      5,CAN,31\n
      6,BRA,156\n
      7,BRA,27\n
      8,BRA,8\n
      9,FRA,174\n
      10,POL,89\n
      11,POL,30\n
      13,RWA,121\n
      14,KEN,1\n
      15,KEN,15\n
      16,KEN,1\n
      18,NLD,102\n""",
), skipinitialspace=True)

# Create and display the figure
fig = fig_sunburst(
   data,
   title="Sunburst Plot of Synthetic Patient Enrolment by Site",
   path=["Country", "Site"],
   values="SubjectID",
)
fig.update_layout(height=600)
fig

# %%
# You should see the plot appearing as given above.
#
# .. note::
#
#   Any dataframe or CSV column names, or dictionary field labels, in the
#   example above that are not specific to the dataset must be as given,
#   otherwise the function may throw an exception or return an incorrect figure.
#
#   Also, the ``height`` parameter, which is optional with a default of ``430``,
#   can be used to customise the plot height. Refer to the
#   :py:func:`~isaricanalytics.visualisation.fig_sunburst` function
#   docstring for more information.
