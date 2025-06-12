from xml.dom import minidom
import os

##########################################

# from CONSTANTS import 
DIR_PATH = os.path.join('.', 'frames') # CHANGE ACCORDINGLY

##########################################
# look-up table = map of class name<->label
# provided our own labels
LUT = {"EV": 0, "ICE": 1, "Other" : 2}

def convert_coordinates(size, box):
    dw = 1.0/size[0]
    dh = 1.0/size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1]-box[0]
    h = box[3]-box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_xml2yolo(file_path: str):
    fname_in = os.path.join(DIR_PATH, file_path)
    xmldoc = minidom.parse(fname_in)
    fname_out = os.path.join(DIR_PATH, (file_path[:-4]+'.txt'))

    with open(fname_out, "w") as f:

        itemlist = xmldoc.getElementsByTagName('object')
        size = xmldoc.getElementsByTagName('size')[0]
        width = int((size.getElementsByTagName('width')[0]).firstChild.data)
        height = int((size.getElementsByTagName('height')[0]).firstChild.data)

        for item in itemlist:
            classid =  (item.getElementsByTagName('name')[0]).firstChild.data
            if classid in LUT:
                label_str = str(LUT[classid])
            else:
                label_str = "-1"
                print ("warning: label '%s' not in look-up table" % classid)

            xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
            ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
            xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
            ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert_coordinates((width,height), b)

            f.write(label_str + " " + " ".join([("%.6f" % a) for a in bb]) + '\n')

    print ("%s" % fname_out)


if __name__ == '__main__':
    for path in os.listdir(DIR_PATH):
        if (path.endswith(".xml")):
            convert_xml2yolo(path)