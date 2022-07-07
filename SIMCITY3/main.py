import pygame
import sys
pygame.init()
screen=pygame.display.set_mode((900,600))
display=pygame.Surface((300,200))
clock=pygame.time.Clock()
sprite=pygame.image.load("sprite.png")
running=True
mousePos=(0,0)
clickR=None
def clip(surf,x,y,x_size,y_size):
    handel_surf=surf.copy()
    clipR=pygame.Rect(x,y,x_size,y_size)
    handel_surf.set_clip(clipR)
    image=surf.subsurface(handel_surf.get_clip())
    return image.copy()
class Font():
    def __init__(self,path):
        self.spacing=1
        self.character_order=["a","b","c","d","e","f","g","h","i","j","k","l","m",
                              "n","o","p","q","r","s","t","u","v","w","x","y","z",
                              "0","1","2","3","4","5","6","7","8","9"]
        font_image=path
        self.characters={}
        character_count=0
        for y in range(3):
            for x in range(12):
                char_img=clip(font_image,x*7,y*7,7,7)
                self.characters[self.character_order[character_count]]=char_img.copy()
                character_count+=1
                self.space_width=self.characters["a"].get_width()
    def render(self,text,loc):
        x_offset=0
        for char in text:
            if loc[0]=="M":
                loc=(350/2-len(text)*8/2,loc[1])
            if char!=" ":
                display.blit(self.characters[char],(loc[0]+x_offset,loc[1]))
                x_offset+=self.characters[char].get_width()+self.spacing
            else:x_offset+=self.space_width+self.spacing
font=clip(sprite,0,41,84,21)
font=Font(font)
def loadMap(path):
    f=open(path+".txt","r")
    data=f.read()
    f.close()
    data=data.split("\n")
    gameMap=[]
    for row in data:
        gameMap.append(list(row))
    return gameMap
gameMap = loadMap("map")
def messageBox(x,y,height,width,text):
    global clickR
    lT=0
    for i in range(width-2):
        display.blit(sprite,(x+8+i*8,y),(0,9,8,8))
        display.blit(sprite,(x+8+i*8,y+(height-1)*8),(9,9,8,8))
    for i in range(height-2):
        display.blit(sprite,(x,y+8+i*8),(18,9,8,8))
        display.blit(sprite,(x+(width-1)*8,y+8+i*8),(27,9,8,8))
        for j in range(width-2):
            display.blit(sprite,(x+j*8+8,y+i*8+8),(36,9,8,8))
    display.blit(sprite,(x,y),(0,18,8,8))
    display.blit(sprite,(x+(width-1)*8,y),(9,18,8,8))
    display.blit(sprite,(x,y+(height-1)*8),(18,18,8,8))
    display.blit(sprite,(x+(width-1)*8,y+(height-1)*8),(27,18,8,8))
    a=0
    for i in text:
        if type(i)==list:
            button=0
            for j in i:
                display.blit(sprite,(x+4+button*8,y+4+(lT)*8),(0,18,8,8))
                display.blit(sprite,(x+4+button*8,y+4+(lT)*8+8),(18,18,8,8))
                display.blit(sprite,(x+4+button*8+len(j)*8,y+4+(lT)*8),(9,18,8,8))
                display.blit(sprite,(x+4+button*8+len(j)*8,y+4+8+(lT)*8),(27,18,8,8))
                for k in range(len(j)-1):
                    display.blit(sprite,(x+4+button*8+k*8+8,y+4+(lT)*8),(0,9,8,8))
                    display.blit(sprite,(x+4+button*8+k*8+8,y+4+(lT)*8+8),(9,9,8,8))
                font.render(j,(x+4+4+button*8,y+4+4+(lT)*8))
                if (mousePos[0]//4*4)>=(x+4+button*8) and (mousePos[0]//4*4)<=(x+4+button*8+len(j)*8+4) and\
                   (mousePos[1]//4*4)>=(y+4+(lT)*8) and (mousePos[1]//4*4)<=(y+4+8+(lT)*8+4):
                    clickR=j
                button=button+len(j)+2
            lT+=2
        else:
            font.render(i,(x+4,y+a*8+4))
        lT+=1
        a+=1
def renderTile(Map,X,Y):
    y=0
    for row in Map:
        x=0
        for col in row:
            x+=8
        y+=8
while running:
    display.fill((100,200,60))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                if clickR=="yes":
                    clickR="startYes"
    mousePos=pygame.mouse.get_pos()
    mousePos=list(mousePos)
    mousePos[0]=mousePos[0]/3
    mousePos[1]=mousePos[1]/3
    if clickR!="startYes" and clickR!="happy":
        messageBox(100,50,7,13,["hello","do you want","to enter","this game",["yes","no"]])
    if clickR=="startYes":
        messageBox(0,0,20,20,["welcome",["happy","unhappy"]])
    pygame.draw.rect(display,(0,0,0),(mousePos[0]//4*4,mousePos[1]//4*4,4,4))
    pygame.display.update()
    screen.blit(pygame.transform.scale(display,(900,600)),(0,0))
    clock.tick(60)
