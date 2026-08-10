"""
Frequency Plots
===============
"""

# %%
# Frequency plots/charts refer to `stacked horizontal bar charts <https://en.wikipedia.org/wiki/Bar_chart#Stacked_bar_chart>`_ which show frequency distribution of data across labelled and segmented subgroups, with segment widths representing the proportion or frequency of the subgroup. These can be generated using the :py:func:`~isaricanalytics.visualisation.fig_frequency_chart` function, which returns a :py:class:`Plotly Go Figure <plotly.graph_objs._figure.Figure>` object.
#
# The plot below was generated using a synthetic dataset of patient treatment complications for Dengue, consisting of ten patients and five complications. **Click** the image to view the full interactive and fully annotated Plotly Go figure.
#
# The synthetic dataset is given below as a table (which can easily be converted to a CSV).
#
# .. list-table:: Synthetic dataset for Dengue patient treatment complications
#    :header-rows: 1
#    :widths: auto
#
#    * - Subgroup Label / Outcome Variable
#      - Description / Short Label
#      - Frequency
#    * - Dengue Haemorrhagic Fever
#      - DHF
#      - 0.4
#    * - Dengue Shock Syndrome
#      - DSS
#      - 0.2
#    * - Thrombocytopenia
#      - Low Platelets
#      - 0.6
#    * - Hepatomegaly
#      - Hepatomegaly
#      - 0.3
#    * - Plasma Leakage
#      - Plasma Leakage
#      - 0.1
#
# The :py:func:`~isaricanalytics.visualisation.fig_frequency_chart` function expects a dataframe with the following columns (in no particular order):
#
# * ``"label"`` - the subgroup label / outcome variable column of the table
# * ``"short_label"`` - the description column of the table
# * ``"proportion"`` - the frequency column of the table
#
# The data source can be in any appropriate form, such as, typically, a CSV. Here are the Python steps you need to generate the plot above using the :py:func:`~isaricanalytics.visualisation.fig_frequency_chart` function:
#
# Here are the Python steps you need to generate the plot.
import io, pandas as pd
from isaricanalytics.visualisation import fig_frequency_chart
# Load the CSV data from a string buffer
data = pd.read_csv(io.StringIO(
   """label,short_label,proportion\n
      Dengue Haemorrhagic Fever,DHF,0.4\n
      Dengue Shock Syndrome,DSS,0.2\n
      Thrombocytopenia,Low Platelets,0.6\n
      Hepatomegaly,Hepatomegaly,0.3\n
      Plasma Leakage,Plasma Leakage,0.1\n
   """
), skipinitialspace=True)
# Create and display the figure
fig = fig_frequency_chart(
   data,
   title="Frequency Chart of Synthetic Dengue Patient Complications",
)
fig.update_layout(autosize=True)
fig

# %%
# You should see the plot appearing as given above.
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
#    parameter. Refer to the :py:func:`~isaricanalytics.visualisation.fig_frequency_chart`
#    function docstring for more information.
