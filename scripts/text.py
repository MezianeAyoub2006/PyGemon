import nova_engine as nova, pygame, math

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
        self.game.freeze = True

    def render_text(self, begin,  lenght):
        first_line = (78, 288 + 75 - self.kill_count*30)
        second_line = (78, 315 + 75 - self.kill_count*30)
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
        if self.begin_count == 0:
            if self.remove :
                if self.kill_count > 0:
                    self.kill_count -= self.game.get_dt()/10
                else:
                    self.erased = True
                    self.game.freeze = False
            if self.c * 2 >= len(l_slice(list(self.text), 45)):
                self.remove = True
            elif self.count + self.game.get_dt()/1.7 < 90: 
                self.count += self.game.get_dt()/1.7
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.c += 1
                    self.count = 0
            self.game.draw(self.game.get_assets()["textbox"], (70, 283 + 75 - self.kill_count*30))
            self.render_text(90 * self.c, 90 * self.c + math.floor(self.count))
        else:
            self.game.draw(self.game.get_assets()["textbox"], (70, 283 + self.begin_count*30))
            self.begin_count -= self.game.get_dt()/10
            if self.begin_count <= 0:
                self.begin_count = 0


