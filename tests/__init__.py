from unittest.mock import MagicMock

def definisci_mock(mock_get_connection):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None
    mock_get_connection.return_value = mock_connection
    return mock_cursor
