from .summary_section import SummaryView
from .projects_section import ProjectsView
from .activities_section import ActivitiesView
from .details_section import DetailsView


def print_report(report, output):
    SummaryView(report.summary_model).render(output)
    ProjectsView(report.projects_model).render(output)
    ActivitiesView(report.activities_model).render(output)
    if report.start_date == report.end_date:
        DetailsView(report.details_model).render(output)
