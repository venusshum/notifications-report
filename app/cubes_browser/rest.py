from flask import Blueprint, render_template, request, make_response

from cubes import Workspace, Cell, cuts_from_string

from app import notify_workspace


cubes_blueprint = Blueprint(
    'cubes_browser',
    __name__,
    url_prefix='/cubes'
)

CUBE_NAME="ft_billing"


@cubes_blueprint.route('', methods=['GET', 'POST'])
@cubes_blueprint.route("/<dim_name>")
def report(dim_name=None):
    browser = notify_workspace.browser(CUBE_NAME)
    cube = browser.cube
    if not dim_name:
        return render_template('report.html', dimensions=cube.dimensions)

    # First we need to get the hierarchy to know the order of levels. Cubes
    # supports multiple hierarchies internally.

    dimension = cube.dimension(dim_name)
    hierarchy = dimension.hierarchy()

    # Parse the`cut` request parameter and convert it to a list of
    # actual cube cuts. Think of this as of multi-dimensional path, even that
    # for this simple example, we are goint to use only one dimension for
    # browsing.

    cutstr = request.args.get("cut")
    cell = Cell(cube, cuts_from_string(cube, cutstr))

    # Get the cut of actually browsed dimension, so we know "where we are" -
    # the current dimension path
    cut = cell.cut_for_dimension(dimension)

    if cut:
        path = cut.path
    else:
        path = []

    #
    # Do the work, do the aggregation.
    #
    result = browser.aggregate(cell, drilldown=[dim_name])
    # If we have no path, then there is no cut for the dimension, # therefore
    # there is no corresponding detail.
    if path:
        details = browser.cell_details(cell, dimension)[0]
    else:
        details = []

    # Find what level we are on and what is going to be the drill-down level
    # in the hierarchy

    levels = hierarchy.levels_for_path(path)
    if levels:
        next_level = hierarchy.next_level(levels[-1])
    else:
        next_level = hierarchy.next_level(None)

    # Are we at the very detailed level?

    is_last = hierarchy.is_last(next_level)
    # Finally, we render it

    return render_template('report.html',
                            dimensions=cube.dimensions,
                            dimension=dimension,
                            levels=levels,
                            next_level=next_level,
                            result=result,
                            cell=cell,
                            is_last=is_last,
                            details=details)
