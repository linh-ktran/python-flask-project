import pytest

from app.models.models import Asset, Manager, Site


@pytest.fixture(scope='module')
def new_manager():
    asset = Manager(fname='Nicolas', lname='Plain')
    return asset


@pytest.fixture(scope='module')
def new_site():
    asset = Site(name='SiteA', address='5 Carlos street', p_max=18000)
    return asset


@pytest.fixture(scope='module')
def new_asset():
    asset = Asset(name='C3', type='CHILLER', p_nominal=2000)
    return asset



"""
from config import db
from build_database import MANAGERS, create_db


@pytest.fixture(scope='module')
def init_database():
    create_db(data=MANAGERS)
    yield db
    db.drop_all()


@pytest.fixture(scope="session")
def app():
    abs_file_path = os.path.abspath(os.path.dirname(__file__))
    openapi_path = os.path.join(abs_file_path, "../", "openapi")
    os.environ["SPEC_PATH"] = openapi_path

    app = create_app()
    return app


from config import create_app

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!






from shutil import copy
import pytest
from football_api.api import create_app
from football_api.constants import FANTASY_FOOTBALL_DATABASE, PROJECT_ROOT


@pytest.fixture
def client(tmpdir):
    copy(f"{PROJECT_ROOT}/{FANTASY_FOOTBALL_DATABASE}", tmpdir.dirpath())

    temp_db_file = f"sqlite:///{tmpdir.dirpath()}/{FANTASY_FOOTBALL_DATABASE}"

    app = create_app(temp_db_file)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
"""