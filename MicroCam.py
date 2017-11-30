from Tkinter import *                                                                       #
from PIL import Image, ImageTk                                                              #
import ttk, serial, os                                                                      #
import serial.tools.list_ports                                                              #

##------------------------------------------DEFS-------------------------------------------##
def Port_Authority():                                                                       #
    ports = list(serial.tools.list_ports.comports())                                        #
    for p in ports:                                                                         #
        if 'Arduino' in p[1]:                                                               #
            return p[0]                                                                     #

def go_send():                                                                              #
    xsteps = float(x.get())*5120
    xout = 'x:'+str(xsteps)                                                                     #
    ysteps = float(y.get())*5100    
    yout = 'y:'+str(ysteps)                                                                     #
    zsteps = float(z.get())*208000    
    zout = 'z:'+str(zsteps)                                                                     #
    speed = '@'+FREQ.get()                                                                  #
    print 'G,'+xout+','+yout+','+zout+','+speed                                             #
    ser.write('G,'+xout+','+yout+','+zout+','+speed)                                        #
    read_serial()                                                                           #

def initialize():                                                                           #
    global ser                                                                              #
    com = Port_Authority()                                                                  #
    try:                                                                                    #
        ser = serial.Serial(com,9600,timeout=.12)                                            #
    except serial.serialutil.SerialException:                                               #
        print 'error'                                                                       #

def check_serial():                                                                         #
    CONNEX.delete(0.0,END)                                                                  #
    try:                                                                                    #
        ser.read()                                                                          #
        CONNEX.insert(END, ser.port)                                                        #
    except serial.serialutil.SerialException:                                               #
        CONNEX.insert(END, 'ERROR')                                                         #
    master.after(1000, check_serial)                                                        #
    
def read_serial():                                                                          #
    data = ser.readline()                                                                   #
    if len(data) > 5:                                                                          #
        absolutes = data.split(',')                                                         #
        print absolutes                                                                     #
        XSHOW.delete(0.0,END)                                                               #
        XSHOW.insert(END,absolutes[0])                                                      #
        YSHOW.delete(0.0,END)                                                               #
        YSHOW.insert(END,absolutes[1])                                                      #
        ZSHOW.delete(0.0,END)                                                               #
        ZSHOW.insert(END,absolutes[2])                                                      #
        if absolutes[3] == 'c':                                                             #
            master.after(10, read_serial)                                                   #
        if absolutes[3] == 's':                                                             #
            return None                                                                     #
    else:                                                                                   #
        master.after(10, read_serial)
        print 'after'        #
    
def zero(coords):                                                                           #
    Z = 'Z'                                                                                 #
    for spec in coords:                                                                     #
        Z = Z+','+spec                                                                      #
    ser.write(Z)                                                                            #
    read_serial()                                                                           #

def home():                                                                                 #   
    ser.write('H')                                                                          #
    read_serial()                                                                           #
    
def pause():                                                                                #
    ser.write('P')                                                                          #
    read_serial()                                                                           #

def resume():                                                                               #
    ser.write('U')                                                                          #
    
def stop():                                                                                 #
    ser.write('S')                                                                          #  
    print 'stop'                                                                            #
    
def camera():                                                                               #
    ser.write('C')                                                                          #
    
panebg = 'light grey'                                                                       #
    
master = Tk()                                                                               #
master.title("Microscope Stage Controller")                                                 #
# master.geometry('%dx%d+%d+%d' % (570,300,-7,0))                                           #

key_flag = False                                                                            #

#------------------------------------------------------------------------------------------##

INFO = LabelFrame(master, text='Info', bg=panebg)                                           #
INFO.grid(row=0, column=0, rowspan=3,columnspan=5, sticky='WENS')                           #

Label(INFO, text='Conected on:', bg=panebg).grid(row=0,column=0, padx=10)                   #

CONNEX = Text(INFO, width=7, font=('TkDefaultFont',12), height=1)                           #
CONNEX.grid(row=0,column=1, padx=12 )                                                       #
initialize()                                                                                #
check_serial()                                                                              #

REINIT = Button(INFO, width=16, text='REINITIALIZE', command=initialize)                    #
REINIT.grid(row=1,column=0, columnspan=2, rowspan=2)                                        #

Label(INFO, text='X :', bg=panebg).grid(row=0, column=3, padx=12)                           #
Label(INFO, text='Y :', bg=panebg).grid(row=1, column=3, padx=12)                           #
Label(INFO, text='Z :', bg=panebg).grid(row=2, column=3, padx=12)                           #

XSHOW = Text(INFO,width=7, font=('TkDefaultFont',12), height=1)                             #
XSHOW.grid(row=0, column=4, padx=12, pady=5)                                                #
XSHOW.insert(0.0, '0')                                                                      #

YSHOW = Text(INFO, width=7, font=('TkDefaultFont',12), height=1)                            #
YSHOW.grid(row=1, column=4, padx=12, pady=5)                                                #
YSHOW.insert(0.0, '0')                                                                      #

ZSHOW = Text(INFO, width=7, font=('TkDefaultFont',12), height=1)                            #
ZSHOW.grid(row=2, column=4, padx=12, pady=5)                                                #
ZSHOW.insert(0.0, '0')                                                                      #

XZERO = Button(INFO, bg='palevioletred', text='Zero X', command=lambda:zero(('x')))         #
XZERO.grid(row=0, column=5, padx=12)                                                        #

YZERO = Button(INFO, bg='palevioletred', text = 'Zero Y', command=lambda:zero(('y')))       #
YZERO.grid(row=1, column=5, padx=12)                                                        #

ZZERO = Button(INFO, bg='palevioletred', text = 'Zero Z', command=lambda:zero(('z')))       #
ZZERO.grid(row=2, column=5, padx=12)                                                        #

AZERO = Button(INFO, width=4, height=8, bg='palevioletred', font=('TkDefaultFont',8),       #
               text='ZERO\n \nALL', wraplength=6, command=lambda:zero(('x','y','z')))       #
AZERO.grid(row=0, column=6, rowspan=3, padx=10, pady=10)                                    #

HOME = Button(INFO, width=12, height=7, text='HOME',bg='lightblue', command=home)           #
HOME.grid(row=0, column=7, rowspan=3, padx=12)                                              #

PAUSE = Button(INFO, width=12, height=3, text='PAUSE', bg='light goldenrod', command=pause) #
PAUSE.grid(row=0, column=8, rowspan=2, padx=12, pady=10, sticky='N')                        #

RESUME = Button(INFO, width=12, height=3, text='RESUME', bg='light green', command=resume)  #
RESUME.grid(row=1, column=8, rowspan=2, padx=12, pady=10, sticky='S')                       #

STOP = Button(INFO, width=12, height=7, text='STOP', bg='lightcoral', command=stop)         #
STOP.grid(row=0, column=9, rowspan=3, padx=12)                                              #    

#------------------------------------------------------------------------------------------##

NUM = LabelFrame(master, text='Numeric Control', bg=panebg)                                 #
NUM.grid(row=3,column=0,rowspan=2,columnspan=2, sticky='WENS')                              #

Label(NUM, height=1, width=20,text='X', bg=panebg).grid(column = 0, row=0)                  #
Label(NUM, height=1, width=20,text='Y', bg=panebg).grid(column = 1, row=0)                  #
Label(NUM, height=1, width=20,text='Z', bg=panebg).grid(column = 2, row=0)                  #
Label(NUM, height=1, width=20,text='Steps/s', bg=panebg).grid(column = 0, row=3)            #

x, y, z, freq = StringVar(), StringVar(), StringVar(), StringVar()                          #
x.set(0), y.set(0), z.set(0), freq.set(500)                                                 #

X = Entry(NUM, width=10, font=('TkDefaultFont',12), textvariable=x)                         #
X.grid(column=0, row=2)                                                                     #

Y = Entry(NUM, width=10, font=('TkDefaultFont',12), textvariable=y)                         #
Y.grid(column=1, row=2)                                                                     #

Z = Entry(NUM, width=10, font=('TkDefaultFont',12), textvariable=z)                         #
Z.grid(column=2, row=2)                                                                     #

FREQ = Entry(NUM, width=10, font=('TkDefaultFont',12), textvariable=freq)                   #
FREQ.grid(column=0, row=4)                                                                  #

G_SEND = Button(NUM, height=1, width=12, text='GO', bg='light green', command=go_send)      #
G_SEND.grid(column=2,row=4)                                                                 #

RAS = LabelFrame(master, text='Raster Controls', bg=panebg)                                 #
RAS.grid(row=5, column=0, rowspan=2, columnspan=2, sticky='WENS')                           #

def raster_send():                                                                          #
    wout = 'w:'+w.get()                                                                     #
    hout = 'h:'+h.get()                                                                     #
    dout = 'd:'+d.get()                                                                     #
    zspan = 't:'+t.get()                                                                    #
    zstep = 's:'+t.get()                                                                    #
    ser.write('R,'+wout+','+hout+','+dout+','+zspan+','+zstep)                              #
    read_serial()                                                                           #

Label(RAS, height=1, width=20, text='Width', bg=panebg).grid(column = 0, row=0)             #
Label(RAS, height=1, width=20, text='Height', bg=panebg).grid(column = 1, row=0)            #
Label(RAS, height=1, width=20, text='Step Size', bg=panebg).grid(column = 2, row=0)         #

w, h, d = StringVar(), StringVar(), StringVar()                                             #
w.set(0), h.set(0), d.set(0)                                                                #

W = Entry(RAS, width=10, font=('TkDefaultFont',12), textvariable=w)                         #
W.grid(column=0, row=1)                                                                     #

H = Entry(RAS, width=10, font=('TkDefaultFont',12), textvariable=h)                         #
H.grid(column=1, row=1)                                                                     #

D = Entry(RAS, width=10, font=('TkDefaultFont',12), textvariable=d)                         #
D.grid(column=2, row=1)                                                                     #

Label(RAS, height=1, width=20, text='Z-Travel', bg=panebg).grid(column = 0, row=2)          #
Label(RAS, height=1, width=20, text='Z-Step', bg=panebg).grid(column = 1, row=2)            #

t, s = StringVar(), StringVar()                                                             #
t.set(0), s.set(0)                                                                          #

ZT = Entry(RAS, width=10, font=('TkDefaultFont',12), textvariable=t)                        #
ZT.grid(column=0, row=3)                                                                    #

ZS = Entry(RAS, width=10, font=('TkDefaultFont',12), textvariable=s)                        #
ZS.grid(column=1, row=3)                                                                    #

R_SEND = Button(RAS, height=1, width=12, text='SCAN', bg='light green', command=raster_send)#
R_SEND.grid(column=2,row=3)                                                                 #

rates = {'Extra Low':'20',                                                                  #
         'Low':'100',                                                                       #
         'Medium':'150',                                                                    #
         'High':'250',                                                                      #
         'Extra High':'300'}                                                                #

def manual(event):                                                                          #
    man = str(event.widget).split('.')[-1]                                                  #
    rt = rate.get()                                                                         #
    ser.write('M,'+man+',@'+rates[rt])                                                      #

def end_manual(event):                                                                      #
    ser.write('S')                                                                          #
    read_serial()                                                                           #

def key(event):                                                                             #
    if keyboard.get() == 1:                                                                 #
        global key_flag                                                                     #
        if key_flag == False:                                                               #
            sym = event.keysym                                                              #
            key_dict[sym].event_generate('<Button-1>')                                      #
            key_dict[sym].event_generate('<Enter>')                                         #
            key_flag = True                                                                 #
        
def end_key(event):                                                                         #
    if keyboard.get() == 1:                                                                 #
        global key_flag                                                                     #
        sym = event.keysym                                                                  #
        key_dict[sym].event_generate('<ButtonRelease-1>')                                   #
        key_dict[sym].event_generate('<Leave>')                                             #
        key_dict[sym].config(relief=RAISED)                                                 #
        key_flag=False                                                                      #

#------------------------------------------------------------------------------------------##
        
CON = LabelFrame(master, text='Manual Adjustment', bg=panebg)                               #
CON.grid(row=3, column=2, rowspan=4, columnspan=2, sticky='WENS')                           #

Label(CON, text='Speed',  bg=panebg).grid(row=0,column=0,columnspan=3)                      #

rate = StringVar()                                                                          #
rate.set('Medium')                                                                          #
RATE = OptionMenu(CON, rate, 'Extra Low', 'Low', 'Medium', 'High', 'Extra High')            #
RATE.config(bd=2, width=20, bg='lemonchiffon')                                              #
RATE.grid(row=1, column=0, columnspan=3, pady=5)                                            #

EKC = Label(CON,text='Enable Keyboard Control', bg=panebg, wraplength=100)                  #
EKC.grid(row=0, column=4, columnspan=2, padx=5, sticky='W'+'E')                             #

keyboard = IntVar()                                                                         #
keyboard.set(0)                                                                             #
KBD = Checkbutton(CON,variable=keyboard, bg=panebg)                                         #
KBD.grid(row=1, column=4, columnspan=2)                                                     #

XYLABEL = Label(CON,text='X/Y', bg=panebg)                                                  #
XYLABEL.grid(row=4,column=1, sticky='EW')                                                   #

NORTH = Button(CON, width=3, font=('Courier',20,'bold'), fg='turquoise',                    #
               bg='dim grey', activebackground='grey', name='+y', text=u'\u25B2')           #
NORTH.grid(row=3, column=1, padx=5, pady=5)                                                 #
NORTH.bind('<Button-1>', manual)                                                            #
NORTH.bind('<ButtonRelease-1>', end_manual)                                                 #
master.bind('<Up>', key)                                                                    #
master.bind('<KeyRelease-Up>', end_key)                                                     #

SOUTH = Button(CON, width=3, font=('Courier',20,'bold'), fg='turquoise',                    #
               bg='dim grey', activebackground='grey', name='-y', text=u'\u25BC')           #
SOUTH.grid(row=5, column=1, padx=5, pady=5)                                                 #
SOUTH.bind('<Button-1>', manual)                                                            #
SOUTH.bind('<ButtonRelease-1>', end_manual)                                                 #
master.bind('<Down>', key)                                                                  #
master.bind('<KeyRelease-Down>', end_key)                                                   #

WEST = Button(CON, width=3, font=('Courier',20,'bold'), fg='RoyalBlue1',                    #
              bg='dim grey', activebackground='grey', name='-x', text=u'\u25C4')            #
WEST.grid(row=4, column=0, padx=5, pady=5)                                                  #
WEST.bind('<Button-1>', manual)                                                             #
WEST.bind('<ButtonRelease-1>', end_manual)                                                  #
master.bind('<Left>', key)                                                                  #
master.bind('<KeyRelease-Left>', end_key)                                                   #

EAST = Button(CON, width=3, font=('Courier',20,'bold'), fg='RoyalBlue1',                    #
              bg='dim grey', activebackground='grey', name='+x', text=u'\u25BA')            #
EAST.grid(row=4, column=2, padx=5, pady=5)                                                  #
EAST.bind('<Button-1>', manual)                                                             #
EAST.bind('<ButtonRelease-1>', end_manual)                                                  #
master.bind('<Right>', key)                                                                 #
master.bind('<KeyRelease-Right>', end_key)                                                  #

Delim2 = ttk.Separator(CON, orient=VERTICAL)                                                #
Delim2.grid(row=2,column=4, rowspan=4, sticky=NS, padx=5)                                   #

Delim3 = ttk.Separator(CON,orient=HORIZONTAL)                                               #
Delim3.grid(row=2, column=0, columnspan=6, sticky='NEW')                                    #

ZLABEL = Label(CON,text='Z', bg=panebg)                                                     #
ZLABEL.grid(row=4, column=3)                                                                #

UP = Button(CON, font=('Times',20,'bold'), fg='firebrick2',                                 #
            bg='dim grey', activebackground='grey', name='+z', text=u'\u2191')              #
UP.grid(row=3, column=3, padx=10, pady=5)                                                   #
UP.bind('<Button-1>', manual)                                                               #
UP.bind('<ButtonRelease-1>', end_manual)                                                    #
master.bind('<Prior>', key)                                                                 #
master.bind('<KeyRelease-Prior>', end_key)                                                  #

DOWN = Button(CON, font=('Times',20,'bold'), fg='firebrick2',                               #
              bg='dim grey', activebackground='grey', name='-z', text=u'\u2193')            #
DOWN.grid(row=5, column=3, padx=10, pady=5)                                                 #
DOWN.bind('<Button-1>', manual)                                                             #
DOWN.bind('<ButtonRelease-1>', end_manual)                                                  #
master.bind('<Next>', key)                                                                  #
master.bind('<KeyRelease-Next>', end_key)                                                   #

shutter = ImageTk.PhotoImage(file='C:\\Users\\Tyler\\Desktop\\cam.ico')                     #
CAM = Button(CON, width=70, height=128, image=shutter, bg='purple', command=camera)         #
CAM.grid(row=3, column=5, rowspan=3, padx=5, sticky='W')                                    #

key_dict={'Left':WEST,'Right':EAST,'Down':SOUTH,'Up':NORTH,'Prior':UP,'Next':DOWN}          #

master.mainloop()                                                                           #