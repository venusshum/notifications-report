from flask import Blueprint


test_blueprint = Blueprint(
    'test',
    __name__,
    url_prefix='/test'
)


@test_blueprint.route('', methods=['GET', 'POST'])
def test_route():
    return 'Hello, World!'


@test_blueprint.route('/<any(service, org):level>', methods=['GET', 'POST'])
def test_any(level):
    return 'Hello, World! {}'.format(level)
