def test_new_manager(new_manager):
    """Test the asset's information when a new asset is created."""
    assert new_manager.fname == 'Nicolas'
    assert new_manager.lname == 'Plain'


def test_new_site(new_site):
    """Test the asset's information when a new asset is created."""
    assert new_site.name == 'SiteA'
    assert new_site.address == '5 Carlos street'
    assert new_site.p_max == 18000


def test_new_asset(new_asset):
    """Test the asset's information when a new asset is created."""
    assert new_asset.name == 'C3'
    assert new_asset.type == 'CHILLER'
    assert new_asset.p_nominal == 2000
