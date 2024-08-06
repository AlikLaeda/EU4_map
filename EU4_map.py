from PIL import Image, ImageDraw
import tkinter as tk
import csv, json, os

# path_eu4 = 'F:\Games\Steam\steamapps\common\Europa Universalis IV'

def first_number(e):
    i = e.find(' - ')
    if i == -1:
        i = e.find('-')
        if i == -1:
            i = e.find(' ')
            if i == -1:
                i = 9999
    #print(i)
    return int(e[:i])

def sea_or_land(filename, number):
    global wastelands
    with open(filename, 'r') as f:
        str = f.read()
        if str.find('culture = ') == -1:
            if number in wastelands:
                return 2
            else:
                return 1
        else:
            return 0

def pixel(x,y,img):
    # map_x,map_y=img.size
    global dict_of_colours
    colour = img.getpixel((x, y))
    prov = dict_of_colours.get(colour)
    return (prov[1], prov[2])

def all_same(pixel, nx, ex, sx, wx):
    if pixel[0] != nx[0]:
        return False
    elif pixel[0] != ex[0]:
        return False
    elif pixel[0] != sx[0]:
        return False
    elif pixel[0] != wx[0]:  
        return False    
    else:
        return True

def all_no_land(pixel, nx, ex, sx, wx):
#    print(pixel, nx, ex, sx, wx)
    if (nx[0]==0) and (pixel[1] != nx[1]):
        return True
    elif (ex[0]==0) and (pixel[1] != ex[1]):
        return True
    elif (sx[0]==0) and (pixel[1] != sx[1]):
        return True
    elif (wx[0]==0) and (pixel[1] != wx[1]):  
        return True    
    else:
        return False


def other_land(pixel, nx, ex, sx, wx):
#    print(pixel, nx, ex, sx, wx)
    if (nx[0]==0) and (pixel[1] != nx[1]):
        return True
    elif (ex[0]==0) and (pixel[1] != ex[1]):
        return True
    # elif (sx[0]==0) and (pixel[1] != sx[1]):
    #     return True
    # elif (wx[0]==0) and (pixel[1] != wx[1]):  
    #     return True    
    else:
        return False

def other_wastland(pixel, nx, ex, sx, wx):
    if (nx[0]==2) and (pixel[1] != nx[1]):
        return True
    elif (ex[0]==2) and (pixel[1] != ex[1]):
        return True
    # elif (sx[0]==2) and (pixel[1] != sx[1]):
    #     return True
    # elif (wx[0]==2) and (pixel[1] != wx[1]):  
    #     return True    
    else:
        return False


def other_sea(pixel, nx, ex, sx, wx):
    if (nx[0]==1) and (pixel[1] != nx[1]):
        return True
    elif (ex[0]==1) and (pixel[1] != ex[1]):
        return True
    # elif (sx[0]==1) and (pixel[1] != sx[1]):
    #     return True
    # elif (wx[0]==1) and (pixel[1] != wx[1]):  
    #     return True    
    else:
        return False

def but01click():
    global path_eu4
    global ent01
    path_eu4 = ent01.get()
    with open("settings.json", "w", encoding="utf-8") as write_file:
        json.dump(path_eu4, write_file, ensure_ascii=False, indent='  ')    
    print("Сохранено")

def menu01click():
    global path_eu4
    global provinces
    global wastelands
    global dict_of_colours
    global lab02


    dict_of_provs = {}
# 
    for i in range(0, len(provinces)):
        dict_of_provs.update({provinces[i][0]: provinces[i][1:-2]})
        # provinces_i = provinces[i][:-2]
        # provinces.pop(i)
        # provinces.insert(i,provinces_i)
        
    
    list_of_files = os.listdir(path_eu4 + '\history\provinces')#[:200]
    list_of_files.sort(key=first_number)

    # print(list_of_files)
    dict_of_colours = {}
    for key, value in dict_of_provs.items():

        if len(list_of_files)==0:
            filename = ''
        else:
            filename = list_of_files.pop(0)
        if key == str(first_number(filename)):
            value.append(filename)
            value.append(sea_or_land(path_eu4 + '\history\provinces\\' + filename, key))
        else:
            list_of_files.insert(0, filename)
            value.append('')
            value.append(1)
        value.append(key)
        dict_of_colours.update({(int(value[0]),int(value[1]),int(value[2])): value[3:]})   

    dict_of_colours.update({(220, 54, 163): ['4759 - Oberkaernten.txt', 0, '4759']}) 
    dict_of_colours.update({(202, 50, 79): ['', 2, '1796']})     
    dict_of_colours.update({(238, 230, 38): ['', 2, '4763']}) 
    dict_of_colours.update({(18, 32, 192): ['128 - Karnten.txt', 0, '128']})

    # print(dict_of_colours)
    # for item in dict_of_provs.items():
    #     print(item)

#   У каждого пикселя проверяем его самого, а также справа, слева, сверху, снизу
#    Х
#   ХОХ
#    Х
#   Если он - море не из списка пустоши и рядом любые моря, то пиксель синий.
#   Если он - море и рядом хоть один пиксель суши или пустоши, то чёрный.
#   Если он - суша и рядом хоть один пиксель суши другой провинции, то чёрный. 
#
#
    # with Image.open('provinces mini.bmp') as base_map:
    with Image.open(path_eu4 + '\map\provinces.bmp') as base_map:
        base_map.load()
    map_x,map_y=base_map.size
    # print(map_x,map_y)
    # print(base_map.getpixel((100,100)))

    # print(base_map.getpixel((3000, 1300)),dict_of_provs.get('1796'))
    # print(base_map.getpixel((3000, 1300)),dict_of_provs.get('4763'))
    # print(base_map.getpixel((3000, 1300)),dict_of_provs.get('4759'))
    # print(base_map.getpixel((3000, 1300)),dict_of_provs.get('128'))




    new_map = Image.new ("P", (map_x,map_y), (255, 255, 255))
#    draw = ImageDraw.Draw(new_map)
    for x in range(0, map_x):
        lab02.config(text = str((100*x)//map_x) + '%')
        for y in range(0, map_y):
            if (x==0) or (y==0) or (x==map_x-1) or (y==map_y-1):
                new_map.putpixel( (x, y), (0, 0, 0) )
            else:
                pixel_x = pixel(x, y, base_map)
                pixel_nx = pixel(x, y-1, base_map)
                pixel_ex = pixel(x+1, y, base_map)
                pixel_sx = pixel(x, y+1, base_map)
                pixel_wx = pixel(x-1, y, base_map)
                if pixel_x[0] == 1:
                    if all_same(pixel_x, pixel_nx, pixel_ex, pixel_sx, pixel_wx):
                        new_map.putpixel( (x, y), (0, 127, 255) )
                    else:
                        new_map.putpixel( (x, y), (0, 0, 0) )
                elif pixel_x[0] == 2:
                    if all_no_land(pixel_x, pixel_nx, pixel_ex, pixel_sx, pixel_wx):
                        new_map.putpixel( (x, y), (0, 0, 0) )
                    else:
                        new_map.putpixel( (x, y), (128, 128, 128) )
                else:
                    if other_land(pixel_x, pixel_nx, pixel_ex, pixel_sx, pixel_wx):
                        new_map.putpixel( (x, y), (0, 0, 0) )





                # if all_same(pixel_x, pixel_nx, pixel_ex, pixel_sx, pixel_wx):
                #     if pixel_x[0] == 1:
                #         new_map.putpixel( (x, y), (0, 127, 255) )
                #     elif pixel_x[0] == 2:
                #         new_map.putpixel( (x, y), (127, 127, 127) )
                #     else:
                #         if other_land(pixel_x, pixel_nx, pixel_ex, pixel_sx, pixel_wx):


                
                
    #             if pixel(x, y, base_map):
    #                 new_map.putpixel( (x, y), (0, 127, 255) )
    new_map.show()




            
        

        




if __name__ == "__main__":
    root = tk.Tk()

    # Открываем файл с настройками (settings.json).
    # И записываем его содержимое в переменную
    with open("settings.json", "r", encoding="utf-8") as f:
        path_eu4 = json.load(f)

   # Открываем файл 
    with open(path_eu4 + '\map\definition.csv', newline='') as csvfile:
        provinces = list(csv.reader(csvfile, delimiter=';'))[1:]

   # Открываем файл 
    with open('Wastelands.csv', newline='') as csvfile:
        wastelands = list(csv.reader(csvfile, delimiter=';'))
        wastelands = list(map(lambda x: x[0], wastelands))




    # print(first_number('1110 - fds;gj.txt'))   
    # print(sea_or_land(path_eu4 + '\history\provinces\\1694 - Central Pacific 8.txt'))   

    # img = Image.new ("P", (300, 300), (255, 255, 255))
    # map_x,map_y=img.size
    # for x in range(0, map_x):
    #     for y in range(0, map_y):
    #         if x==y:
    #             img.putpixel( (x, y), (0, 128, 255) )
    # img.show()

    mainmenu = tk.Menu(root) 
    root.config(menu=mainmenu)
    mainmenu.add_command(label='Начать', command=menu01click)

    lab01 = tk.Label(text="Путь к EU4:")
    lab01.grid(row=0, column=0)
    
    lab02 = tk.Label(text="")
    lab02.grid(row=0, column=1)

    ent01 = tk.Entry(width=70)
    ent01.insert(1, path_eu4)
    ent01.grid(column=0, row=1)

    but01 = tk.Button(root, text='Клик', command=but01click) 
    but01.grid(column=0, row=2)

    butquit = tk.Button(root, text='Закрыть', command=root.destroy) 
    butquit.grid(column=1, row=2)

    root.mainloop()