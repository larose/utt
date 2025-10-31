from datetime import datetime, timedelta
from io import StringIO

import pytz

from utt.data_structures.activity import Activity
from utt.report.project_summary.model import ProjectSummaryModel
from utt.report.project_summary.view import ProjectSummaryView


def create_activity(name, start_time, duration_minutes, is_current=False):
    start = pytz.UTC.localize(start_time)
    end = start + timedelta(minutes=duration_minutes)
    return Activity(name, start, end, is_current)


def test_view_output_with_aligned_colons():
    activities = [
        create_activity("project1: task1", datetime(2024, 1, 1, 9, 0), 240),
        create_activity("project2: task1", datetime(2024, 1, 1, 13, 0), 165),
        create_activity("project3: task1", datetime(2024, 1, 1, 16, 0), 30),
        create_activity("project4: task1", datetime(2024, 1, 1, 17, 0), 30),
        create_activity("project5: task1", datetime(2024, 1, 1, 18, 0), 15),
    ]
    model = ProjectSummaryModel(activities)
    view = ProjectSummaryView(model)
    output = StringIO()

    view.render(output)
    result = output.getvalue()

    lines = result.split("\n")
    assert "Project Summary" in lines[1]
    assert "project1: 4h00" in lines[3]
    assert "project2: 2h45" in lines[4]
    assert "project3: 0h30" in lines[5]
    assert "project4: 0h30" in lines[6]
    assert "project5: 0h15" in lines[7]
    assert "Total   : 8h00" in lines[9]


def test_view_output_with_current_activity():
    activities = [
        create_activity("project1: task1", datetime(2024, 1, 1, 9, 0), 240),
        create_activity("project2: task1", datetime(2024, 1, 1, 13, 0), 165),
        create_activity("project3: task1", datetime(2024, 1, 1, 16, 0), 30),
        create_activity("project4: task1", datetime(2024, 1, 1, 17, 0), 30),
        create_activity("project5: task1", datetime(2024, 1, 1, 18, 0), 15),
        create_activity("-- Current Activity --", datetime(2024, 1, 1, 19, 0), 220, is_current=True),
    ]
    model = ProjectSummaryModel(activities)
    view = ProjectSummaryView(model)
    output = StringIO()

    view.render(output)
    result = output.getvalue()

    lines = result.split("\n")
    assert "project1: 4h00" in lines[3]
    assert "project2: 2h45" in lines[4]
    assert "project3: 0h30" in lines[5]
    assert "project4: 0h30" in lines[6]
    assert "project5: 0h15" in lines[7]
    assert "-- Current Activity --: 3h40" in lines[8]
    assert "Total   : 11h40" in lines[10]


def test_view_colons_aligned_with_varying_project_lengths():
    activities = [
        create_activity("a: task1", datetime(2024, 1, 1, 9, 0), 60),
        create_activity("medium-name: task1", datetime(2024, 1, 1, 10, 0), 120),
        create_activity("very-long-project-name: task1", datetime(2024, 1, 1, 12, 0), 30),
    ]
    model = ProjectSummaryModel(activities)
    view = ProjectSummaryView(model)
    output = StringIO()

    view.render(output)
    result = output.getvalue()

    lines = result.split("\n")
    colon_positions = []
    for line in lines[3:6]:
        if ":" in line and "---" not in line:
            colon_positions.append(line.index(":"))

    assert len(set(colon_positions)) == 1, "All colons should be at the same position"


def test_view_empty_activities():
    model = ProjectSummaryModel([])
    view = ProjectSummaryView(model)
    output = StringIO()

    view.render(output)
    result = output.getvalue()

    assert "Project Summary" in result
    assert "Total: 0h00" in result


def test_view_single_project():
    activities = [
        create_activity("backend: api work", datetime(2024, 1, 1, 9, 0), 180),
    ]
    model = ProjectSummaryModel(activities)
    view = ProjectSummaryView(model)
    output = StringIO()

    view.render(output)
    result = output.getvalue()

    assert "backend: 3h00" in result
    assert "Total  : 3h00" in result


def test_view_projects_without_names():
    activities = [
        create_activity("standalone task", datetime(2024, 1, 1, 9, 0), 60),
        create_activity("another task", datetime(2024, 1, 1, 10, 0), 30),
    ]
    model = ProjectSummaryModel(activities)
    view = ProjectSummaryView(model)
    output = StringIO()

    view.render(output)
    result = output.getvalue()

    lines = result.split("\n")
    assert ": 1h30" in lines[3]
    assert "Total: 1h30" in lines[5]


def test_view_sorting_by_duration():
    activities = [
        create_activity("alpha: task1", datetime(2024, 1, 1, 9, 0), 30),
        create_activity("beta: task1", datetime(2024, 1, 1, 10, 0), 90),
        create_activity("gamma: task1", datetime(2024, 1, 1, 12, 0), 60),
    ]
    model = ProjectSummaryModel(activities)
    view = ProjectSummaryView(model)
    output = StringIO()

    view.render(output)
    result = output.getvalue()

    lines = [line for line in result.split("\n") if ":" in line and "Project Summary" not in line and "---" not in line]
    project_lines = [line for line in lines if "Total" not in line]

    assert "beta" in project_lines[0]
    assert "gamma" in project_lines[1]
    assert "alpha" in project_lines[2]


def test_view_large_durations():
    activities = [
        create_activity("marathon: task1", datetime(2024, 1, 1, 9, 0), 1500),
        create_activity("sprint: task1", datetime(2024, 1, 2, 10, 0), 600),
    ]
    model = ProjectSummaryModel(activities)
    view = ProjectSummaryView(model)
    output = StringIO()

    view.render(output)
    result = output.getvalue()

    assert "marathon: 25h00" in result
    assert "sprint  : 10h00" in result
    assert "Total   : 35h00" in result


def test_view_mixed_named_and_unnamed_projects():
    activities = [
        create_activity("asd: A-526", datetime(2024, 1, 1, 9, 0), 195),
        create_activity("qwer: b-73", datetime(2024, 1, 1, 12, 15), 45),
        create_activity("hard work", datetime(2024, 1, 1, 13, 0), 60),
        create_activity("A: z-8", datetime(2024, 1, 1, 14, 0), 30),
    ]
    model = ProjectSummaryModel(activities)
    view = ProjectSummaryView(model)
    output = StringIO()

    view.render(output)
    result = output.getvalue()

    lines = result.split("\n")
    assert "asd : 3h15" in lines[3]
    assert "    : 1h00" in lines[4]
    assert "qwer: 0h45" in lines[5]
    assert "A   : 0h30" in lines[6]
    assert "Total: 5h30" in lines[8]


def test_view_with_percentages():
    activities = [
        create_activity("project1: task1", datetime(2024, 1, 1, 9, 0), 240),
        create_activity("project2: task1", datetime(2024, 1, 1, 13, 0), 120),
        create_activity("project3: task1", datetime(2024, 1, 1, 15, 0), 60),
    ]
    model = ProjectSummaryModel(activities)
    view = ProjectSummaryView(model, show_perc=True)
    output = StringIO()

    view.render(output)
    result = output.getvalue()

    lines = result.split("\n")
    assert "project1: 4h00 ( 57.1%)" in lines[3]
    assert "project2: 2h00 ( 28.6%)" in lines[4]
    assert "project3: 1h00 ( 14.3%)" in lines[5]
    assert "Total   : 7h00 (100.0%)" in lines[7]


def test_view_with_percentages_and_current_activity():
    activities = [
        create_activity("project1: task1", datetime(2024, 1, 1, 9, 0), 240),
        create_activity("project2: task1", datetime(2024, 1, 1, 13, 0), 120),
        create_activity("-- Current Activity --", datetime(2024, 1, 1, 15, 0), 60, is_current=True),
    ]
    model = ProjectSummaryModel(activities)
    view = ProjectSummaryView(model, show_perc=True)
    output = StringIO()

    view.render(output)
    result = output.getvalue()

    lines = result.split("\n")
    assert "project1: 4h00 ( 57.1%)" in lines[3]
    assert "project2: 2h00 ( 28.6%)" in lines[4]
    assert "-- Current Activity --: 1h00 ( 14.3%)" in lines[5]
    assert "Total   : 7h00 (100.0%)" in lines[7]


def test_view_percentages_without_flag():
    activities = [
        create_activity("project1: task1", datetime(2024, 1, 1, 9, 0), 240),
        create_activity("project2: task1", datetime(2024, 1, 1, 13, 0), 120),
    ]
    model = ProjectSummaryModel(activities)
    view = ProjectSummaryView(model, show_perc=False)
    output = StringIO()

    view.render(output)
    result = output.getvalue()

    assert "%" not in result
    assert "project1: 4h00" in result
    assert "project2: 2h00" in result
