import cv2
def responsive(img_src, numX, numY, saveIn):
    img = cv2.imread(img_src)
    size = img.shape
    rangeX, rangeY = int(size[1]/numX), int(size[0]/numY)
    setX, setY = 0, 0
    print('Manual Debugging (Save path) = ',saveIn)
    for x in range(numX):
        for y in range(numY):
            # fileName = img_src.split('.')[0]+'-Aidesign'+str(x)+str(y)+'.'+img_src.split('.')[-1]
            fileName = 'Aidesign-Splitter-'+str(x)+str(y)+'.'+img_src.split('.')[-1]
            print('Manual Debugging (File name)= ',fileName)
            croppedImage = img[setY:setY+rangeY, setX:setX+rangeX]
            # cv2.imshow(fileName,croppedImage)
            # cv2.waitKey(0)
            cv2.imwrite((saveIn+fileName),croppedImage)
            setY+=rangeY
        setY = 0
        setX+=rangeX
    


# responsive('13.jpg',3,2)