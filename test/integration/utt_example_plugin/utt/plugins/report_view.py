from utt.api import _v1


class MySubModel:
    def __init__(self, activities: _v1.Activities):
        self._activities = activities

    @property
    def activity_count(self):
        return len(self._activities)


_v1.register_component(MySubModel, MySubModel)


class MySubView:
    def __init__(self, my_sub_model: MySubModel):
        self._my_sub_model = my_sub_model

    def render(self, output: _v1.Output) -> None:
        print(f"Number of activities: {self._my_sub_model.activity_count}", file=output)


class MyReportView(_v1.ReportView):
    def __init__(self, report_model: _v1.ReportModel, my_sub_model: MySubModel):
        self._report_model = report_model
        self._my_sub_model = my_sub_model

    def render(self, output: _v1.Output) -> None:
        _v1.SummaryView(self._report_model.summary_model).render(output)

        if self._report_model.per_day:
            _v1.PerDayView(self._report_model.per_day_model).render(output)
        else:
            _v1.ProjectsView(self._report_model.projects_model).render(output)

        _v1.ActivitiesView(self._report_model.activities_model).render(output)

        if (self._report_model.start_date == self._report_model.end_date) or self._report_model.show_details:
            _v1.DetailsView(self._report_model.details_model, show_comments=self._report_model.show_comments).render(
                output
            )

        MySubView(self._my_sub_model).render(output)


_v1.register_component(_v1.ReportView, MyReportView)
