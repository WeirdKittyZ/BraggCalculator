from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QLabel, QLineEdit,
                             QPushButton, QTextEdit, QSplashScreen, QProgressBar,
                             QGridLayout, QSpacerItem, QSizePolicy, QTextBrowser)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt 
import time
import sys
import function

class MainWindow(QMainWindow):
    def __init__(self):
        # Call the constructor of the base class (QMainWindow).
        super().__init__()

        # Set the window title.
        self.setWindowTitle("Zi's Calculator")

        # Set the position and size of the window.
        self.setGeometry(200, 200, 2000, 800)

        # Set the stylesheet for the window and its child widgets.
        self.setStyleSheet("""
            QMainWindow {
                background-color: lavenderblush;
            }
            QPushButton {
                background-color: lavender;
                color: black;
                font: 15pt 'Calibri';
            }
            QLabel {
                color: black;
                font: 15pt 'Calibri';
            }
            QLineEdit {
                color: black;
                font: 15pt 'Calibri';
            }
            QTextEdit {
                color: black;
                font: 15pt 'Calibri';
            }
        """)
        
        # Update the GUI to reflect the style sheet changes
        app.processEvents()



        # Create a central widget for the window.
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a grid layout for the central widget.
        layout = QGridLayout()
        central_widget.setLayout(layout)

        
# =============================================================================
# 
# =============================================================================
        # Lattice Parameters Input
        labels_a = ["a (Å):", "b (Å):", "c (Å):"]
        labels_alpha = ["α:", "β:", "γ:"]
        self.lattice_params_entries = []
        for i, label_text in enumerate(labels_a):
            label = QLabel(label_text)
            entry = QLineEdit()
            layout.addWidget(label, 1, i * 2 + 1)
            layout.addWidget(entry, 1, i * 2 + 2)
            self.lattice_params_entries.append(entry)
        for i, label_text in enumerate(labels_alpha):
            label = QLabel(label_text)
            entry = QLineEdit()
            layout.addWidget(label, 2, i * 2 + 1)
            layout.addWidget(entry, 2, i * 2 + 2)
            self.lattice_params_entries.append(entry)

        # HKL Parameters Input
        labels_hkl1 = ["h₁:", "k₁:", "l₁:"]
        labels_hkl2 = ["h₂:", "k₂:", "l₂:"]
        self.hkl_entries = []
        for i, (label_text1, label_text2) in enumerate(zip(labels_hkl1, labels_hkl2)):
            label1 = QLabel(label_text1)
            entry1 = QLineEdit()
            label2 = QLabel(label_text2)
            entry2 = QLineEdit()
            layout.addWidget(label1, 5, i * 2 + 1)
            layout.addWidget(entry1, 5, i * 2 + 2)
            layout.addWidget(label2, 6, i * 2 + 1)
            layout.addWidget(entry2, 6, i * 2 + 2)
            self.hkl_entries.extend([entry1, entry2])

        # Calculate Button
        calculate_button1 = QPushButton("Calculate")
        calculate_button1.clicked.connect(self.calculate_button_click1)
        layout.addWidget(calculate_button1, 7, 2, 1, 4)

        # Results Display
        self.result_text = QTextEdit()
        self.result_text.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.result_text, 8, 0, 5, 8)

# =============================================================================
# 
# =============================================================================
       # Energy Entry and Conversion Section
        label_ev = "Photon Energy (eV):"
        self.entry_ev = QLineEdit()
        layout.addWidget(QLabel(label_ev), 13, 9)
        layout.addWidget(self.entry_ev, 13, 10, 1, 2)
        
        convert_button1 = QPushButton("Convert to Å")
        convert_button1.clicked.connect(self.convert_energy)
        layout.addWidget(convert_button1, 13, 13, 1, 2)
        
        # Display Area for Energy Conversion Result
        self.result_text3 = QTextEdit()
        self.result_text3.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_text3, 14, 9, 5, 8)
        
        # Wavelength Entry Section
        label_A = "Wavelength (Å):"
        self.entry_A = QLineEdit()
        layout.addWidget(QLabel(label_A), 5, 9)
        layout.addWidget(self.entry_A, 5, 10, 1, 2)
        
        # Additional HKL Parameters Input
        labels_hkl_otherfun = ["h:", "k:", "l:"]
        self.hkl_entries_otherfun = []
        for i, label_text in enumerate(labels_hkl_otherfun):
            label = QLabel(label_text)
            entry = QLineEdit()
            layout.addWidget(label, 6, i * 2 + 8)
            layout.addWidget(entry, 6, i * 2 + 9)
            self.hkl_entries_otherfun.append(entry)
        
        # Calculate Button for Additional Functionality
        calculate_button2 = QPushButton("Calculate")
        calculate_button2.clicked.connect(self.calculate_button_click2)
        layout.addWidget(calculate_button2, 7, 10, 1, 3)
        
        # Display Area for Additional Calculation Result
        self.result_text2 = QTextEdit()
        self.result_text2.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_text2, 8, 9, 5, 8)

# =============================================================================
# 
# =============================================================================
# Note Section with Common X-ray Wavelengths
        note_text = """
        Cu-Ka1 wavelength=1.540562<br>
        Cu-Ka2 wavelength=1.544398<br>
        Co-Ka1 wavelength=1.788965<br>
        Co-Ka2 wavelength=1.792850<br>
        Mo-Ka1 wavelength=0.709300<br>
        Mo-Ka2 wavelength=0.713590<br>
        Ag-Ka1 wavelength=0.559407<br>
        Ag-Ka2 wavelength=0.563798<br>
        Cr-Ka1 wavelength=2.289700<br>
        Cr-Ka2 wavelength=2.293606<br>
        Fe-Ka1 wavelength=1.936042<br>
        Fe-Ka2 wavelength=1.939980<br>
        Ge-Ka1 wavelength=1.254054<br>
        Ge-Ka2 wavelength=1.258011<br>
        Ni-Ka1 wavelength=1.657910<br>
        Ni-Ka2 wavelength=1.661747<br>
        Zn-Ka1 wavelength=1.435155<br>
        Zn-Ka2 wavelength=1.439000"""
        note_browser = QTextBrowser()
        note_browser.setAlignment(Qt.AlignCenter)
        note_browser.setReadOnly(True)
        note_browser.setOpenLinks(False)
        note_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        note_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        note_browser.setOpenExternalLinks(False)
        note_browser.setHtml(note_text)
        
        layout.addWidget(note_browser, 14, 0, 5, 8)

    # Calculate Button 1 Click Event
    def calculate_button_click1(self):
        lattice_params = [float(entry.text()) for entry in self.lattice_params_entries]
        a_star_cartesian, b_star_cartesian, c_star_cartesian = function.lattice_vectors_to_cartesian(function.reciprocal_latt(lattice_params))

        hkl_values = [float(entry.text()) for entry in self.hkl_entries]
        v1 = hkl_values[0] * a_star_cartesian + hkl_values[2] * b_star_cartesian + hkl_values[4] * c_star_cartesian
        v2 = hkl_values[1] * a_star_cartesian + hkl_values[3] * b_star_cartesian + hkl_values[5] * c_star_cartesian

        angle = function.angle_between_vectors(v1, v2)
        self.result_text.append(f"Angle between {hkl_values[0],hkl_values[2],hkl_values[4]} and {hkl_values[1],hkl_values[3],hkl_values[5]} is: {angle:.2f} degrees")

    
    # Calculate Button 2 Click Event
    def calculate_button_click2(self):
        lattice_params = [float(entry.text()) for entry in self.lattice_params_entries]
        hkl_values = [float(entry.text()) for entry in self.hkl_entries_otherfun]
        wavelength_values = float(self.entry_A.text())
        d_hkl, two_theta = function.bragg_angle(hkl_values, lattice_params, wavelength_values)
        self.result_text2.append(f"({hkl_values[0]},{hkl_values[1]},{hkl_values[2]}):\n d-spacing: {d_hkl:.4f} Å\n 2θ angle: {two_theta:.2f} degrees\n")
  

    # Energy Conversion Button Click Event
    def convert_energy(self):
        ev_value = float(self.entry_ev.text())
        angstrom_value = function.ev_to_angstrom(ev_value)
        self.result_text3.append(f"{ev_value} eV is {angstrom_value:.4f} Å\n")

# Splash Screen Function
def show_splash_screen():
    # Load the splash screen image.
    pixmap = QPixmap("three_legged_horse.png")
    
    # Create a QSplashScreen object with the pixmap.
    splash = QSplashScreen(pixmap)
    splash.show()
    
    # Process events to ensure the splash screen is displayed.
    app.processEvents()

    # Create a QProgressBar to show a loading progress indicator.
    progress_bar = QProgressBar(splash)
    progress_bar.setMaximum(10)
    progress_bar.setGeometry(20, pixmap.height() - 40, pixmap.width(), 20)
    progress_bar.show()

    # Simulate a loading process with a progress bar.
    for i in range(1, 11):
        progress_bar.setValue(i)
        time.sleep(0.1)  # Pause for a short time to simulate loading.
        app.processEvents()  # Update the GUI to show the progress.

    # Return the splash screen object.
    return splash

# Main Execution
if __name__ == "__main__":
    # Create an instance of QApplication.
    app = QApplication(sys.argv)

    # Display the splash screen with a progress bar.
    splash = show_splash_screen()

    # Create an instance of the MainWindow class.
    window = MainWindow()
    window.show()  # Show the main window.

    # Close the splash screen once the main window is displayed.
    splash.finish(window)

    # Start the main event loop of the application.
    sys.exit(app.exec_())

