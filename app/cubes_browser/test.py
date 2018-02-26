
from cubes import Workspace, PointCut, Cell, Cube, cuts_from_string


CUBE_NAME="ft_billing_template"
#analytical workspace
workspace = Workspace()
workspace.register_default_store("sql", url="postgresql://venusbailey@localhost:5432/notification_api",schema="reports")
#Model
workspace.import_model("./model.json")

# Aggregations

print('\n\n...test aggregation...')
browser = workspace.browser(CUBE_NAME)
cube = browser.cube
result = browser.aggregate()
print('Sum of record counts = ' + str(result.summary["record_count"]))
print('Amount = ' + str(result.summary["amount_sum"]))

# Drill down on year
print('\n\n....drilling down on year...')
result = browser.aggregate(drilldown=["dm_datetime:year"])
for record in result:
     print(record)

# Drill down on service
print('\n\n...drilling down on services...')
result = browser.aggregate(drilldown=["dm_service:service_name"])
for record in result:
    print(record)
    # print(record["dm_service.crown"], "\t", record['amount_sum'])



# Cut

print('\n\n...Cut services for Crown Service Only...')

dimension = cube.dimension("dm_service")
hierarchy = dimension.hierarchy()

cell = Cell(cube, cuts_from_string(cube, "dm_service:True"))

cut = cell.cut_for_dimension(dimension)

if cut:
    path = cut.path
else:
    path = []

#
# Do the work, do the aggregation.
#
result = browser.aggregate(cell, drilldown=["dm_datetime"])
for record in result:
    print(record)



print('\n\n...Cut year for 2018 Only...')

# cuts = [
#     PointCut("dm_year", ["Test"])
# ]
cell = Cell(cube)
cell = cell.drilldown("dm_datetime", 2018)


result = browser.aggregate(cell, drilldown=["dm_service:service_name"])
for record in result:
    print(record)

print('\n\n')





print('\n\n...Cut year for 2018 November Only...')

cut = PointCut("dm_datetime", [2017, 11])

cell = Cell(cube, [cut])
result = browser.aggregate(cell, drilldown=["dm_datetime"])

for record in result:
    print(record)

print('\n\n')



print('\n\n...Cut year for non-crown:Test service Only...')

cut = PointCut("dm_service", [True, 'Test'])

cell = Cell(cube, [cut])
result = browser.aggregate(cell, drilldown=['dm_datetime'])

for record in result:
    print(record)

print('\n\n')



# print('\n\n...Cut year for non-crown:Test service 2018 Only...')
#
# cuts = [PointCut("dm_service", [True, 'Test']),
#         PointCut("dm_datetime", [2017, 11])]
#
# cell = Cell(cube, [cuts])
# result = browser.aggregate(cell)
#
# for record in result:
#     print(record)
#
# print('\n\n')
