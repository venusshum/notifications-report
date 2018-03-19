from app import notify_workspace

def report_data():
    cut = PointCut("dm_service", [True, 'Test'])

    cell = Cell(cube, [cut])
    result = browser.aggregate(cell, drilldown=['dm_datetime'])

    for record in result:
        print(record)

    print('\n\n')
