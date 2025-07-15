import sys
import subprocess
import os
import signal
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QPushButton,
                             QLabel, QCheckBox, QComboBox, QLineEdit, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt

class KoohaStyleRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kooha‑Style Screen Recorder")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(700, 55)
        screen_geometry = QApplication.primaryScreen().geometry()
        x = int((screen_geometry.width() - self.width()) / 2)
        self.move(x, 0)
        self.setStyleSheet("background-color: rgba(40,40,40,150); border-radius: 20px;")

        self.recording = False
        self.paused = False
        self.process = None
        self.output_file = None

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 5, 10, 5)

        transparent_style = "background: transparent; color: white; border: none; font-size: 14px;"

        self.label = QLabel("🎥 Ready")
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; color:white; background: transparent;")
        layout.addWidget(self.label)

        self.start_btn = QPushButton("▶ Start")
        self.start_btn.setStyleSheet("background-color:#28a745; color:white; padding:6px; font-size:14px; border-radius:8px;")
        self.start_btn.clicked.connect(self.start_recording)
        layout.addWidget(self.start_btn)

        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.setStyleSheet("background-color:#ffc107; color:white; padding:6px; font-size:14px; border-radius:8px;")
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setEnabled(False)
        layout.addWidget(self.pause_btn)

        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setStyleSheet("background-color:#dc3545; color:white; padding:6px; font-size:14px; border-radius:8px;")
        self.stop_btn.clicked.connect(self.stop_recording)
        self.stop_btn.setEnabled(False)
        layout.addWidget(self.stop_btn)

        self.audio_checkbox = QCheckBox("Audio")
        self.audio_checkbox.setStyleSheet(transparent_style)
        self.audio_checkbox.setChecked(True)
        layout.addWidget(self.audio_checkbox)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp4", "mkv", "webm"])
        self.format_combo.setStyleSheet("background: transparent; color:white; border:none; font-size:14px;")
        layout.addWidget(self.format_combo)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Save directory")
        self.path_input.setStyleSheet("background: transparent; color:white; border:none; font-size:14px; padding:2px;")
        layout.addWidget(self.path_input)

        browse_btn = QPushButton("📁")
        browse_btn.setStyleSheet(transparent_style)
        browse_btn.clicked.connect(self.browse_dir)
        layout.addWidget(browse_btn)

        close_btn = QPushButton("✖")
        close_btn.setStyleSheet(transparent_style)
        close_btn.clicked.connect(self.quit_app)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def quit_app(self):
        if self.recording and self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception as e:
                print(f"Error stopping process: {e}")
        QApplication.quit()

    def closeEvent(self, event):
        self.quit_app()
        event.accept()

    def browse_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose Save Directory")
        if directory:
            self.path_input.setText(directory)

    def start_recording(self):
        if self.recording:
            QMessageBox.warning(self, "Warning", "Already recording!")
            return

        save_dir = self.path_input.text().strip()
        if not save_dir:
            QMessageBox.warning(self, "Warning", "Please choose a save directory.")
            return

        fmt = self.format_combo.currentText()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = os.path.join(save_dir, f"recording_{timestamp}.{fmt}")

        audio_opts = []
        if self.audio_checkbox.isChecked():
            audio_opts = ["-f", "pulse", "-i", "default"]

        screen = QApplication.primaryScreen().geometry()
        cmd = [
            "ffmpeg", "-y",
            "-f", "x11grab", "-video_size", f"{screen.width()}x{screen.height()}", "-i", ":0.0",
            *audio_opts,
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-r", "30",
            self.output_file
        ]

        try:
            self.process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start recording: {e}")
            return

        self.recording = True
        self.paused = False
        self.label.setText("⏺ Recording…")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.pause_btn.setEnabled(True)

    def toggle_pause(self):
        if not self.recording or not self.process:
            return
        try:
            if not self.paused:
                os.kill(self.process.pid, signal.SIGSTOP)
                self.paused = True
                self.pause_btn.setText("▶ Resume")
                self.label.setText("⏸ Paused")
            else:
                os.kill(self.process.pid, signal.SIGCONT)
                self.paused = False
                self.pause_btn.setText("⏸ Pause")
                self.label.setText("⏺ Recording…")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Pause/Resume failed: {e}")

    def stop_recording(self):
        if not self.recording:
            return
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to stop recording: {e}")
        self.process = None
        self.recording = False
        self.paused = False
        self.label.setText("✅ Saved")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setText("⏸ Pause")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = KoohaStyleRecorder()
    win.show()
    sys.exit(app.exec())
    sys.exit(app.exec())
