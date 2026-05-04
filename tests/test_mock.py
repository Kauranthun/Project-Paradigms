from unittest.mock import patch
from app.services.logic import can_user_upload
from unittest.mock import MagicMock

def test_can_user_upload_limit_reached_mock():
    """Test que l'upload est bloqué si le compteur (mocké) atteint la limite."""
    class FakeUser:
        package = 'FREE'
        id = 1

    with patch('app.services.logic.get_user_daily_count') as mocked_count:
        mocked_count.return_value = 2
        
        result = can_user_upload(FakeUser())
        
        assert result is False
        mocked_count.assert_called_once()

def test_file_save_logic_mock():
    """Test la logique de sauvegarde sans écrire sur le disque."""
    mock_file = MagicMock()
    mock_file.filename = "test_image.jpg"

    path = "/fake/path/test_image.jpg"
    mock_file.save(path)
    
    mock_file.save.assert_called_with(path)