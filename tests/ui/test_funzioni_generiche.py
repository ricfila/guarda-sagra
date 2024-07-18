import unittest
from unittest.mock import MagicMock, patch, call
import tkinter as tk
from tkinter import ttk
from src.ui.funzioni_generiche import *




class TestFunzioniGeneriche(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.root = MagicMock()

    @classmethod
    def tearDownClass(self):
        self.root.destroy()

    def test_replace_single_quotes(self):
        result = replace_single_quotes("l'acqua l'aria")
        self.assertEqual(result, "l''acqua l''aria")

    def test_toggle_checkbox(self):
        var = MagicMock()

        toggle_checkbox(None, var)
        self.assertTrue(var.set.called)

    def test_crea_checkbox(self):
        parent_frame = MagicMock()
        label_text = "Test"
        var = MagicMock()
        var.get.return_value = False

        checkbox_frame = crea_checkbox(parent_frame, label_text, var)
        self.assertIsInstance(checkbox_frame, tk.Frame)

if __name__ == '__main__':
    unittest.main()
