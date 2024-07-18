import unittest
from unittest.mock import MagicMock, patch, call
import tkinter as tk
from tkinter import ttk
from src.ui.funzioni_generiche import *




class TestFunzioniGeneriche(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.root = MagicMock(spec=tk.Tk())

    @classmethod
    def tearDownClass(self):
        self.root.destroy()

    def test_replace_single_quotes(self):
        result = replace_single_quotes("l'acqua l'aria")
        self.assertEqual(result, "l''acqua l''aria")

    def test_toggle_checkbox(self):
        var = tk.BooleanVar()
        var.set(False)

        toggle_checkbox(None, var)
        self.assertTrue(var.get())

        toggle_checkbox(None, var)
        self.assertFalse(var.get())

    def test_crea_checkbox(self):
        parent_frame = MagicMock(spec=tk.Frame())
        label_text = "Test"
        var = tk.BooleanVar()

        checkbox_frame = crea_checkbox(parent_frame, label_text, var)
        self.assertIsInstance(checkbox_frame, tk.Frame)

        var.set(True)
        checkbox_frame.event_generate("<ButtonRelease-1>")
        self.assertTrue(var.get())

        var.set(False)
        checkbox_frame.event_generate("<ButtonRelease-1>")
        self.assertFalse(var.get())


if __name__ == '__main__':
    unittest.main()
