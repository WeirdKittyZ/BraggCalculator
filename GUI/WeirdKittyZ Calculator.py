# -*- coding: utf-8 -*-
"""
@author: zyj
GUI layout update by Microsoft Copilot, version 1.25
"""

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QSplashScreen,
    QProgressBar,
    QGridLayout,
    QSizePolicy,
    QTextBrowser,
    QMessageBox,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import time
import sys
import function


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WeirdKittyZ's Calculator")
        self.setGeometry(200, 200, 1400, 850)
        self.setMinimumSize(1100, 700)

        self.setStyleSheet("""
            QMainWindow {
                background-color: lavenderblush;
            }
            QGroupBox {
                color: black;
                font: bold 15pt 'Calibri';
                border: 2px solid lavender;
                border-radius: 10px;
                margin-top: 14px;
                padding: 16px 10px 10px 10px;
                background-color: rgba(255, 255, 255, 120);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 8px;
            }
            QPushButton {
                background-color: lavender;
                color: black;
                font: 14pt 'Calibri';
                min-height: 34px;
                border-radius: 6px;
            }
            QLabel {
                color: black;
                font: 14pt 'Calibri';
            }
            QLineEdit {
                color: black;
                font: 14pt 'Calibri';
                min-height: 30px;
                max-height: 30px;
            }
            QTextEdit, QTextBrowser {
                color: black;
                font: 13pt 'Calibri';
                border: 1px solid lavender;
                border-radius: 6px;
                background-color: white;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QGridLayout()
        main_layout.setContentsMargins(18, 18, 18, 12)
        main_layout.setHorizontalSpacing(18)
        main_layout.setVerticalSpacing(16)
        central_widget.setLayout(main_layout)

        angle_section = self._build_angle_section()
        bragg_section = self._build_bragg_section()
        energy_section = self._build_energy_section()
        notes_section = self._build_notes_section()

        main_layout.addWidget(angle_section, 0, 0)
        main_layout.addWidget(bragg_section, 0, 1)
        main_layout.addWidget(notes_section, 1, 0)
        main_layout.addWidget(energy_section, 1, 1)

        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 1)
        main_layout.setRowStretch(0, 3)
        main_layout.setRowStretch(1, 2)

        copyright_label = QLabel(
            "© 2026 WeirdKittyZ. Built with Microsoft Copilot. Version 4.1. All rights reserved."
        )
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("QLabel {color: black; font: 11pt 'Calibri';}")
        main_layout.addWidget(copyright_label, 2, 0, 1, 2)

    def _make_group_box(self, title):
        group_box = QGroupBox(title)
        group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return group_box

    def _make_line_edit(self):
        entry = QLineEdit()
        entry.setFixedWidth(120)
        entry.setAlignment(Qt.AlignCenter)
        entry.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        return entry

    def _make_result_box(self, min_height=130):
        result_box = QTextEdit()
        result_box.setReadOnly(True)
        result_box.setMinimumHeight(min_height)
        result_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return result_box

    def _add_label_entry_row(self, layout, row, labels, entries_list, start_col=0):
        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            entry = self._make_line_edit()
            col = start_col + i * 2
            layout.addWidget(label, row, col)
            layout.addWidget(entry, row, col + 1)
            entries_list.append(entry)

    def _build_angle_section(self):
        group_box = self._make_group_box("Angle Between Two HKLs")
        section_layout = QVBoxLayout()
        section_layout.setSpacing(12)
        group_box.setLayout(section_layout)

        input_grid = QGridLayout()
        input_grid.setHorizontalSpacing(10)
        input_grid.setVerticalSpacing(10)
        section_layout.addLayout(input_grid)

        self.lattice_params_entries = []
        self._add_label_entry_row(input_grid, 0, ["a (Å):", "b (Å):", "c (Å):"], self.lattice_params_entries)
        self._add_label_entry_row(input_grid, 1, ["α:", "β:", "γ:"], self.lattice_params_entries)

        for col in range(6):
            input_grid.setColumnStretch(col, 1)

        hkl_grid = QGridLayout()
        hkl_grid.setHorizontalSpacing(10)
        hkl_grid.setVerticalSpacing(10)
        section_layout.addLayout(hkl_grid)

        self.hkl_entries = []
        self._add_label_entry_row(hkl_grid, 0, ["h₁:", "k₁:", "l₁:"], self.hkl_entries)
        self._add_label_entry_row(hkl_grid, 1, ["h₂:", "k₂:", "l₂:"], self.hkl_entries)

        for col in range(6):
            hkl_grid.setColumnStretch(col, 1)

        calculate_button = QPushButton("Calculate Angle")
        calculate_button.clicked.connect(self.calculate_button_click1)
        section_layout.addWidget(calculate_button)

        self.result_text = self._make_result_box()
        self.result_text.setAlignment(Qt.AlignLeft)
        section_layout.addWidget(self.result_text)

        return group_box

    def _build_bragg_section(self):
        group_box = self._make_group_box("HKL Bragg Calculator")
        section_layout = QVBoxLayout()
        section_layout.setSpacing(12)
        group_box.setLayout(section_layout)

        wavelength_layout = QHBoxLayout()
        wavelength_layout.addStretch(1)
        wavelength_label = QLabel("Wavelength (Å):")
        wavelength_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.entry_A = self._make_line_edit()
        wavelength_layout.addWidget(wavelength_label)
        wavelength_layout.addWidget(self.entry_A)
        wavelength_layout.addStretch(1)
        section_layout.addLayout(wavelength_layout)

        hkl_grid = QGridLayout()
        hkl_grid.setHorizontalSpacing(10)
        hkl_grid.setVerticalSpacing(10)
        section_layout.addLayout(hkl_grid)

        self.hkl_entries_otherfun = []
        self._add_label_entry_row(hkl_grid, 0, ["h:", "k:", "l:"], self.hkl_entries_otherfun)

        for col in range(6):
            hkl_grid.setColumnStretch(col, 1)

        calculate_button = QPushButton("Calculate d-spacing and 2θ")
        calculate_button.clicked.connect(self.calculate_button_click2)
        section_layout.addWidget(calculate_button)

        self.result_text2 = self._make_result_box()
        self.result_text2.setAlignment(Qt.AlignCenter)
        section_layout.addWidget(self.result_text2)

        return group_box

    def _build_energy_section(self):
        group_box = self._make_group_box("Photon Energy Conversion")
        section_layout = QVBoxLayout()
        section_layout.setSpacing(12)
        group_box.setLayout(section_layout)

        energy_layout = QHBoxLayout()
        energy_layout.addStretch(1)
        energy_label = QLabel("Photon Energy (eV):")
        energy_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.entry_ev = self._make_line_edit()
        energy_layout.addWidget(energy_label)
        energy_layout.addWidget(self.entry_ev)
        energy_layout.addStretch(1)
        section_layout.addLayout(energy_layout)

        convert_button = QPushButton("Convert to Å")
        convert_button.clicked.connect(self.convert_energy)
        section_layout.addWidget(convert_button)

        self.result_text3 = self._make_result_box(110)
        self.result_text3.setAlignment(Qt.AlignCenter)
        section_layout.addWidget(self.result_text3)

        return group_box

    def _build_notes_section(self):
        group_box = self._make_group_box("Common X-ray Wavelengths")
        section_layout = QVBoxLayout()
        group_box.setLayout(section_layout)

        note_text = """
        Cu-Ka1 wavelength = 1.540562<br>
        Cu-Ka2 wavelength = 1.544398<br>
        Co-Ka1 wavelength = 1.788965<br>
        Co-Ka2 wavelength = 1.792850<br>
        Co-Kb1 wavelength = 1.620800<br>
        Mo-Ka1 wavelength = 0.709300<br>
        Mo-Ka2 wavelength = 0.713590<br>
        Ag-Ka1 wavelength = 0.559407<br>
        Ag-Ka2 wavelength = 0.563798<br>
        Cr-Ka1 wavelength = 2.289700<br>
        Cr-Ka2 wavelength = 2.293606<br>
        Fe-Ka1 wavelength = 1.936042<br>
        Fe-Ka2 wavelength = 1.939980<br>
        Ge-Ka1 wavelength = 1.254054<br>
        Ge-Ka2 wavelength = 1.258011<br>
        Ni-Ka1 wavelength = 1.657910<br>
        Ni-Ka2 wavelength = 1.661747<br>
        Zn-Ka1 wavelength = 1.435155<br>
        Zn-Ka2 wavelength = 1.439000
        """
        note_browser = QTextBrowser()
        note_browser.setReadOnly(True)
        note_browser.setOpenLinks(False)
        note_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        note_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        note_browser.setOpenExternalLinks(False)
        note_browser.setHtml(note_text)
        section_layout.addWidget(note_browser)

        return group_box

    def _show_error(self, message):
        QMessageBox.warning(self, "Input Error", message)

    def _read_float(self, entry, field_name):
        text = entry.text().strip()
        if not text:
            raise ValueError(f"{field_name} is empty. Please enter a number.")
        try:
            return float(text)
        except ValueError:
            raise ValueError(f"{field_name} must be a valid number. Current value: {text}")

    def _read_float_entries(self, entries, field_names):
        return [self._read_float(entry, field_name) for entry, field_name in zip(entries, field_names)]

    def calculate_button_click1(self):
        try:
            lattice_params = self._read_float_entries(
                self.lattice_params_entries,
                ["a", "b", "c", "alpha", "beta", "gamma"],
            )
            a_star_cartesian, b_star_cartesian, c_star_cartesian = function.lattice_vectors_to_cartesian(
                function.reciprocal_latt(lattice_params)
            )

            hkl_values = self._read_float_entries(
                self.hkl_entries,
                ["h1", "k1", "l1", "h2", "k2", "l2"],
            )
            v1 = hkl_values[0] * a_star_cartesian + hkl_values[1] * b_star_cartesian + hkl_values[2] * c_star_cartesian
            v2 = hkl_values[3] * a_star_cartesian + hkl_values[4] * b_star_cartesian + hkl_values[5] * c_star_cartesian

            angle = function.angle_between_vectors(v1, v2)
            self.result_text.append(
                f"Angle between ({hkl_values[0]}, {hkl_values[1]}, {hkl_values[2]}) and "
                f"({hkl_values[3]}, {hkl_values[4]}, {hkl_values[5]}) is: {angle:.2f} degrees"
            )
        except ValueError as error:
            self._show_error(str(error))
        except Exception as error:
            self._show_error(f"Calculation failed: {error}")

    def calculate_button_click2(self):
        try:
            lattice_params = self._read_float_entries(
                self.lattice_params_entries,
                ["a", "b", "c", "alpha", "beta", "gamma"],
            )
            hkl_values = self._read_float_entries(self.hkl_entries_otherfun, ["h", "k", "l"])
            wavelength_values = self._read_float(self.entry_A, "Wavelength")
            d_hkl, two_theta = function.bragg_angle(hkl_values, lattice_params, wavelength_values)
            self.result_text2.append(
                f"({hkl_values[0]}, {hkl_values[1]}, {hkl_values[2]}):\n"
                f"d-spacing: {d_hkl:.4f} Å\n"
                f"2θ angle: {two_theta:.2f} degrees\n"
            )
        except ValueError as error:
            self._show_error(str(error))
        except Exception as error:
            self._show_error(f"Calculation failed: {error}")

    def convert_energy(self):
        try:
            ev_value = self._read_float(self.entry_ev, "Photon Energy")
            angstrom_value = function.ev_to_angstrom(ev_value)
            self.result_text3.append(f"{ev_value} eV is {angstrom_value:.4f} Å\n")
        except ValueError as error:
            self._show_error(str(error))
        except Exception as error:
            self._show_error(f"Conversion failed: {error}")


import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def show_splash_screen():
    pixmap = QPixmap(resource_path("three_legged_horse.png"))
    print("Loaded:", pixmap.isNull())
    splash = QSplashScreen(pixmap)
    splash.show()
    app.processEvents()

    progress_bar = QProgressBar(splash)
    progress_bar.setMaximum(10)
    progress_bar.setGeometry(20, pixmap.height() - 40, pixmap.width(), 20)
    progress_bar.show()

    for i in range(1, 11):
        progress_bar.setValue(i)
        time.sleep(0.1)
        app.processEvents()

    return splash


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = show_splash_screen()
    window = MainWindow()
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())
