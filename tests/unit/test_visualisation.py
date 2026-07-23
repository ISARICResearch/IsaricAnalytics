# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --
import pandas as pd
import plotly.graph_objs as go
import pytest
from numpy.testing import assert_array_equal

# -- Internal libraries --
from isaricanalytics.utils import strip_html
from isaricanalytics.visualisation import (
    fig_bar_chart,
    fig_count_chart,
    fig_dual_stack_pyramid,
    fig_forest_plot,
    fig_frequency_chart,
    fig_kaplan_meier,
    fig_pie,
    fig_placeholder,
    fig_sunburst,
    fig_table,
    fig_timelines,
    hex_to_rgb,
    hex_to_rgba,
    rgb_to_rgba,
)


class TestFigBarChart:
    def test_fig_bar_chart(self):
        data_in = pd.DataFrame().assign(
            time=["06:00", "09:00", "12:00", "15:00", "18:00", "21:00"],
            temperature=[12.0, 15.5, 18.9, 20.2, 18.5, 15.8],
        )
        fig_out = fig_bar_chart(
            data_in,
            title="Test bar chart - time vs temperature (Celsius)",
            xlabel="Time of day",
            ylabel="Temperature (Celsius)",
            index_column="time",
            height=340,
        )

        assert isinstance(fig_out, go.Figure)
        assert (
            fig_out.layout.title.text
            == "Test bar chart - time vs temperature (Celsius)"
        )
        assert fig_out.layout.height == 340
        assert isinstance(fig_out.data[0], go._bar.Bar)
        assert_array_equal(fig_out.data[0].x, data_in["time"].values)
        assert_array_equal(fig_out.data[0].y, data_in["temperature"].values)


class TestFigCountChart:
    def test_fig_count_chart(self):
        data_in = pd.DataFrame().assign(
            label=["Mathematics", "Economics", "Physics", "Physiology or Medicine"],
            count=[2, 3, 2, 3],
            short_label=[
                "Mathematics",
                "Economics",
                "Physics",
                "Physiology or Medicine",
            ],
        )
        fig_out = fig_count_chart(
            data_in,
            title="Test count chart - students by major field",
            xlabel="Count",
            ylabel="Student Major Field",
            height=350,
        )

        assert isinstance(fig_out, go.Figure)
        assert fig_out.layout.title.text == "Test count chart - students by major field"
        assert fig_out.layout.height == 350
        assert len(fig_out.data) == 4
        assert all(isinstance(data_item, go._bar.Bar) for data_item in fig_out.data)


class TestFigDualStackedPyramid:
    def test_fig_dual_stack_pyramid(self):
        # Test data taken from the dual stacked pyramid chart in the Dengue
        # demo project with synthetic data.
        data_in = pd.DataFrame(
            columns=["side", "y_axis", "stack_group", "value", "left_side"],
            data=[
                ["Female", "0-5", "Censored", 2, True],
                ["Female", "0-5", "Death", 1, True],
                ["Female", "0-5", "Discharged", 3, True],
                ["Male", "0-5", "Death", 13, False],
                ["Male", "0-5", "Censored", 18, False],
                ["Male", "0-5", "Discharged", 12, False],
                ["Male", "6-10", "Death", 5, False],
                ["Male", "6-10", "Discharged", 2, False],
                ["Male", "6-10", "Censored", 5, False],
                ["Female", "6-10", "Censored", 3, True],
                ["Female", "6-10", "Death", 1, True],
                ["Male", "11-15", "Censored", 2, False],
                ["Male", "11-15", "Death", 3, False],
                ["Male", "16-20", "Death", 1, False],
                ["Female", "16-20", "Censored", 1, True],
                ["Female", "16-20", "Discharged", 1, True],
                ["Female", "16-20", "Death", 1, True],
                ["Male", "16-20", "Discharged", 1, False],
                ["Male", "16-20", "Censored", 4, False],
                ["Male", "21-25", "Death", 2, False],
                ["Male", "21-25", "Censored", 1, False],
                ["Female", "26-30", "Discharged", 1, True],
                ["Male", "26-30", "Censored", 6, False],
                ["Male", "26-30", "Discharged", 4, False],
                ["Female", "26-30", "Censored", 1, True],
                ["Male", "26-30", "Death", 2, False],
                ["Male", "31-35", "Death", 2, False],
                ["Male", "31-35", "Discharged", 3, False],
                ["Male", "31-35", "Censored", 3, False],
                ["Male", "36-40", "Discharged", 2, False],
                ["Male", "36-40", "Death", 1, False],
                ["Male", "36-40", "Censored", 4, False],
                ["Female", "36-40", "Censored", 1, True],
                ["Female", "36-40", "Death", 1, True],
                ["Female", "36-40", "Discharged", 1, True],
                ["Female", "41-45", "Censored", 1, True],
                ["Male", "41-45", "Censored", 5, False],
                ["Male", "41-45", "Death", 1, False],
                ["Male", "41-45", "Discharged", 3, False],
                ["Male", "46-50", "Censored", 5, False],
                ["Male", "46-50", "Death", 4, False],
                ["Male", "46-50", "Discharged", 4, False],
                ["Female", "46-50", "Censored", 1, True],
                ["Female", "51-55", "Censored", 1, True],
                ["Male", "51-55", "Death", 1, False],
                ["Male", "51-55", "Discharged", 2, False],
                ["Male", "51-55", "Censored", 1, False],
                ["Male", "56-60", "Death", 1, False],
                ["Male", "56-60", "Discharged", 4, False],
                ["Male", "56-60", "Censored", 3, False],
                ["Female", "56-60", "Death", 1, True],
                ["Female", "61-65", "Censored", 1, True],
                ["Male", "61-65", "Discharged", 2, False],
                ["Male", "61-65", "Death", 4, False],
                ["Male", "61-65", "Censored", 5, False],
                ["Male", "66-70", "Discharged", 2, False],
                ["Male", "66-70", "Censored", 5, False],
                ["Male", "66-70", "Death", 2, False],
                ["Female", "66-70", "Discharged", 1, True],
                ["Male", "71-75", "Discharged", 1, False],
                ["Female", "71-75", "Death", 1, True],
                ["Male", "71-75", "Censored", 3, False],
                ["Male", "71-75", "Death", 1, False],
                ["Male", "76-80", "Discharged", 1, False],
                ["Male", "76-80", "Death", 1, False],
                ["Male", "76-80", "Censored", 3, False],
                ["Female", "76-80", "Censored", 1, True],
                ["Male", "81-85", "Censored", 6, False],
                ["Male", "81-85", "Death", 2, False],
                ["Male", "81-85", "Discharged", 1, False],
                ["Female", "81-85", "Death", 2, True],
                ["Male", "86-90", "Death", 2, False],
                ["Male", "86-90", "Censored", 7, False],
                ["Male", "86-90", "Discharged", 2, False],
                ["Male", "91-95", "Discharged", 1, False],
                ["Male", "91-95", "Death", 2, False],
                ["Female", "91-95", "Censored", 1, True],
                ["Female", "91-95", "Death", 1, True],
                ["Male", "91-95", "Censored", 3, False],
                ["Male", "96-100", "Death", 2, False],
                ["Male", "96-100", "Censored", 3, False],
                ["Male", "96-100", "Discharged", 2, False],
            ],
        )
        fig_out = fig_dual_stack_pyramid(
            data_in,
            title=(
                "Test dual-sided population pyramid chart - "
                "showing age, sex and outcome"
            ),
            ylabel="Age Group",
            base_color_map={
                "Discharged": "#00C26F",
                "Censored": "#FFF500",
                "Death": "#DF0069",
            },
            height=430,
        )

        assert isinstance(fig_out, go.Figure)
        assert (
            fig_out.layout.title.text
            == "Test dual-sided population pyramid chart - showing age, sex and outcome"
        )
        assert fig_out.layout.height == 430

        # Bar charts for the no. of combinations of sex and outcome = 2 x 3 = 6
        assert len(fig_out.data) == 6
        assert all(isinstance(data_item, go._bar.Bar) for data_item in fig_out.data)


class TestFigForestPlot:
    def test_fig_forest_plot(self):
        data_in = pd.DataFrame(
            columns=[
                "Variable",
                "OddsRatio (multi)",
                "LowerCI (multi)",
                "UpperCI (multi)",
                "p-value (multi)",
            ],
            data=[
                ["Sex at birth, Male", 1.949, 1.149, 3.307, 0.0134],
                ["Age", 1.01, 0.998, 1.021, 0.1012],
                [
                    "Type of liver disease, Moderate or severe",
                    0.584,
                    0.183,
                    1.864,
                    0.3642,
                ],
                ["Obesity", 1.181, 0.679, 2.054, 0.555],
                ["Hypertension (physician diagnosed)", 2.399, 1.431, 4.022, 0.0009],
                [
                    "Vaccinated for seasonal influenza (ever)",
                    1.644,
                    0.98,
                    2.758,
                    0.0594,
                ],
                ["Fever", 1.379, 0.766, 2.484, 0.2841],
                ["Headache", 0.787, 0.469, 1.32, 0.3634],
                [
                    "Glasgow Coma Score (GCS / 15), Moderate (9 to 11)",
                    1.801,
                    0.96,
                    3.38,
                    0.0669,
                ],
                [
                    "Glasgow Coma Score (GCS / 15), Severe (less than 9)",
                    2.878,
                    1.526,
                    5.426,
                    0.0011,
                ],
                ["Platelets (10^3/uL), Low (under 1.5)", 1.536, 0.706, 3.339, 0.2789],
                ["Platelets (10^3/uL), High (over 4.5)", 4.741, 1.336, 16.829, 0.016],
                ["Employed as a healthcare worker", 0.644, 0.309, 1.341, 0.2398],
                ["Ever smoked", 1.53, 0.842, 2.781, 0.1631],
                ["Diabetes mellitus", 2.174, 1.231, 3.838, 0.0074],
                [
                    "Stage of chronic kidney disease, Stage 1",
                    1.607,
                    0.427,
                    6.048,
                    0.4833,
                ],
                [
                    "Stage of chronic kidney disease, Stage 2",
                    0.627,
                    0.194,
                    2.021,
                    0.4339,
                ],
                [
                    "Stage of chronic kidney disease, Stage 3a",
                    0.895,
                    0.281,
                    2.852,
                    0.8507,
                ],
                [
                    "Stage of chronic kidney disease, Stage 3b or 4 or 5",
                    1.798,
                    0.485,
                    6.674,
                    0.3803,
                ],
                ["Type of liver disease, Mild", 2.089, 0.975, 4.473, 0.058],
            ],
        )
        fig_out = fig_forest_plot(
            data_in,
            title="Test forest plot - anytime in-hospital mortality",
            xlabel="Odds Ratio (95% CI)",
            ylabel="",
            labels=[
                "Variable",
                "OddsRatio (multi)",
                "LowerCI (multi)",
                "UpperCI (multi)",
                "p-value (multi)",
            ],
            height=600,
        )

        assert isinstance(fig_out, go.Figure)
        assert (
            fig_out.layout.title.text
            == "Test forest plot - anytime in-hospital mortality"
        )
        assert fig_out.layout.xaxis.title.text == "Odds Ratio (95% CI)"
        assert fig_out.layout.height == 600
        assert len(fig_out.data) == 21
        assert all(
            isinstance(data_item, go._scatter.Scatter) for data_item in fig_out.data
        )
        assert set(fig_out.data[0].x) == set(data_in["OddsRatio (multi)"])
        assert set(fig_out.data[0].y) == set(data_in["Variable"])


class TestFigFrequencyChart:
    def test_fig_frequency_chart(self):
        data_in = pd.DataFrame().assign(
            label=["Mathematics", "Economics", "Physics", "Physiology or Medicine"],
            proportion=[0.3, 0.15, 0.1, 0.45],
            short_label=[
                "Mathematics",
                "Economics",
                "Physics",
                "Physiology or Medicine",
            ],
        )
        fig_out = fig_frequency_chart(
            data_in,
            title="Test frequency chart - student majors by field",
            xlabel="Percentage",
            ylabel="Student Major Field",
            height=350,
        )

        assert isinstance(fig_out, go.Figure)
        assert (
            fig_out.layout.title.text
            == "Test frequency chart - student majors by field"
        )
        assert fig_out.layout.height == 350
        assert len(fig_out.data) == 8
        assert all(isinstance(data_item, go._bar.Bar) for data_item in fig_out.data)


class TestFigKaplanMeier:
    def test_fig_kaplan_meier(self):
        km_data_in = pd.DataFrame(
            columns=[
                "timeline",
                "0-39",
                "0-39_lower_0.95",
                "0-39_upper_0.95",
                "40-64",
                "40-64_lower_0.95",
                "40-64_upper_0.95",
                ">64",
                ">64_lower_0.95",
                ">64_upper_0.95",
            ],
            data=[
                [0.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                [
                    3.0,
                    98.18181818181826,
                    96.39735054616156,
                    99.08657016907878,
                    99.55752212389378,
                    96.90088134700424,
                    99.93755232321789,
                    98.81889763779525,
                    96.38311787603637,
                    99.61753753722978,
                ],
                [
                    4.0,
                    98.18181818181826,
                    96.39735054616156,
                    99.08657016907878,
                    98.89820078532492,
                    95.54952547737416,
                    99.73073978542168,
                    98.81889763779525,
                    96.38311787603637,
                    99.61753753722978,
                ],
                [
                    5.0,
                    95.36768963520568,
                    92.60698242810584,
                    97.11347866289374,
                    98.89820078532492,
                    95.54952547737416,
                    99.73073978542168,
                    98.81889763779525,
                    96.38311787603637,
                    99.61753753722978,
                ],
                [
                    6.0,
                    94.42810648609036,
                    91.27618131269512,
                    96.46318369215324,
                    97.999126232731,
                    93.65495711588476,
                    99.37876135264092,
                    97.948246557286,
                    95.13505854819972,
                    99.14196321338244,
                ],
                [
                    7.0,
                    91.84103507551256,
                    87.53090853993217,
                    94.7060430396404,
                    96.7096640454582,
                    90.86213734535134,
                    98.8386876127919,
                    94.94983084634872,
                    91.034097752017,
                    97.18164888548608,
                ],
                [
                    8.0,
                    84.61758287856217,
                    77.37293717865721,
                    89.6953188510786,
                    92.59435919245998,
                    82.6454677155429,
                    96.94188674506084,
                    90.42841032985592,
                    85.10140816062759,
                    93.91813320008492,
                ],
                [
                    9.0,
                    76.15582459070596,
                    65.80771668823222,
                    83.75137248761123,
                    89.16493848162813,
                    75.70020536177844,
                    95.385530380624,
                    87.01601748721983,
                    80.64628925994477,
                    91.3999519629908,
                ],
                [
                    10.0,
                    66.22245616583126,
                    51.45905617744299,
                    77.43915318100328,
                    72.44651251632285,
                    48.96117462409049,
                    86.46098576504949,
                    82.3751632212348,
                    74.49383017790512,
                    88.01469585065641,
                ],
                [
                    11.0,
                    52.97796493266499,
                    32.231842991966055,
                    70.01448228633087,
                    63.39069845178251,
                    36.1082330026806,
                    81.54643352355325,
                    77.11717407945385,
                    67.23047069641812,
                    84.36189542328422,
                ],
                [
                    12.0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    69.13953538157931,
                    56.100461856710325,
                    79.0082809666679,
                ],
                [
                    13.0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    61.00547239551115,
                    44.7978150272324,
                    73.77461192167068,
                ],
                [
                    14.0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    47.44870075206421,
                    26.8197019105621,
                    65.55170703215035,
                ],
                [
                    15.0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    37.95896060165138,
                    16.243468770788308,
                    59.67418998689532,
                ],
            ],
        )
        risktable_data_in = pd.DataFrame(
            columns=["Group", "0", "5", "10", "15"],
            data=[
                ["0-39", 512, 314, 23, 0],
                ["40-64", 233, 151, 16, 0],
                [">64", 255, 254, 75, 5],
            ],
        )

        fig_out = fig_kaplan_meier(
            (km_data_in, risktable_data_in),
            title="Test Kaplan-Meier plot - in-hospital mortality",
            xlabel="Time (days)",
            ylabel="Survival Probability",
            index_column="Group",
            p_value=0.004799680324617032,
            height=480,
        )

        assert isinstance(fig_out, go.Figure)
        assert (
            fig_out.layout.annotations[0].text
            == "Test Kaplan-Meier plot - in-hospital mortality"
        )
        assert fig_out.layout.xaxis.title.text == "Time (days)"
        assert fig_out.layout.yaxis.title.text == "Survival Probability"
        assert fig_out.layout.height == 480


class TestFigPie:
    def test_fig_pie(self):
        data_in = pd.DataFrame().assign(
            country=["Country A", "Country B", "Country C", "Country D", "Country E"],
            population=[10000000, 2000000, 5000000, 12000000, 1000000],
        )
        fig_out = fig_pie(
            data_in,
            title="Test pie chart - countries and populations",
            xlabel="",
            ylabel="",
            base_color_map={
                10000000: "maroon",
                12000000: "red",
                1000000: "pink",
                2000000: "green",
                5000000: "yellow",
            },
            names=data_in["country"],
            values=data_in["population"],
            height=450,
        )

        assert isinstance(fig_out, go.Figure)
        assert fig_out.layout.title.text == "Test pie chart - countries and populations"
        assert fig_out.layout.height == 450
        assert isinstance(fig_out.data[0], go._pie.Pie)
        assert_array_equal(fig_out.data[0].labels, data_in["country"])
        assert_array_equal(fig_out.data[0].values, data_in["population"])


class TestFigPlaceholder:
    def test_fig_placeholder__no_data(self):
        fig_out = fig_placeholder(
            None,
            title="Test placeholder scatter plot - no data",
            xlabel="x",
            ylabel="y",
            height=450,
        )

        assert isinstance(fig_out, go.Figure)
        assert fig_out.layout.title.text == "Test placeholder scatter plot - no data"
        assert fig_out.layout.xaxis.title.text == "x"
        assert fig_out.layout.yaxis.title.text == "y"
        assert fig_out.layout.height == 450
        assert isinstance(fig_out.data[0], go._scatter.Scatter)
        assert_array_equal(fig_out.data[0].x, [1, 2, 3, 4, 5])
        assert len(fig_out.data[0].y) == 5
        assert min(fig_out.data[0].y) >= 10
        assert max(fig_out.data[0].y) <= 15

    def test_fig_placeholder__custom_data(self):
        data_in = pd.DataFrame().assign(x=[1, 2, 3, 4, 5], y=[1, 4, 9, 16, 25])
        fig_out = fig_placeholder(
            data_in,
            title="Test placeholder scatter plot - custom data",
            xlabel="x",
            ylabel="y",
            height=450,
        )

        assert isinstance(fig_out, go.Figure)
        assert (
            fig_out.layout.title.text == "Test placeholder scatter plot - custom data"
        )
        assert fig_out.layout.xaxis.title.text == "x"
        assert fig_out.layout.yaxis.title.text == "y"
        assert fig_out.layout.height == 450
        assert isinstance(fig_out.data[0], go._scatter.Scatter)
        assert_array_equal(fig_out.data[0].x, data_in["x"])
        assert_array_equal(fig_out.data[0].y, data_in["y"])


class TestFigSunburst:
    def test_fig_sunburst(self):
        data_in = pd.DataFrame().assign(
            total_bill=[16.99, 10.34, 21.01, 23.68, 24.59],
            tip=[1.01, 1.66, 3.50, 3.31, 3.61],
            sex=["Female", "Male", "Male", "Male", "Female"],
            smoker=["No", "No", "No", "No", "No"],
            day=["Sun", "Sat", "Fri", "Fri", "Sun"],
            occasion=["Dinner", "Lunch", "Drinks", "Drinks", "Dinner"],
        )
        fig_out = fig_sunburst(
            data_in,
            title="Test sunburst chart - restaurant bills by day, occasion, sex",
            path=["day", "occasion", "sex"],
            values="total_bill",
            height=430,
        )

        assert isinstance(fig_out, go.Figure)
        assert (
            fig_out.layout.title.text
            == "Test sunburst chart - restaurant bills by day, occasion, sex"
        )
        assert fig_out.layout.height == 430
        assert isinstance(fig_out.data[0], go._sunburst.Sunburst)


class TestFigTable:
    def test_fig_table(self):
        data_in = pd.DataFrame().assign(
            A=["A1", "A2", "A3", "A4", "A5"],
            B=["B1", "B2", "B3", "B4", "B5"],
            C=["C1", "C2", "C3", "C4", "C5"],
        )
        fig_out = fig_table(
            data_in,
            table_key="test_table_key",
            columnwidth=[0.1] * 3,
            height=500,
        )

        assert isinstance(fig_out, go.Figure)
        assert fig_out.layout.title.text == "test_table_key"
        assert fig_out.layout.height == 500
        assert isinstance(fig_out.data[0], go._table.Table)
        assert_array_equal(
            [strip_html(val) for val in fig_out.data[0].header.values],
            data_in.columns.tolist(),
        )
        for i, col in zip([0, 1, 2], ["A", "B", "C"]):
            assert_array_equal(fig_out.data[0].cells.values[i], data_in[col].values)


class TestFigText:
    def test_fig_text(self):
        data_in = pd.DataFrame(
            "Test disclaimer text", columns=["paragraphs"], index=range(1)
        )
        fig_out = fig_table(
            data_in,
            height=430,
        )

        assert isinstance(fig_out, go.Figure)
        assert fig_out.layout.height == 430
        assert isinstance(fig_out.data[0], go._table.Table)
        assert fig_out.data[0].cells.values[0][0] == "Test disclaimer text"


class TestFigTimelines:
    def test_fig_timelines__no_size_col(self):
        data_in = pd.DataFrame().assign(
            task=["Phase A", "Phase B", "Phase C"],
            start=["2026-01-01", "2026-03-05", "2026-02-20"],
            end=["2026-02-28", "2026-04-15", "2026-05-30"],
        )
        # One task per group, vice versa
        fig_out = fig_timelines(
            data_in,
            title="Test timelines plot - job phases",
            label_col="task",
            group_col="task",
            start_date="start",
            end_date="end",
            size_col=None,
            height=500,
        )

        assert isinstance(fig_out, go.Figure)
        assert fig_out.layout.title.text == "Test timelines plot - job phases"
        assert all(
            isinstance(data_item, go._scatter.Scatter) for data_item in fig_out.data
        )
        assert_array_equal([t.legendgroup for t in fig_out.data], data_in["task"])
        assert all(
            isinstance(data_item, go._scatter.Scatter) for data_item in fig_out.data
        )
        for i, task in enumerate(data_in["task"]):
            assert (
                str(fig_out.data[i].x[0].date())
                == data_in[data_in["task"] == task]["start"].at[i]
            )
            assert (
                str(fig_out.data[i].x[1].date())
                == data_in[data_in["task"] == task]["end"].at[i]
            )

    def test_fig_timelines__size_col(self):
        data_in = pd.DataFrame().assign(
            task=["Phase A", "Phase B", "Phase C"],
            start=["2026-01-01", "2026-03-05", "2026-02-20"],
            end=["2026-02-28", "2026-04-15", "2026-05-30"],
            line_width=[2, 2.5, 4],
        )
        # One task per group, vice versa
        fig_out = fig_timelines(
            data_in,
            title="Test timelines plot - job phases",
            label_col="task",
            group_col="task",
            start_date="start",
            end_date="end",
            size_col="line_width",
            height=500,
        )

        assert isinstance(fig_out, go.Figure)
        assert fig_out.layout.title.text == "Test timelines plot - job phases"
        assert all(
            isinstance(data_item, go._scatter.Scatter) for data_item in fig_out.data
        )
        assert_array_equal([t.legendgroup for t in fig_out.data], data_in["task"])
        assert all(
            isinstance(data_item, go._scatter.Scatter) for data_item in fig_out.data
        )
        for i, task in enumerate(data_in["task"]):
            assert (
                str(fig_out.data[i].x[0].date())
                == data_in[data_in["task"] == task]["start"].at[i]
            )
            assert (
                str(fig_out.data[i].x[1].date())
                == data_in[data_in["task"] == task]["end"].at[i]
            )


class TestHexToRgb:
    @pytest.mark.parametrize(
        """hex_color,
           expected_rgb_color""",
        [
            (
                "#000000",
                (0, 0, 0),
            ),
            (
                "#ffffff",
                (255, 255, 255),
            ),
            (
                "#092227",
                (9, 34, 39),
            ),
            (
                "#d9384b",
                (217, 56, 75),
            ),
        ],
    )
    def test_hex_to_rgb(self, hex_color, expected_rgb_color):
        assert hex_to_rgb(hex_color) == expected_rgb_color


class TestHexToRgba:
    @pytest.mark.parametrize(
        """hex_color,
           opacity,
           expected_rgba_string""",
        [
            (
                "#000000",
                0.0,
                "rgba(0, 0, 0, 0.0)",
            ),
            (
                "#092227",
                0.5,
                "rgba(9, 34, 39, 0.5)",
            ),
            (
                "#ffffff",
                1.0,
                "rgba(255, 255, 255, 1.0)",
            ),
        ],
    )
    def test_hex_to_rgba(self, hex_color, opacity, expected_rgba_string):
        assert hex_to_rgba(hex_color, opacity) == expected_rgba_string


class TestRgbToRgba:
    @pytest.mark.parametrize(
        """rgb_color,
           alpha,
           expected_rgba_string""",
        [
            ("rgb(0, 0, 0)", 0.0, "rgba(0,0,0,0.0)"),
            ("rgb(9, 34, 39)", 0.5, "rgba(9,34,39,0.5)"),
            ("rgb(255, 255, 255)", 1.0, "rgba(255,255,255,1.0)"),
        ],
    )
    def test_rgb_to_rgba(self, rgb_color, alpha, expected_rgba_string):
        assert rgb_to_rgba(rgb_color, alpha) == expected_rgba_string
