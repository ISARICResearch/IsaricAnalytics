"""
Upset Plots
===========
"""

# %%
# `Upset plots <https://en.wikipedia.org/wiki/UpSet_plot>`_ can be generated using the :py:func:`~isaricanalytics.visualisation.fig_upset` function, which returns a :py:class:`Plotly Go Figure <plotly.graph_objs._figure.Figure>` object.

# %%
# The plot below was generated using a synthetic dataset of patient treatment complications for Dengue, consisting of five complications and their patient counts, as well as counts for the intersections (conjoint occurrences) of the complication subsets.
#
# The dataset is given below as a table (but can also be loaded from the static :file:`examples/csv/upset.csv` file).
#
# .. list-table:: Dengue patient treatment complications - patient counts
#    :header-rows: 1
#    :widths: auto
#
#    * - Complication
#      - Patient Count
#    * - Shock
#      - 891
#    * - Meningitis
#      - 781
#    * - Acute renal injury / acute renal failure
#      - 757
#    * - Cardiac arrest
#      - 709
#    * - Focal neurological signs
#      - 702
#
# and the second showing the intersections between these subsets:
#
# .. list-table:: Dengue patient treatment complications - intersection counts
#    :header-rows: 1
#    :widths: auto
#
#    * - Complication Intersections
#      - Patient Count
#    * - Shock, Meningitis, Acute renal injury / acute renal failure, Cardiac arrest, Focal neurological signs
#      - 256
#    * - Shock, Meningitis, Acute renal injury / acute renal failure, Cardiac arrest
#      - 121
#    * - Shock, Meningitis, Acute renal injury / acute renal failure, Focal neurological signs
#      - 115
#    * - Shock, Meningitis, Cardiac arrest, Focal neurological signs
#      - 86
#    * - Shock, Acute renal injury / acute renal failure, Cardiac arrest, Focal neurological signs
#      - 67
#    * - Shock, Meningitis, Focal neurological signs
#      - 37
#    * - Shock, Acute renal injury / acute renal failure, Cardiac arrest
#      - 37
#    * - Shock, Acute renal injury / acute renal failure, Focal neurological signs
#      - 34
#    * - Shock, Meningitis, Cardiac arrest
#      - 31
#    * - Shock, Meningitis, Acute renal injury / acute renal failure
#      - 30
#    * - Meningitis, Acute renal injury / acute renal failure, Cardiac arrest, Focal neurological signs
#      - 30
#    * - Shock, Cardiac arrest, Focal neurological signs
#      - 26
#    * - Meningitis, Acute renal injury / acute renal failure, Focal neurological signs
#      - 18
#    * - Shock, Meningitis
#      - 15
#    * - Meningitis, Acute renal injury / acute renal failure, Cardiac arrest
#      - 15
#    * - Shock, Acute renal injury / acute renal failure
#      - 14
#    * - Shock, Cardiac arrest
#      - 11
#    * - Shock, Focal neurological signs
#      - 9
#    * - Meningitis, Cardiac arrest, Focal neurological signs
#      - 8
#    * - Meningitis, Acute renal injury / acute renal failure
#      - 7
#    * - Meningitis, Cardiac arrest
#      - 6
#    * - Acute renal injury / acute renal failure, Cardiac arrest, Focal neurological signs
#      - 6
#    * - Acute renal injury / acute renal failure, Cardiac arrest
#      - 5
#    * - Meningitis, Focal neurological signs
#      - 3
#    * - Meningitis,
#      - 3
#    * - Cardiac arrest, Focal neurological signs
#      - 3
#    * - Shock,
#      - 2
#    * - Acute renal injury / acute renal failure, Focal neurological signs
#      - 2
#    * - Focal neurological signs,
#      - 2
#    * - Cardiac arrest,
#      - 1
#
# The :py:func:`~isaricanalytics.visualisation.fig_upset` function expects these tables in the form of **a pair** of dataframes, the first dataframe containing the complication counts data with the following columns (in no particular order):
#
# * ``"index"`` - a label internal to the function denoting the complication, and prefixed with ``"compl"``, e.g. ``"compl_shock"`` for shock, ``"compl_meningitis"`` for meningitis, ``"compl_acuterenal"`` for acute renal injury / failure etc.
# * ``"label"`` - a descriptive label for the complication
# * ``"short_label"`` - a more concise descriptive label for the complication, which could be the same as the value of ``"label"``
# * ``"count"`` - the complication count
#
# and the second dataframe containing the complication intersection data with the following columns (in no particular order):
#
# * ``"index"`` - a string form of a tuple of the labels described above for the complications, e.g. ``"('compl_shock', 'compl_meningitis', 'compl_acuterenal', 'compl_cardiarrest', 'compl_focalneuro')"`` for the intersection of shock, meningitis, acute renal injury / failure, cardiac arrest, focal neurological signs.
# * ``"label"`` - a string form of the descriptive labels associated with the complications, e.g. ``"('Shock ', 'Meningitis', 'Acute renal injury / acute renal failure', 'Cardiac arrest', 'Focal neurological signs')"``
# * ``"count"`` - the complication intersection count
#
# Here are the Python steps you need to generate the plot using the :py:func:`~isaricanalytics.visualisation.fig_upset` function:
import io, pandas as pd
from isaricanalytics.visualisation import fig_upset

# Load the CSV data from a string buffer
counts = pd.read_csv("./csv/upset_counts.csv")
intersections = pd.read_csv("./csv/upset_intersections.csv")

# Create and display the figure
fig = fig_upset(
   (counts, intersections),
   title="Upset Plot of Dengue Patient Treatment Complications",
)
fig.update_layout(autosize=True)
fig

# %%
#
# .. note::
#
#    Note that the counts and intersections dataframes are provided in a :py:class:`tuple` object.
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
#    parameter. Refer to the :py:func:`~isaricanalytics.visualisation.fig_upset`
#    function docstring for more information.
