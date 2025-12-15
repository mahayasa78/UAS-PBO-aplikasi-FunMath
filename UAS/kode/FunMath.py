import tkinter as tk
import pygame
import random


# ===================== AUDIO MANAGER =====================
class AudioManager:
    """Mengatur audio aplikasi (encapsulation)"""

    def __init__(self):
        pygame.mixer.init()

        # Memuat suara efek
        self.__suara_benar = pygame.mixer.Sound("sounds/benar.mp3")
        self.__suara_salah = pygame.mixer.Sound("sounds/salah.mp3")

        # Memutar musik latar secara looping
        pygame.mixer.music.load("sounds/backsound 1.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def play_benar(self):
        self.__suara_benar.play()

    def play_salah(self):
        self.__suara_salah.play()

    @staticmethod
    def set_volume(value):
        pygame.mixer.music.set_volume(value)

    @staticmethod
    def toggle(status):
        if status:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()


# ===================== MODEL SOAL =====================
class Soal:
    """Menyimpan data soal dan jawaban (encapsulation)"""

    def __init__(self, pertanyaan, jawaban, tingkat):
        self.__pertanyaan = pertanyaan
        self.__jawaban = jawaban
        self.__tingkat = tingkat

    def get_pertanyaan(self):
        return self.__pertanyaan

    def get_jawaban(self):
        return self.__jawaban

    def cek_jawaban(self, user):
        return int(user) == self.__jawaban


# ===================== Inheritance & polymorphism =====================
class OperasiMatematika: #super class
    """Kelas dasar operasi matematika (polymorphism)"""

    def hitung(self, a, b):
        raise NotImplementedError


class Penjumlahan(OperasiMatematika): #sub class
    def hitung(self, a, b):
        return f"{a} + {b} = ?", a + b


class Pengurangan(OperasiMatematika): #sub class
    def hitung(self, a, b):
        return f"{max(a, b)} - {min(a, b)} = ?", abs(a - b)


class Perkalian(OperasiMatematika): #sub class
    def hitung(self, a, b):
        return f"{a} × {b} = ?", a * b


class Pembagian(OperasiMatematika): #sub class
    def hitung(self, a, b):
        return f"{a * b} ÷ {b} = ?", a


# ===================== GENERATOR SOAL =====================
class GeneratorSoal:
    """Membuat soal baru berdasarkan tingkat dan operasi"""

    batas_tingkat = {"Mudah": 10, "Sedang": 50, "Sulit": 100}

    def __init__(self, tingkat, operasi: OperasiMatematika):
        self.min = 1
        self.max = self.batas_tingkat[tingkat]
        self.operasi = operasi
        self.tingkat = tingkat

    def generate(self):
        a = random.randint(self.min, self.max)
        b = random.randint(self.min, self.max)
        teks, jawaban = self.operasi.hitung(a, b)
        return Soal(teks, jawaban, self.tingkat)


# ===================== STATISTIK PEMAIN =====================
class StatistikPemain:
    """Menyimpan statistik pemain (encapsulation)"""

    def __init__(self):
        self.__total = 0
        self.__benar = 0
        self.__salah = 0
        self.__skor = 0

    def benar(self):
        self.__benar += 1
        self.__total += 1
        self.__skor += 10

    def salah(self):
        self.__salah += 1
        self.__total += 1

    def reset(self):
        self.__benar = self.__salah = self.__total = self.__skor = 0

    def get_info(self):
        akurasi = (self.__benar / self.__total) * 100 if self.__total else 0
        return self.__skor, self.__benar, self.__salah, akurasi


# ===================== GUI APLIKASI =====================
class AplikasiMatematika:
    """Kelas utama GUI permainan matematika"""

    def __init__(self, root):
        self.root = root
        self.root.title("🎓 FUNMATH 🎓")
        self.root.geometry("750x550")
        self.root.minsize(720, 500)
        self.root.configure(bg="#E3F2FD")

        # Property aplikasi
        self.soal = None
        self.boleh_lanjut = False
        self.music_playing = True

        # Model
        self.statistik = StatistikPemain()
        self.audio = AudioManager()

        self.tingkat = tk.StringVar(value="Mudah")
        self.tipe_operasi = tk.StringVar(value="Penjumlahan")

        self.build_ui()
        self.update_stats()

    # ===================== USER INTERFACE =====================
    def build_ui(self):
        """Membangun antarmuka aplikasi"""

        header = tk.Label(
            self.root, text="🎓 Belajar Matematika Ceria 🎓",
            font=("Comic Sans MS", 24, "bold"), bg="#1976D2", fg="white", pady=10
        )
        header.pack(fill="x")

        main = tk.Frame(self.root, bg="#E3F2FD")
        main.pack(expand=True, fill="both")

        # LEFT PANEL
        left = tk.Frame(main, bg="#BBDEFB", width=130)
        left.pack(side="left", fill="y")

        tk.Label(left, text="🎵 Volume", font=("Arial", 10, "bold"), bg="#BBDEFB").pack(pady=10)

        volume_slider = tk.Scale(
            left, from_=100, to=0, orient="vertical",
            command=lambda v: AudioManager.set_volume(int(v) / 100),
            length=200, bg="#BBDEFB", highlightthickness=0
        )
        volume_slider.set(50)
        volume_slider.pack(pady=5)

        self.btn_music = tk.Button(
            left, text="Pause Musik", bg="#1565C0", fg="white", width=12,
            command=self.toggle_music
        )
        self.btn_music.pack(pady=10)

        # CENTER PANEL
        center = tk.Frame(main, bg="#E3F2FD")
        center.pack(expand=True, fill="both")

        top_controls = tk.Frame(center, bg="#E3F2FD")
        top_controls.pack(pady=10)

        tk.OptionMenu(top_controls, self.tipe_operasi,
                      "Penjumlahan", "Pengurangan", "Perkalian", "Pembagian").pack(side="left", padx=8)

        tk.OptionMenu(top_controls, self.tingkat,
                      "Mudah", "Sedang", "Sulit").pack(side="left", padx=8)

        self.label_soal = tk.Label(center, text="Klik Mulai untuk mulai",
                                   font=("Arial", 26, "bold"), bg="#E3F2FD")
        self.label_soal.pack(pady=20)

        self.entry = tk.Entry(center, font=("Arial", 22), width=6, justify="center")
        self.entry.pack()
        self.entry.bind("<Return>", lambda e: self.cek_jawaban())

        self.btn_next = tk.Button(center, text="Mulai", bg="#43A047", fg="white",
                                  font=("Arial", 14, "bold"), command=self.generate_soal)
        self.btn_next.pack(pady=10)

        tk.Button(center, text="Cek Jawaban", bg="#0288D1", fg="white",
                  font=("Arial", 13, "bold"), command=self.cek_jawaban).pack(pady=5)

        self.label_feedback = tk.Label(center, font=("Arial", 22, "bold"), bg="#E3F2FD")
        self.label_feedback.pack(pady=10)

        self.label_stats = tk.Label(center, font=("Arial", 14, "bold"), bg="#E3F2FD")
        self.label_stats.pack(pady=10)

        tk.Button(center, text="Reset Statistik", bg="#FB8C00", fg="white",
                  font=("Arial", 13, "bold"), command=self.reset_stats).pack(pady=10)

    # ===================== LOGIC =====================
    @staticmethod
    def buat_operasi(tipe):
        """Factory untuk menentukan operasi matematika"""
        mapping = {
            "Penjumlahan": Penjumlahan(),
            "Pengurangan": Pengurangan(),
            "Perkalian": Perkalian(),
            "Pembagian": Pembagian()
        }
        return mapping[tipe]

    def toggle_music(self):
        AudioManager.toggle(self.music_playing)
        self.btn_music.config(text="Play Musik" if self.music_playing else "Pause Musik")
        self.music_playing = not self.music_playing

    def generate_soal(self):
        operasi = self.buat_operasi(self.tipe_operasi.get())
        generator = GeneratorSoal(self.tingkat.get(), operasi)
        self.soal = generator.generate()

        self.label_soal.config(text=self.soal.get_pertanyaan())
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.label_feedback.config(text="")
        self.boleh_lanjut = False
        self.btn_next.config(text="Soal Selanjutnya")

    def cek_jawaban(self):
        if not self.soal:
            return

        if self.boleh_lanjut:
            self.generate_soal()
            return

        try:
            if self.soal.cek_jawaban(self.entry.get()):
                self.statistik.benar()
                self.audio.play_benar()
                self.label_feedback.config(text="✔ Benar!", fg="green")
            else:
                self.statistik.salah()
                self.audio.play_salah()
                self.label_feedback.config(text=f"✘ Salah! Jawaban: {self.soal.get_jawaban()}", fg="red")

            self.update_stats()
            self.boleh_lanjut = True

        except ValueError:
            self.label_feedback.config(text="⚠ Masukkan angka!", fg="orange")

    def update_stats(self):
        skor, benar, salah, akurasi = self.statistik.get_info()
        self.label_stats.config(
            text=f"Skor: {skor} | Benar: {benar} | Salah: {salah} | Akurasi: {akurasi:.1f}%"
        )

    def reset_stats(self):
        self.statistik.reset()
        self.update_stats()
        self.label_soal.config(text="Klik Mulai untuk mulai")
        self.label_feedback.config(text="")
        self.btn_next.config(text="Mulai")
        self.soal = None


# ===================== MAIN APP =====================
if __name__ == "__main__":
    root = tk.Tk()
    AplikasiMatematika(root)
    root.mainloop()
