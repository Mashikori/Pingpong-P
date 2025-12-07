import pygame  # import library pygame untuk membuat game
from pygame import sprite, key, display, image, transform, time, font  # import fungsi-fungsi penting dari pygame
from pygame.locals import *  # import semua konstanta event dan key
from pygame import mixer  # import mixer untuk suara
pygame.init()  # inisialisasi pygame

# ===============================
#   SOUND SETUP
# ===============================

mixer.init()  # inisialisasi mixer
mixer.music.load('Welcome Horizons.mp3')  # load musik latar
mixer.music.play(-1)  # mainkan musik secara loop

# ===============================
#   CLASS DEFINITIONS
# ===============================

class GameSprite(sprite.Sprite):  # class dasar semua objek dalam game
    def __init__(self, player_image, x, y, speed, width, height):  # constructor objek
        super().__init__()  # panggil constructor Sprite dari pygame
        self.image = transform.scale(image.load(player_image), (width, height))  # load gambar sprite dan ubah ukurannya
        self.speed = speed  # set kecepatan sprite
        self.rect = self.image.get_rect()  # ambil rectangle untuk posisi dan ukuran
        self.rect.x = x  # set posisi X sprite
        self.rect.y = y  # set posisi Y sprite

    def draw(self, surface):  # fungsi menggambar sprite ke layar
        surface.blit(self.image, (self.rect.x, self.rect.y))  # tampilkan gambar di posisi rect


class Player(GameSprite):  # class khusus untuk paddle pemain
    def update_right(self):  # update posisi paddle kanan berdasarkan input
        keys_pressed = key.get_pressed()  # ambil semua tombol yang ditekan
        if keys_pressed[K_UP] and self.rect.y > 5:  # naik
            self.rect.y -= self.speed  # geser paddle ke atas
        if keys_pressed[K_DOWN] and self.rect.y < win_height - 150:  # turun
            self.rect.y += self.speed  # geser paddle ke bawah

    def update_left(self):  # update posisi paddle kiri berdasarkan input
        keys_pressed = key.get_pressed()  # ambil semua tombol yang ditekan
        if keys_pressed[K_w] and self.rect.y > 5:  # naik
            self.rect.y -= self.speed  # geser paddle ke atas
        if keys_pressed[K_s] and self.rect.y < win_height - 150:  # turun
            self.rect.y += self.speed  # geser paddle ke bawah


# ===============================
#   GAME SETUP
# ===============================

win_width = 600  # lebar window game
win_height = 500  # tinggi window game
background_color = (110, 190, 255)  # warna latar belakang biru muda

window = display.set_mode((win_width, win_height))  # buat window dengan ukuran tertentu
display.set_caption("💥 Pong Battle Game by Fahri!")  # set judul window

clock = time.Clock()  # buat objek clock untuk mengatur FPS
FPS = 60  # set frame per second menjadi 60

# OBJECTS
racket1 = Player("racket.png", 30, 200, 6, 50, 150)  # buat paddle kiri dengan gambar, posisi, kecepatan, ukuran
racket2 = Player("racket.png", 520, 200, 6, 50, 150)  # buat paddle kanan dengan gambar, posisi, kecepatan, ukuran
ball = GameSprite("tenis_ball.png", win_width // 2 - 25, win_height // 2 - 25, 5, 50, 50)  # buat bola di tengah layar dengan kecepatan 5

font_big = font.Font(None, 60)  # font besar untuk teks akhir game
font_small = font.Font(None, 40)  # font kecil untuk skor dan pesan

score1 = 0  # skor awal player 1
score2 = 0  # skor awal player 2
max_score = 3  # skor maksimal normal sebelum dynamic rule berlaku

speed_x = 4  # kecepatan bola horizontal
speed_y = 4  # kecepatan bola vertikal

running = True  # flag loop utama game berjalan
finished = False  # flag game selesai atau tidak
show_message = ""  # variabel pesan yang ditampilkan di layar
message_timer = 0  # timer untuk durasi pesan selisih 1 poin


def reset_ball():  # fungsi untuk mereset posisi bola dan paddle setelah poin
    global speed_x, speed_y  # gunakan variabel global speed_x dan speed_y
    ball.rect.x = win_width // 2 - 25  # reset posisi X bola ke tengah
    ball.rect.y = win_height // 2 - 25  # reset posisi Y bola ke tengah
    speed_x = 4  # reset kecepatan horizontal bola
    speed_y = 4  # reset kecepatan vertikal bola
    racket1.rect.y = 200  # reset posisi paddle kiri
    racket2.rect.y = 200  # reset posisi paddle kanan


# ===============================
#   MAIN GAME LOOP
# ===============================

while running:  # loop utama game berjalan terus
    dt = clock.tick(FPS)  # dapatkan delta time (ms) untuk timer pesan

    for e in pygame.event.get():  # iterasi semua event yang terjadi
        if e.type == QUIT:  # jika event close window
            running = False  # hentikan loop utama
        if finished and e.type == KEYDOWN:  # jika game selesai dan tombol keyboard ditekan
            score1 = 0  # reset skor player 1
            score2 = 0  # reset skor player 2
            finished = False  # set game menjadi belum selesai
            show_message = ""  # hapus pesan
            message_timer = 0  # reset timer pesan
            reset_ball()  # reset posisi bola dan paddle

    if not finished:  # jika game belum selesai
        window.fill(background_color)  # isi background dengan warna biru muda

        racket1.update_left()  # update posisi paddle kiri berdasarkan WASD
        racket2.update_right()  # update posisi paddle kanan berdasarkan panah atas/bawah

        ball.rect.x += speed_x  # tambahkan kecepatan horizontal ke posisi bola
        ball.rect.y += speed_y  # tambahkan kecepatan vertikal ke posisi bola

        # Pantulan bola ketika terkena paddle kiri atau kanan
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1.05  # balik arah horizontal dan tambah kecepatan sedikit
            show_message = ""  # hapus pesan sementara untuk menampilkan lagi jika diperlukan
            message_timer = 0  # reset timer pesan

        # Pantulan bola atas dan bawah
        if ball.rect.y <= 0 or ball.rect.y >= win_height - 50:
            speed_y *= -1  # balik arah vertikal bola

        # Jika bola keluar kiri
        if ball.rect.x < 0:
            score2 += 1  # player 2 mendapat poin
            reset_ball()  # reset posisi bola dan paddle

        # Jika bola keluar kanan
        if ball.rect.x > win_width:
            score1 += 1  # player 1 mendapat poin
            reset_ball()  # reset posisi bola dan paddle

        # Dynamic win rule dengan timer
        if abs(score1 - score2) == 1 and (score1 >= 3 or score2 >= 3):  # jika selisih skor 1 dan salah satu >= 3
            target_score = 4  # target score dinaikkan
            if message_timer <= 0:  # jika timer habis
                show_message = "Karena selisih 1, skor maksimal jadi 4!"  # set pesan
                message_timer = 3000  # set timer 3 detik (ms)
        else:
            target_score = max_score  # target score normal
            show_message = ""  # hapus pesan

        if message_timer > 0:  # jika timer pesan aktif
            message_timer -= dt  # kurangi timer sesuai delta time
            if message_timer <= 0:
                show_message = ""  # hapus pesan setelah 3 detik

        # Cek pemenang
        if score1 >= target_score:
            finished = True  # set game selesai
            show_message = "PLAYER 1 MENANG!"  # tampilkan pesan menang
        if score2 >= target_score:
            finished = True  # set game selesai
            show_message = "PLAYER 2 MENANG!"  # tampilkan pesan menang

        # Gambar objek
        racket1.draw(window)  # gambar paddle kiri
        racket2.draw(window)  # gambar paddle kanan
        ball.draw(window)  # gambar bola

        # Gambar skor
        score_text = font_small.render(f"{score1} : {score2}", True, (0, 0, 0))  # buat teks skor
        window.blit(score_text, (260, 20))  # tampilkan teks skor

        # Tampilkan pesan dinamis jika ada
        if show_message and not finished:  # hanya jika game belum selesai
            msg = font_small.render(show_message, True, (255, 0, 0))  # render teks pesan
            window.blit(msg, (50, 450))  # tampilkan teks pesan

    else:  # jika game selesai
        window.fill((30, 30, 30))  # layar kemenangan gelap
        end_text = font_big.render(show_message, True, (255, 255, 255))  # teks kemenangan besar
        window.blit(end_text, (60, 200))  # tampilkan teks kemenangan

        replay_text = font_small.render("Tekan tombol apa saja untuk replay", True, (200, 200, 200))  # instruksi replay
        window.blit(replay_text, (100, 300))  # tampilkan instruksi replay

    display.update()  # update layar