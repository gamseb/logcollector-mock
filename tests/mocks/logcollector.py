import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QLineEdit,
    QPushButton, QTextEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QCheckBox, QMessageBox
)
from PyQt5.QtCore import QTimer

class MockLogCollectorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Log Collector')
        self.setGeometry(100, 100, 600, 600)

        # Layouts
        main_layout = QVBoxLayout()
        profile_layout = QHBoxLayout()
        age_layout = QHBoxLayout()
        log_type_layout = QHBoxLayout()
        save_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        log_panel_layout = QVBoxLayout()

        # Collection Profile
        profile_label = QLabel('Collection Profile:')
        self.collection_profile = QComboBox()
        self.collection_profile.addItems(['Default', 'All', 'None', 'Custom'])
        profile_layout.addWidget(profile_label)
        profile_layout.addWidget(self.collection_profile)

        # Logs Age Limit
        age_label = QLabel('Logs Age Limit [days]:')
        self.logs_age_limit = QComboBox()
        self.logs_age_limit.addItems(['1', '5', '30', '60'])
        age_layout.addWidget(age_label)
        age_layout.addWidget(self.logs_age_limit)

        # Log File Type
        log_type_label = QLabel('Log File Type:')
        self.log_file_type = QComboBox()
        self.log_file_type.addItems(['Filtered binary', 'Filtered XML'])
        log_type_layout.addWidget(log_type_label)
        log_type_layout.addWidget(self.log_file_type)

        # Save Location
        save_label = QLabel('Save Location:')
        self.save_location = QLineEdit()
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_save_location)
        self.save_location.textChanged.connect(self.check_save_location)
        save_layout.addWidget(save_label)
        save_layout.addWidget(self.save_location)
        save_layout.addWidget(self.browse_button)

        # Collect Button
        self.collect_button = QPushButton('Collect')
        self.collect_button.setEnabled(False)  # Initially disabled
        self.collect_button.clicked.connect(self.start_collection)
        button_layout.addWidget(self.collect_button)

        # Log Panel
        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        log_panel_layout.addWidget(self.log_panel)

        # Artifacts to collect
        artifacts_group = QGroupBox("Artifacts to collect")
        artifacts_layout = QGridLayout()

        self.artifacts_checkboxes = [
            QCheckBox('Running processes (open handles and loaded DLLs)'),
            QCheckBox('Drives info'),
            QCheckBox('Devices info'),
            QCheckBox('Services Registry key content'),
            QCheckBox('Network configuration'),
            QCheckBox('Winsock LSP catalog'),
            QCheckBox('WFP filters'),
            QCheckBox('Complete Windows Registry content'),
            QCheckBox('List of files in temporary directories'),
            QCheckBox('Windows scheduled tasks'),
            QCheckBox('WMI repository'),
            QCheckBox('Application event log'),
            QCheckBox('System event log'),
            QCheckBox('SetupAPI logs'),
            QCheckBox('Terminal services - LSM operational event log'),
            QCheckBox('WMI Activity operational event log'),
            QCheckBox('Drivers install logs')
        ]

        artifacts_labels = [
            "Windows Processes",
            "System Configuration",
            "Windows Logs"
        ]

        section_indices = [0, 1, 11]
        row = 0
        for i, checkbox in enumerate(self.artifacts_checkboxes):
            if i in section_indices:
                label = QLabel(artifacts_labels[section_indices.index(i)])
                artifacts_layout.addWidget(label, row, 0, 1, 2)
                row += 1
            artifacts_layout.addWidget(checkbox, row, 0, 1, 2)
            row += 1

        artifacts_group.setLayout(artifacts_layout)

        # Adding layouts to the main layout
        main_layout.addLayout(profile_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(artifacts_group)
        main_layout.addLayout(age_layout)
        main_layout.addLayout(log_type_layout)
        main_layout.addLayout(save_layout)
        main_layout.addLayout(log_panel_layout)

        self.setLayout(main_layout)

    def browse_save_location(self):
        save_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if save_path:
            self.save_location.setText(save_path)

    def check_save_location(self):
        if self.save_location.text():
            self.collect_button.setEnabled(True)
        else:
            self.collect_button.setEnabled(False)

    def start_collection(self):
        self.log_panel.append('Collection started...')
        self.collect_button.setText('Cancel')
        self.collect_button.clicked.disconnect()
        self.collect_button.clicked.connect(self.cancel_collection)
        # Mock collection logic here
        QTimer.singleShot(5000, self.complete_collection)

    def cancel_collection(self):
        self.log_panel.append('Collection cancelled.')
        self.collect_button.setText('Collect')
        self.collect_button.clicked.disconnect()
        self.collect_button.clicked.connect(self.start_collection)

    def complete_collection(self):
        if not self.collect_button.text() == 'Collect':
            self.log_panel.append(f'Collection complete. File saved at {self.save_location.text()}')
            self.collect_button.setText('Collect')
            self.collect_button.clicked.disconnect()
            self.collect_button.clicked.connect(self.start_collection)
            QMessageBox.information(self, 'Success', 'Collection complete!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MockLogCollectorApp()
    ex.show()
    sys.exit(app.exec_())
