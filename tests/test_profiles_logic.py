import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import ttk
from src.profiles_logic import open_profiles_window, profiles_choice


class TestProfilesLogic(unittest.TestCase):

    @patch('src.profiles_logic.profiles_choice')
    @patch('tkinter.Tk')
    @patch('tkinter.ttk.Frame')
    @patch('tkinter.ttk.Label')
    @patch('tkinter.ttk.Button')
    def test_open_profiles_window(self, MockButton, MockLabel, MockFrame, MockTk, mock_profiles_choice):
        mock_window = MockTk.return_value
        mock_frame = MockFrame.return_value
        mock_label = MockLabel.return_value
        mock_button = MockButton.return_value

        title = "Test Title"
        size = (800, 600)
        open_profiles_window(title, size)

        MockTk.assert_called_once()
        mock_window.title.assert_called_once_with(title)

        mock_window.geometry.assert_called_once_with(f'{size[0]}x{size[1]}')
        mock_window.minsize.assert_called_once_with(size[0], size[1])

        MockFrame.assert_called_once_with(mock_window)
        mock_profiles_choice.assert_called_once_with(mock_window, mock_frame)

if __name__ == '__main__':
    unittest.main()
