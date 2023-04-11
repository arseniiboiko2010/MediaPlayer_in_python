import sys
import argparse
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QFileDialog
import vlc
from PyQt5.QtWidgets import QSizePolicy


class MediaPlayer(QWidget):

    def __init__(self, video_file):
        super().__init__()
        self.current_volume = 50  # set initial volume to 50%
        self.media_player = vlc.MediaPlayer()
        current_volume = self.media_player.audio_get_volume()
        new_volume = min(current_volume + 10, 100)
        self.media_player.audio_set_volume(new_volume)
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Медіаплеєр")
        self.layout = QVBoxLayout()
        self.media_player = vlc.MediaPlayer()
        self.media = vlc.Media(video_file)
        self.media_player.set_media(self.media)
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setLineWidth(2)
        self.frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.media_player.set_hwnd(self.frame.winId())
        self.media_player.play()
        self.time_up_button = QPushButton(">>", self)
        self.time_down_button = QPushButton("<<", self)
        self.volume_up_button = QPushButton("+", self)
        self.volume_down_button = QPushButton("-", self)
        self.open_button = QPushButton("Open", self)
        self.play_button = QPushButton("Play", self)
        self.pause_button = QPushButton("Pause", self)
        self.volume_up_button.setFixedSize(20, 20)
        self.volume_down_button.setFixedSize(20, 20)
        self.time_up_button.setFixedSize(20, 20)
        self.time_down_button.setFixedSize(20, 20)
        self.time_up_button.clicked.connect(self.time_up)
        self.time_down_button.clicked.connect(self.time_down)
        self.volume_up_button.clicked.connect(self.volume_up)
        self.volume_down_button.clicked.connect(self.volume_down)
        self.open_button.clicked.connect(self.open_media)
        self.play_button.clicked.connect(self.play_media)
        self.pause_button.clicked.connect(self.pause_media)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.time_down_button)
        hbox2.addWidget(self.time_up_button)
        hbox2.addWidget(self.volume_down_button)
        hbox2.addWidget(self.volume_up_button)
        self.layout.addLayout(hbox2)
        hbox = QHBoxLayout()
        hbox.addWidget(self.open_button)
        hbox.addWidget(self.play_button)
        hbox.addWidget(self.pause_button)
        self.layout.addLayout(hbox)
        self.layout.addWidget(self.frame)
        self.setLayout(self.layout)

    def open_media(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"Open Video File", "","Video Files (*.mp4 *.avi *.mkv *.mpeg *.mov)", options=options)
        if file_name:
            self.media = vlc.Media(file_name)
            self.media_player.set_media(self.media)
            self.media_player.play()
    def play_media(self):
        self.media_player.set_time(0)
    def pause_media(self):
        if self.media_player.is_playing():
            self.media_player.pause()
        else:
            self.media_player.play()
    def volume_up(self):
        new_volume = min(self.current_volume + 5, 100)
        self.media_player.audio_set_volume(new_volume)
        self.current_volume = new_volume
    def volume_down(self):
        new_volume = max(self.current_volume - 5, 0)
        self.media_player.audio_set_volume(new_volume)
        self.current_volume = new_volume
    def time_up(self):
        self.media_player.set_time(self.media_player.get_time() + 10000)
    def time_down(self):
        self.media_player.set_time(self.media_player.get_time() - 5000)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video_file', help='The path to the video file.')
    args = parser.parse_args()
    app = QApplication(sys.argv)
    window = MediaPlayer(args.video_file)
    window.show()
    sys.exit(app.exec_())
