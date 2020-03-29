# flake8: noqa

from ...command import Command
from ...components.activities import Activities
from ...components.entries import Entries  # Injectable
from ...components.now import Now  # Injectable
from ...components.output import Output  # Injectable
from ...components.report_model import ReportModel
from ...components.report_view import ReportView  # Injectable
from ...constants import HELLO_ENTRY_NAME
from ...data_structures.activity import Activity
from ...data_structures.entry import Entry
from ...data_structures.name import Name
from ...report.activities.view import ActivitiesView
from ...report.details.view import DetailsView
from ...report.per_day.view import PerDayView
from ...report.projects.view import ProjectsView
from ...report.summary.view import SummaryView
from ._private import register_command, register_component
