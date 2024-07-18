import unittest
from unittest.mock import patch, MagicMock, Mock
import tkinter as tk
from tkinter import ttk
from src.profiles_logic import open_profiles_window, profiles_choice, profile_selection


class TestProfilesLogic(unittest.TestCase):

    @patch('src.profiles_logic.profiles_choice')
    @patch('tkinter.Tk')
    @patch('tkinter.ttk.Frame')
    def test_open_profiles_window(self, MockFrame, MockTk, mock_profiles_choice):
        mock_window = MockTk.return_value
        mock_frame = MockFrame.return_value

        title = "Test Title"
        size = (800, 600)
        open_profiles_window(title, size)

        MockTk.assert_called_once()
        mock_window.title.assert_called_once_with(title)

        mock_window.geometry.assert_called_once_with(f'{size[0]}x{size[1]}')
        mock_window.minsize.assert_called_once_with(size[0], size[1])

        MockFrame.assert_called_once_with(mock_window)
        mock_profiles_choice.assert_called_once_with(mock_window, mock_frame)

    @patch('src.profiles_logic.Main_window')
    def test_profile_selection(self, MockMainWindow):
        mock_profiles_window = MagicMock()
        profile = {'nome': 'admin'}
        logout_value = MagicMock(spec=tk.BooleanVar)
        logout_value.set.return_value = False

        with patch('tkinter.BooleanVar', return_value=logout_value):
            profile_selection(mock_profiles_window, profile)

        MockMainWindow.assert_called_once_with(profile, logout_value)
        MockMainWindow.return_value.mainloop.assert_called_once()
        if logout_value.get():
            mock_profiles_window.destroy.assert_called_once()

if __name__ == '__main__':
    unittest.main()
