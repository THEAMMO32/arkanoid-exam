import math
import pygame


class AudioManager:
    """Процедурные звуки без внешних файлов."""

    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.sfx_volume = 0.45
        self.music_on = True
        self._sounds = {}
        self._build_sounds()
        self._music_started = False

    def _tone(self, freq, ms, volume=None):
        """Генерирует короткий синусоидальный сэмпл."""
        vol = self.sfx_volume if volume is None else volume
        rate = 44100
        n = int(rate * ms / 1000)
        buf = bytearray()
        for i in range(n):
            t = i / rate
            env = 1.0 - (i / n) * 0.35
            val = int(vol * 32767 * env * math.sin(2 * math.pi * freq * t))
            sample = val.to_bytes(2, 'little', signed=True)
            buf += sample + sample
        return pygame.mixer.Sound(buffer=bytes(buf))

    def _build_sounds(self):
        """Создаёт набор звуковых эффектов."""
        self._sounds['paddle'] = self._tone(440, 45)
        self._sounds['brick'] = self._tone(720, 35)
        self._sounds['brick_strong'] = self._tone(520, 50)
        self._sounds['life'] = self._tone(180, 280, 0.5)
        self._sounds['powerup'] = self._tone(880, 90)
        self._sounds['win'] = self._tone(660, 120)
        self._sounds['lose'] = self._tone(220, 200, 0.55)
        self._sounds['level'] = self._tone(550, 100)

    def _play(self, name):
        """Воспроизводит звук по имени."""
        snd = self._sounds.get(name)
        if snd:
            snd.play()

    def play_paddle(self):
        self._play('paddle')

    def play_brick(self, strong=False):
        self._play('brick_strong' if strong else 'brick')

    def play_life_lost(self):
        self._play('life')

    def play_powerup(self):
        self._play('powerup')

    def play_win(self):
        self._play('win')

    def play_lose(self):
        self._play('lose')

    def play_level(self):
        self._play('level')

    def start_music(self):
        """Запускает тихий фоновый гул (зацикленный низкий тон)."""
        if self._music_started or not self.music_on:
            return
        hum = self._tone(110, 4000, 0.08)
        self._music_channel = hum.play(loops=-1)
        self._music_started = True

    def pause_music(self):
        if self._music_started:
            pygame.mixer.pause()

    def resume_music(self):
        if self._music_started:
            pygame.mixer.unpause()
