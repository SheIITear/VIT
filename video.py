import re, os, cv2, math, sys
from PIL import Image

class colour:
    def __init__(self, r=None, g=None, b=None, a=None):
        self.r = round(r)
        self.g = round(g)
        self.b = round(b)

    def code(self):
        return u'\033[48;2;'+str(self.r)+';'+str(self.g)+';'+str(self.b)+'m'

class cell:
    def __init__(self, c='  ', colour=colour(200, 200, 200)):
        self.colour = colour
        self.c = c

    def rendered(self):
        return (u'\033[' + self.colour.code()) + self.c

class picture:
    def __init__(self, im):
        self.width = math.floor(75/2)
        self.height = math.floor(32)
        self.text = []
        px = im.load()
        for i in range(self.height):
            self.text.append([])
            for j in range(self.width):
                self.text[i].append(cell(colour=colour(*px[j*(im.width/self.width), i*(im.height/self.height)])))
        im.close()

    def rendered(self):
        string = ''
        for i in range(self.height):
            for j in range(self.width):
                string += self.text[i][j].rendered()
            string += u'\033[0m\n'
        return string[:-1]

if __name__ == '__main__':
    v = cv2.VideoCapture(sys.argv[2]) 
    cu = 0
    
    while(True): 
        ret,frame = v.read() 
        
        if ret: 
            name = sys.argv[1] + 'frame' + str(cu) + '.jpg'
            cu += 1
            cv2.imwrite(name, frame) 
            im = Image.open(name)
            c = picture(im)
            print(c.rendered()+"\n", end='', flush=False)
            os.remove(name)
        else: 
            break
    
    v.release() 
    cv2.destroyAllWindows()

def render(pa):
    im = Image.open(pa)
    return picture(im).rendered()
