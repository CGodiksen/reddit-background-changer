from settings import Settings

from PyQt5 import QtWidgets, uic


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

        # Load the UI Page.
        uic.loadUi("resources/settingsdialog.ui", self)

        # Loading the settings and writing them to their respective line edits.
        self.settings = Settings()
        self.clientIDLineEdit.setText(self.settings.client_id)
        self.clientSecretLineEdit.setText(self.settings.client_secret)
        self.userAgentLineEdit.setText(self.settings.user_agent)
        self.changeFrequencySpinBox.setValue(self.settings.change_frequency)

        # Saving the text in the line edits to the settings file when the user presses the "OK" button.
        self.accepted.connect(self.ok)

        # Reverting any changes if the user presses the "Cancel" button.
        self.rejected.connect(self.cancel)

    def ok(self):
        """Saving the text in the line edits to the settings file."""
        self.settings.client_id = self.clientIDLineEdit.text()
        self.settings.client_secret = self.clientSecretLineEdit.text()
        self.settings.user_agent = self.userAgentLineEdit.text()
        self.settings.change_frequency = self.changeFrequencySpinBox.value()

        self.settings.save_settings()

    def cancel(self):
        """Reverting the text in the line edits back to the initial text."""
        self.clientIDLineEdit.setText(self.settings.client_id)
        self.clientSecretLineEdit.setText(self.settings.client_secret)
        self.userAgentLineEdit.setText(self.settings.user_agent)
        self.changeFrequencySpinBox.setValue(self.settings.change_frequency)
