import itertools

def plain_text_format(context):

    print()
    print(_title(str(_format_date(context.args.date)) + \
                     " (week " + \
                     str(context.args.date.isocalendar()[1]) + \
                     ")"))
    print()

    print("Working Time: %s" % _format_duration(context.work.duration), end='')

    
    if context.work.current_activity:
        cur_duration = context.work.current_activity.duration
        print(" (%s + %s)" % (_format_duration(
                    context.work.duration - cur_duration),
                              _format_duration(cur_duration)))
    else:
        print()

    print("Break   Time: %s" % _format_duration(context.break_.duration),
          end='')
    if context.break_.current_activity:
        cur_duration = context.break_.current_activity.duration
        print(" (%s + %s)" % (_format_duration(
                    context.break_.duration - cur_duration),
                              _format_duration(cur_duration)))
    else:
        print()

        

    print()
    print(_title('Projects'))
    print()

    _print_dicts(list(map(_project2dict, context.work.projects)))

    print()
    print(_title('Activities'))
    print()

    _print_dicts(list(map(_grouped2dict, context.work.names)))

    print()

    _print_dicts(list(map(_grouped2dict, context.break_.names)))

    print()
    print(_title('Details'))
    print()

    # TODO: duration: aligne a droite
    # TODO: Faire de quoi generique avec print_dicts
    for activity in context.activities:
        print("(%s) %s-%s %s" % (_format_duration(activity.duration),
                                 _format_time(activity.start),
                                 _format_time(activity.end),
                                 activity.name))

    print()
   
def _format_date(datetime):
    return datetime.strftime("%A, %b %d, %Y")

def _format_duration(duration):
    mm, ss = divmod(duration.seconds, 60)
    hh, mm = divmod(mm, 60)
    s = "%dh%02d" % (hh, mm)
    if duration.days:
        def plural(n):
            return n, abs(n) != 1 and "s" or ""
        s = ("%d day%s, " % plural(duration.days)) + s
    return s

def _format_time(datetime):
    return datetime.strftime("%H:%M")

def _grouped2dict(grouped):
    return { 'duration': _format_duration(grouped.duration),
             'project': grouped.project,
             'name': grouped.name }

def _print_groups(groups):
    projects = (group.project for group in groups)
    projects_max_length = max(len(project) for project in projects)

    for group in groups:
        print("({duration}) {project:^{projects_max_length}}: {name}".format(
                duration=_format_duration(group.duration),
                project=group.project,
                name=group.name,
                projects_max_length=projects_max_length))

def _print_dicts(dcts):
    format_string = "({duration}) {project:^{projects_max_length}}: {name}"

    projects = (dct['project'] for dct in dcts)
    projects_max_length = max(
        itertools.chain([0], (len(project) for project in projects)))
    context = {'projects_max_length': projects_max_length}
    for dct in dcts:
        print(format_string.format(**dict(context, **dct)))

def _project2dict(project):
    return { 'duration': _format_duration(project.duration),
             'project': project.name,
             'name': ', '.join(sorted(set(act.name.task
                                          for act in project.activities))) }

def _title(text):
    return '{:-^80}'.format(' ' + text + ' ')
