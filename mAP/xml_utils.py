from xml.dom import minidom

def convert_bboxes(xml_path, new_txt_path):
    f = open(new_txt_path,"w")
    doc = minidom.parse(xml_path)
    clas = doc.getElementsByTagName("name")[0]
    #print(name.firstChild.data)
    objects = doc.getElementsByTagName("object")
    for object in objects:
        #sid = employee.getAttribute("id")
        clas = object.getElementsByTagName("name")[0]
        xmin = object.getElementsByTagName("xmin")[0]
        ymin = object.getElementsByTagName("ymin")[0]
        xmax = object.getElementsByTagName("xmax")[0]
        ymax = object.getElementsByTagName("ymax")[0]
        print("class:%s " % clas.firstChild.data)
        print("xmin:%s" % xmin.firstChild.data)
        print("ymin:%s" % ymin.firstChild.data)
        print("ymin:%s" % xmax.firstChild.data)
        print("ymax:%s" % ymax.firstChild.data)
        #clase = clas.firstChild.data
        #print(clase)
        clase = str(clas.firstChild.data)
        xmine = str(xmin.firstChild.data)
        ymine = str(ymin.firstChild.data)
        xmaxi = str(xmax.firstChild.data)
        ymaxi = str(ymax.firstChild.data)
        print(clase)
        print(f"1.0,{clas.firstChild.data},{xmin.firstChild.data},{ymin.firstChild.data},{xmax.firstChild.data},{ymax.firstChild.data}")
        #f.writelines(["\n1.0,{xmin.firstChild.data},{ymin.firstChild.data},{xmax.firstChild.data},{ymax.firstChild.data}"])
        #f.writelines("\n" + {clas.firstChild.data},",",{xmin.firstChild.data},",",{ymin.firstChild.data},",",{xmax.firstChild.data},",",{ymax.firstChild.data})
        f.write(clase +"," +"0.91" + "," + xmine + "," + ymine + "," + xmaxi + "," + ymaxi + "\n")
        #with open("1.txt","w") as txtfile:
        #    print("1.0,{}.format=(clas),{clas.firstChild.data},{xmin.firstChild.data},{ymin.firstChild.data},{xmax.firstChild.data},{ymax.firstChild.data}",file=txtfile)
        #linea = '"1.0",str((clas.firstChild.data)),{xmin.firstChild.data},{ymin.firstChild.data},{xmax.firstChild.data},{ymax.firstChild.data}'
        #f.write(linea)
    f.close()