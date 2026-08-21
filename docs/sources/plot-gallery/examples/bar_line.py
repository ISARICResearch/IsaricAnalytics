"""
Bar Line Charts
===============
"""

# %%
# Bar-line charts, which combine `line charts <https://en.wikipedia.org/wiki/Line_chart>`_, can be generated using the :py:func:`~isaricanalytics.visualisation.fig_bar_line_chart` function, which returns a :py:class:`Plotly Go Figure <plotly.graph_objs._figure.Figure>` object.
#
# The plot below was generated using a synthetic dataset of monthly and cumulative patient enrolment data for a clinical site.
#
# The dataset is given below as a table (but can also be loaded from the static :file:`examples/csv/bar_line.csv` file).
#
# .. list-table:: Monthly and cumulative patient enrolment at a clinical site between January and June, 2026
#   :header-rows: 1
#   :widths: auto
#
#   * - Month-Year
#     - Patient Enrolment
#     - Cumulative Patient Enrolment
#   * - January 2026
#     - 2
#     - 2
#   * - February 2026
#     - 8
#     - 10
#   * - March 2026
#     - 50
#     - 60
#   * - April 2026
#     - 20
#     - 80
#   * - May 2026
#     - 15
#     - 95
#   * - June 2026
#     - 5
#     - 100
#
# In addition to the data(frame) itself, note some of the other key columns required :py:func:`~isaricanalytics.visualisation.fig_bar_line` function:
#
# * ``"xlabel"`` - the ``x``-axis label
# * ``"ylabel_left"`` - the left ``y``-axis label, which should correspond to the bar column (see below)
# * ``"ylabel_right"`` - the right ``y``-axis label, which should correspond to the line column (see below)
# * ``"bar_column"`` - the column representing the bar values, which should be labelled with ``"ylabel_left"``
# * ``"line_column"`` - the column representing the line values, which should be labelled with ``"ylabel_right"``
#
# Here are the Python steps you need to generate the plot using the :py:func:`~isaricanalytics.visualisation.fig_bar_line_chart` function:
import pandas as pd
from isaricanalytics.visualisation import fig_bar_line_chart

# Load the CSV
data = pd.read_csv("./csv/bar_line.csv")

# Create and display the figure
fig = fig_bar_line_chart(
    data,
    title="Bar-Line Chart of Monthly and Cumulative Patient Enrolment",
    xlabel="Month-Year",
    ylabel_left="Cumulative Patients Enrolled",
    ylabel_right="Patients Enrolled",
    bar_column="cum_patients_enrolled",
    line_column="patients_enrolled",
    index_column="month_year"
)
fig.update_layout(autosize=True)
fig

# %%
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
#    parameter. Refer to the :py:func:`~isaricanalytics.visualisation.fig_sunburst`
#    function docstring for more information.
