from pygame.constants import QUIT, KEYDOWN, K_ESCAPE,K_UP,K_DOWN, K_LEFT, K_RIGHT, K_b, K_n
from pygame.display import flip, set_caption, set_mode
from pygame.event import Event, get, post
from pygame import Surface, Rect, init
from pygame.draw import line, rect
from pygame.font import SysFont
from numpy import sort, array, zeros, uint8, amax, amin, random, rot90, copy
from time import time
from random import choice


class Zaman(object):

    def __init__(self):self.sonZaman, self.hzm, self.hzmd = time() , 3, [0.5, 0.75, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]

    def zamanDurumu(self):
        if time() > self.sonZaman + (1 / self.hzmd[self.hzm]):
            self.sonZaman = time()
            return True
        return False

class Skor(object):
    # def __init__(self):self.skor, self.enYuksek = 0, 0
    def __init__(self):self.skor, self.enYuksek = 0, 37560

class Turler(object):

    def __init__(self, nesil):
        self.idt = random.randint(1,10000)
        self.a_bosSatir, self.a_maksYuk, self.a_minYuk, self.a_boslukSay, self.a_engebe = 0, 0, 0, 0, 0
        self.nesil = nesil
        self.skor = 0

    def __str__(self):return f'Skor: {self.skor}\nId :{self.idt}' + '\nBoş Satır  : %0.10f' % self.a_bosSatir + '\nMaks Yükseklik : %0.10f' % self.a_maksYuk + '\nToplam Yükseklik : %0.10f' % self.a_minYuk + '\nBoşluk Sayısı : %0.10f' % self.a_boslukSay + '\nEngebe : %0.10f' % self.a_engebe

    # def ilkTurler(self):
    #     self.a_bosSatir = random.random() - 0.5
    #     self.a_maksYuk = random.random() - 0.5
    #     self.a_minYuk = random.random() - 0.5
    #     self.a_boslukSay = random.random() - 0.5
    #     self.a_engebe = random.random() - 0.5

    def ilkTurler(self, gen, count):
        with open("veriler.csv", encoding='utf-8') as f_normal:
            datas = []
            lines = f_normal.readlines()
            for i in range(1,len(lines)):
                datas.append(lines[i].strip().split(','))
            self.idt = int(datas[gen*40+count][0])
            self.a_boslukSay = float(datas[gen*40+count][1])
            self.a_maksYuk = float(datas[gen*40+count][2])
            self.a_minYuk = float(datas[gen*40+count][3])
            self.a_engebe = float(datas[gen*40+count][4])
            self.a_bosSatir = float(datas[gen*40+count][5])
            self.skor = datas[gen*40+count][6]

    def caprazlama(self, ata1, ata2):
        self.a_bosSatir = choice([ata1.a_bosSatir, ata2.a_bosSatir])
        self.a_maksYuk = choice([ata1.a_maksYuk, ata2.a_maksYuk])
        self.a_minYuk = choice([ata1.a_minYuk, ata2.a_minYuk])
        self.a_boslukSay = choice([ata1.a_boslukSay, ata2.a_boslukSay])
        self.a_engebe = choice([ata1.a_engebe, ata2.a_engebe])

    def mutasyon(self):
        if random.random() < 0.5:self.a_bosSatir = self.a_bosSatir + 0.2 * (2 * random.random() - 1)
        if random.random() < 0.5:self.a_maksYuk = self.a_maksYuk + 0.2 * (2 * random.random() - 1)
        if random.random() < 0.5:self.a_minYuk = self.a_minYuk + 0.2 * (2 * random.random() - 1)
        if random.random() < 0.5:self.a_boslukSay = self.a_boslukSay + 0.2 * (2 * random.random() - 1)
        if random.random() < 0.5:self.a_engebe = self.a_engebe + 0.2 * (2 * random.random() - 1)

    __repr__ = __str__

class Nesil(object):

    def __init__(self, nesil):
        self.nesil, self.turler, self.elit = nesil, [], []
        for _ in range(40):self.turler.append(Turler(self.nesil))

    def ilkTurler(self, gen):
        for i in range(40):self.turler[i].ilkTurler(gen,i)

class Karo(object):

    def __init__(self, duzen, idt):
        self.duzen = array(duzen, dtype=uint8)
        self.idt = idt

class Populasyon(object):

    def __init__(self):
        # self.nesiller = [Nesil(0)]
        # for turler in self.nesiller[0].turler:turler.ilkTurler()

        self.nesiller = []
        for q in range(26):
            self.nesiller.append(Nesil(q))
            self.nesiller[q].ilkTurler(q)


    def sonrakiNesil(self):
        gn = len(self.nesiller)-1#Geçerli Nesil
        sn = gn + 1#Sonraki Nesil
        skorlar = sort(array([(i, self.nesiller[gn].turler[i].skor) for i in range(0,len(self.nesiller[gn].turler))], dtype=[('index', int), ('skor', int)]), order='skor')
        elit = list(reversed([x[0] for x in skorlar[30:40]]))
        self.nesiller[gn].elit = elit
        self.nesiller.append(Nesil(sn))
        for i in range(40):
            if i < 5:
                self.nesiller[sn].turler[i].caprazlama(self.nesiller[gn].turler[elit[i]], self.nesiller[gn].turler[elit[i]])
            else:
                ata1 = random.randint(10)
                ata2 = random.randint(10)
                self.nesiller[sn].turler[i].caprazlama(self.nesiller[gn].turler[elit[ata1]], self.nesiller[gn].turler[elit[ata2]])
            self.nesiller[sn].turler[i].mutasyon()


class Izgara(object):

    def __init__(self, skor:Skor):
        self.skor = skor
        self.izgara = zeros([10, 20], dtype=uint8)
        self.gercekHamle = True
        self.g_bosSatir = 0
        self.g_maksYuk = 0
        self.g_minYuk = 0
        self.g_engebe = 0
        self.g_boslukSay = 0

    def alanKontrol(self, pozX, pozY):
        if pozX < 0 or pozX > 9 or pozY > 19 or pozY < 0:
            return False
        if self.izgara[pozX, pozY] != 0:
            return False
        return True

    def tamSatSil(self):
        satirlar = 0
        for y in range(19, -1, -1):
            while amin(self.izgara.T[y]) != 0:
                satirlar += 1
                for y2 in range(y, 0, -1):
                    for x in range(10):
                        self.izgara[x, y2] = self.izgara[x, y2-1]
        self.g_bosSatir = satirlar
        yukseklik = []
        for sutun in self.izgara:
            c = 20
            for i in range(19, -1, -1):
                if sutun[i] != 0:
                    c = i
            yukseklik.append(20 - c)
        self.g_maksYuk = amax(yukseklik)
        self.g_minYuk = amin(yukseklik)
        self.g_engebe = 0
        for x in range(9):
            self.g_engebe += abs(yukseklik[x] + yukseklik[x-1])
        self.g_boslukSay = 0
        for x in range(10):
            for y in range(19, 1, -1):
                if self.izgara[x, y] == 0 and self.izgara[x, y-1] != 0:
                    self.g_boslukSay += 1
        if self.gercekHamle:
            self.skor.skor += [0, 40, 100, 300, 1200][satirlar]

    def oyunSonuKont(self):
        for y in range(4):
            if amax(self.izgara.T[y]) != 0:
                if self.gercekHamle:
                    self.izgara = zeros([10, 20], dtype=uint8)
                    if self.skor.skor > self.skor.enYuksek:self.skor.enYuksek = self.skor.skor
                    self.skor.skor = 0
                return True
        return False


class HareketliKaro(Karo):

    def __init__(self, duzen, idt, izgara:Izgara):
        Karo.__init__(self, duzen, idt)
        self.izgara = izgara
        self.pozX, self.pozY = 3, 0
        self.rot = random.randint(0, 4)

    def ArtX(self):
        for r in range(4):
            sonDurak = -1
            for c in range(4):
                if rot90(self.duzen, self.rot).T[r][c] == 1:sonDurak = c
            if sonDurak != -1:
                if not self.izgara.alanKontrol(self.pozX + sonDurak + 1, self.pozY + r):return False
        self.pozX += 1
        return True

    def EksX(self):
        for r in range(4):
            ilkDurak = -1
            for c in range(3, -1, -1):
                if rot90(self.duzen, self.rot).T[r][c] == 1:ilkDurak = c
            if ilkDurak != -1:
                if not self.izgara.alanKontrol(self.pozX + ilkDurak - 1, self.pozY + r):return False
        self.pozX -= 1
        return True

    def ArtY(self):
        for c in range(4):
            altDurak = -1
            for r in range(4):
                if rot90(self.duzen, self.rot)[c][r] == 1:altDurak = r
            if altDurak != -1:
                if not self.izgara.alanKontrol(self.pozX + c, self.pozY + altDurak + 1):return False
        self.pozY += 1
        return True

    def dondurme(self):
        for x in range(4):
            for y in range(4):
                if rot90(self.duzen, (self.rot + 1) % 4)[x, y] == 1:
                    if not self.izgara.alanKontrol(self.pozX + x, self.pozY + y):return False
        self.rot = (self.rot + 1) % 4
        return True

    def tarama(self):
        izgara = zeros([10, 20], dtype=uint8)
        for x in range(4):
            for y in range(4):
                if -1 < x+self.pozX < 10 and -1 < y+self.pozY < 20:izgara[x+self.pozX, y+self.pozY] = rot90(self.duzen, self.rot)[x, y] * self.idt
        return izgara

    def uygula(self):
        tarali = self.tarama()
        for x in range(10):
            for y in range(20):
                if tarali[x, y] != 0:
                    self.izgara.izgara[x, y] = self.idt
        self.izgara.tamSatSil()


class YapayZeka(object):

    def __init__(self, izgara:Izgara, skor:Skor):
        self.izgara = izgara
        self.skor = skor
        self.populasyon = Populasyon()
        # self.gecerliNesil = 0
        self.gecerliNesil = 25
        self.gecerliTurler = 0
        self.yedekIzgara = zeros([10, 20], dtype=uint8)
        self.yedekKaro = [0, 0, 0]

    def hamleYap(self, tile:HareketliKaro):
        self.yedekIzgara = copy(self.izgara.izgara)
        self.izgara.gercekHamle = False
        self.yedekKaro = [tile.pozX, tile.pozY, tile.rot]
        enIyiOran = -10000000000000
        enIyiHamle = 0
        enIyiRotasyon = 0
        for h in range(-5, 6):
            for r in range(0, 3):
                for i in range(0, r):tile.dondurme()
                if h < 0:
                    for i in range(0, -h):tile.EksX()
                if h > 0:
                    for i in range(0, h):tile.ArtX()
                while tile.ArtY():pass
                tile.uygula()
                self.izgara.tamSatSil()
                if self.hamleOranla()[0] > enIyiOran:
                    enIyiHamle = h
                    enIyiRotasyon = r
                    enIyiOran, oyunsonu = self.hamleOranla()
                tile.pozX, tile.pozY, tile.rot = self.yedekKaro
                self.izgara.izgara = copy(self.yedekIzgara)
        self.izgara.gercekHamle = True
        self.izgara.izgara = copy(self.yedekIzgara)
        if oyunsonu:
            self.populasyon.nesiller[self.gecerliNesil].turler[self.gecerliTurler].skor = self.skor.skor
            if self.gecerliTurler == 39:
                self.gecerliTurler = 0
                self.populasyon.sonrakiNesil()
                self.gecerliNesil += 1
            else:self.gecerliTurler += 1
        for i in range(0, enIyiRotasyon):tile.dondurme()
        if enIyiHamle < 0:
            for i in range(0, -enIyiHamle):tile.EksX()
        if enIyiHamle > 0:
            for i in range(0, enIyiHamle):tile.ArtX()
        while tile.ArtY():pass
        return enIyiHamle, enIyiRotasyon, enIyiOran

    def hamleOranla(self):
        oyunsonu = False
        gTurler: Turler = self.populasyon.nesiller[self.gecerliNesil].turler[self.gecerliTurler]
        oran = self.izgara.g_bosSatir * gTurler.a_bosSatir + self.izgara.g_maksYuk * gTurler.a_maksYuk + self.izgara.g_minYuk * gTurler.a_minYuk + self.izgara.g_boslukSay * gTurler.a_boslukSay + self.izgara.g_engebe * gTurler.a_engebe
        if self.izgara.oyunSonuKont():
            oran -= 500
            oyunsonu = True
        return oran, oyunsonu


class KaroKon(object):

    def __init__(self, izgara):
        self.izgara = izgara

    def rastgeleKaro(self):
        karo = [
            Karo([[1, 0, 0, 0], [1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]], 1),#T
            Karo([[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]], 2),#I
            Karo([[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 0, 0], [0, 0, 0, 0]], 3),#L
            Karo([[0, 1, 0, 0], [0, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]], 4),#L(Ters)
            Karo([[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]], 5),#O
            Karo([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]], 6),#Z
            Karo([[0, 0, 0, 0], [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]], 7) #Z(Ters)
        ][random.randint(0, 6)]
        return HareketliKaro(karo.duzen, karo.idt, self.izgara)


class Ekran(object):

    r1 = (24, 24, 24)#rgb(24,24,24)
    r2 = (0, 255, 255)#rgb(0,255,255)
    r3 = (0, 128, 255)#rgb(0,128,255)
    r4 = (0, 255, 128)#rgb(0,255,128)
    r5 = (255, 0, 255)#rgb(255,0,255)
    r6 = (255, 255, 0)#rgb(255,255,0)
    r7 = (128, 0, 255)#rgb(128,0,255)
    r8 = (255, 0, 128)#rgb(255,0,128)
    r9 = (255, 255, 255)#rgb(255,255,255)
    renkler = [r1, r2, r3, r4, r5, r6, r7, r8]

    def __init__(self, izgara:Izgara, zaman:Zaman, skor:Skor, ai:YapayZeka):
        self.izgara, self.zaman, self.skor, self.yz  = izgara, zaman, skor, ai
        self.durdur = False
        self.bilgiModu = 0
        self.pencere = [0, -1]
        self.ekran = set_mode((820, 720))
        set_caption("Tetris")
        init()
        self.buyukF = SysFont('Calibri', 60, True, False)
        self.ortaF = SysFont('Calibri', 24, True, False)
        self.kucukF = SysFont('Calibri', 17, True, False)
        self.statikGuncelle(True)

    def statikGuncelle(self, render = False):
        if not render:
            self.ekran.blit(self.statik, (0, 0))
            return
        statik = Surface((840, 720))
        statik.set_colorkey((0, 0, 0))
        statik.fill(self.r1)
        for i in range(10):
            line(statik, self.r9, (30 * i + 60, 60), (30 * i + 60, 660))
            line(statik, self.r9, (60, 30 * i + 60), (360, 30 * i + 60), 1 + 2 * (i == 4))
            line(statik, self.r9, (60, 30 * i + 390), (360, 30 * i + 390))
        line(statik, self.r9, (360, 60), (360, 660))
        line(statik, self.r9, (60, 360), (360, 360))
        for i in range(5):
            line(statik, self.r9, (480, 30 * i + 180), (600, 30 * i + 180))
            line(statik, self.r9, (30 * i + 480, 180), (30 * i + 480, 300))
        statik.blit(self.buyukF.render("Tetris", 2, self.r2), (615 - self.buyukF.size("Tetris")[0] / 2, 30))
        self.statik = statik

    def karoAyarlama(self, gKaro, sKaro):
        self.gKaro: HareketliKaro = gKaro
        self.sKaro: HareketliKaro = sKaro

    def tusKontrol(self):
        for eve in get():
            if eve.type == QUIT:self.durdur = True
            if eve.type == KEYDOWN:
                if eve.key == K_ESCAPE:post(Event(QUIT))
                if eve.key == K_b:self.bilgiModu = 0
                if eve.key == K_n:self.bilgiModu = 1
                if self.bilgiModu == 0:
                    if eve.key == K_UP:self.zaman.hzm = min(self.zaman.hzm+1, 14)
                    if eve.key == K_DOWN:self.zaman.hzm = max(self.zaman.hzm-1, 0)
                if self.bilgiModu == 1:
                    if eve.key == K_UP:self.pencere[1] = min(39, self.pencere[1]+1)
                    if eve.key == K_DOWN:self.pencere[1] = max(-1,self.pencere[1]-1)
                if eve.key == K_LEFT:self.pencere[0] = max(0, self.pencere[0]-1)
                if eve.key == K_RIGHT:self.pencere[0] = min(len(self.yz.populasyon.nesiller)-1, self.pencere[0]+1)

    def guncelle(self):
        self.tusKontrol()
        self.statikGuncelle()
        #Izgarayı Güncelleme
        izgara = self.izgara.izgara + self.gKaro.tarama()
        for x in range(10):
            for y in range(20):
                rect(self.ekran, self.renkler[izgara[x, y]], Rect(30 * x + 65, 30 * y + 65, 21, 21), 0)
        #Oyunu Güncelleme
        color = self.renkler[self.sKaro.idt]
        preview = rot90(self.sKaro.duzen, self.sKaro.rot)
        for x in range(4):
            for y in range(4):
                if preview[x, y] != 0:rect(self.ekran, color, Rect(30 * x + 485, 30 * y + 185, 21, 21),0)
        self.ekran.blit(self.ortaF.render(str(self.skor.skor), 2, self.r3), (780-self.ortaF.size(str(self.skor.skor))[0], 180))
        self.ekran.blit(self.ortaF.render(str(self.skor.enYuksek), 2, self.r4), (780-self.ortaF.size(str(self.skor.enYuksek))[0], 240))
        if self.bilgiModu == 0:
            self.ekran.blit(self.ortaF.render(f'{self.yz.gecerliNesil + 1}.Nesil', 2, self.r4), (540, 350))
            self.ekran.blit(self.ortaF.render(f'{self.yz.gecerliTurler + 1}.Tür', 2, self.r3), (640, 350))
            rect(self.ekran, self.r4, Rect(480, 410, 300, 30), 1)
            rect(self.ekran, self.r7, Rect(480, 410, min(300, 300 * (time() - self.zaman.sonZaman) / (1 / self.zaman.hzmd[self.zaman.hzm])), 30))
            self.ekran.blit(self.ortaF.render(f'{self.zaman.hzmd[self.zaman.hzm]}x', 2, self.r6), (590, 410))
        if self.bilgiModu == 1:
            self.ekran.blit(self.kucukF.render(f'{self.pencere[0]+1}.Nesil -> Tür {self.pencere[1]+1}', 2, self.r6), (480, 400))
            if self.pencere[1] == -1:
                for i in range(10):self.ekran.blit(self.kucukF.render(f'{i+1}:', 2, self.r7), (480, 450+15*i))
                for i in range(40):self.ekran.blit(self.kucukF.render(str(self.yz.populasyon.nesiller[self.pencere[0]].turler[i].skor), 2, self.r8), (515+75*int(i/10), 450+15*(i % 10)))
            if self.pencere[1] != -1:
                for i in range(len(str(self.yz.populasyon.nesiller[self.pencere[0]].turler[self.pencere[1]]).split('\n'))):self.ekran.blit(self.kucukF.render(str(self.yz.populasyon.nesiller[self.pencere[0]].turler[self.pencere[1]]).split('\n')[i], 2, self.r7), (480, 450+15*i))
        flip()


class Main():

    def __init__(self):
        self.skor  = Skor()
        self.izgara = Izgara(self.skor)
        self.karokon = KaroKon(self.izgara)
        self.yZ = YapayZeka(self.izgara, self.skor)
        self.zaman = Zaman()
        self.ekran = Ekran(self.izgara, self.zaman, self.skor, self.yZ)
        self.gKaro = self.karokon.rastgeleKaro()# Geçerli Karo,
        self.sKaro = self.karokon.rastgeleKaro()# Sonraki Karo
        self.ekran.karoAyarlama(self.gKaro, self.sKaro)
        self.startGame()

    def startGame(self):
        while not self.ekran.durdur:
            if self.zaman.zamanDurumu():
                self.yZ.hamleYap(self.gKaro)
                if not self.gKaro.ArtY():
                    self.gKaro.uygula()
                    if not self.izgara.oyunSonuKont():self.skor.skor += 10
                    self.gKaro = self.sKaro
                    self.sKaro = self.karokon.rastgeleKaro()
                    self.ekran.karoAyarlama(self.gKaro, self.sKaro)
            self.ekran.guncelle()

if __name__ == '__main__':Main()
