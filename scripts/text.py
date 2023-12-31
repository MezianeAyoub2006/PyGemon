import nova_engine as nova, pygame, math

#Fonction qui divise une liste en n listes de count éléments (ex: l_slice([1,2,2,7,1,5,3], 3) renvoie [[1,2,2], [7,1,5], [3]])
def l_slice(chaine, count):
    if len(chaine) == count:
        return [chaine]
    c = 0
    rtrn = []
    l = []
    for i in range(len(chaine)):
        if c == count:
            rtrn.append(l)
            l = []
            c = 0
        l.append(chaine[i])
        c += 1
    if c != count:
        rtrn.append(l)
    return rtrn

#Système textuel
class TextBox(nova.Object):
    def __init__(self, text, game):
        nova.Object.__init__(self, game, (0,0), z_pos=10)
        self.game = game
        self.text = text
        self.count = 0
        self.c = 0
        self.kill_count = 2.5
        self.remove = False
        self.begin_count = 2.5
        self.click = False
        self.click_count = 0
        self.game.freeze = True

    def render_text(self, begin,  lenght):
        first_line = (78 - 64, 288 + 77 - self.kill_count*30)
        second_line = (78 - 64, 315 + 77 - self.kill_count*30)
        txt = self.text[begin:lenght]
        txts = ["".join(i) for i in l_slice(list(txt), 45)]
        if len(txts) == 1:
            self.game.render_text(txts[0], "main30", (0,0,0), first_line)
        elif len(txts) == 2:
            self.game.render_text(txts[0], "main30", (0,0,0), first_line)
            self.game.render_text(txts[1], "main30", (0,0,0), second_line)
        else:
            try:
                self.game.render_text(txts[self.c], "main30", (0,0,0), first_line)
                self.game.render_text(txts[self.c+1], "main30", (0,0,0), second_line)
            except IndexError:
                self.game.render_text(txts[self.c-1], "main30", (0,0,0), first_line)
                self.game.render_text(txts[self.c], "main30", (0,0,0), second_line)

    def render(self):
        self.click_count += self.game.get_dt()/60
        if self.click_count >= 0.3:
            self.click_count = 0
            self.click = not self.click
        if self.begin_count == 0:
            if self.remove :
                if self.kill_count > 0:
                    self.kill_count -= self.game.get_dt()/10
                else:
                    self.erased = True
                    self.game.freeze = False
            if self.c * 2 >= len(l_slice(list(self.text), 45)) or (self.count >= len(self.text) and pygame.key.get_pressed()[pygame.K_SPACE]):
                self.remove = True
            elif self.count + self.game.get_dt()/1.2 < 90: 
                self.count += self.game.get_dt()/1.2
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.c += 1 
                    self.count = 0

            self.game.draw(self.game.get_assets()["textbox"], (70 - 64, 283 + 77 - self.kill_count*30))
            self.render_text(90 * self.c, 90 * self.c + math.floor(self.count))

            if not self.count + self.game.get_dt()/1.2 < 90 or self.count >= len(self.text): 
                self.game.draw(self.game.get_assets()["textcursor"], (535 - 95, 320 + 77 - self.kill_count*30 - (2 if self.click else -2)))

        else:
            self.game.draw(self.game.get_assets()["textbox"], (70 - 64, 283 + 2 + self.begin_count*30))
            self.begin_count -= self.game.get_dt()/10
            if self.begin_count <= 0:
                self.begin_count = 0


