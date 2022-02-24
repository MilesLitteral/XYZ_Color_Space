import math
import random
from PIL import Image
from collections import namedtuple
from enum import Enum, auto

XYZ = namedtuple('XYZ', 'x y z')
CIE = namedtuple('CIE', "l a b")
RGB = namedtuple('RGB', "r g b")

class GeneRender:
    def __init__(self, x=500, y=600):
        self.x = x
        self.y = y
        self.img = Image.new("RGB",(x, y), "black")
        
    def showRender(self):
        self.img.show()

    def finishRender(self) -> Image:
        return self.img
        
    def renderData(self, data, show: bool):
        self.img = Image.new("RGB",(self.x, self.y), data)
        self.finishRender()
        if show != True:
            return 
        else:
            self.showRender()

def dotprod(r, g, b):
    return (r + g + b) - 128

def getColorDeltaE(c1, c2):
    xyzC1 = rgbToXyz(c1)
    xyzC2 = rgbToXyz(c2)
    labC1 = xyzToCIELAB(xyzC1)
    labC2 = xyzToCIELAB(xyzC2)
    
    #Euclidian Distance between two points in 3D matrices
    deltaE = math.sqrt( pow(labC1.l - labC2.l, 2) + pow(labC1.a - labC2.a, 2) + pow(labC1.b - labC2.b, 2) )
    return deltaE


def rgbToXyz(c, radian):
    #See Also
    #https://www.falloutsoftware.com/tutorials/gl/normal-map.html
    
    r = c.r / 255.0; 
    g = c.g / 255.0; 
    b = c.b / 255.0
    
    if (r > 0.04045):
        r = pow(( (r + 0.055) / 1.055 ), 2.4)
    else:
        r /= 12.92
    
    if (g > 0.04045):
        g = pow(( (g + 0.055) / 1.055 ), 2.4)
    else:
        g /= 12.92
    
    if (b > 0.04045):
        b = pow(( (b + 0.055) / 1.055 ), 2.4)
    else:
        b /= 12.92
    
    r *= 100 
    g *= 100 
    b *= 100

    #Calibration for observer @2° with illumination = D65
    #0.0f - 1.0f
    #radian[0].x = 0.4124
    #radian[0].y = 0.3576
    #radian[0].z = 0.1805

    #radian[1].x =  0.2126 
    #radian[1].y =  0.7152
    #radian[1].z =  0.0722
    
    #radian[2].z =  0.0193
    #radian[2].z =  0.1192
    #radian[2].z =  0.9505
    
    x = r * radian[0].x + g * radian[0].y + b * radian[0].z
    y = r * radian[1].x + g * radian[1].y + b * radian[1].z
    z = r * radian[2].x + g * radian[2].y + b * radian[2].z
    
    print(f"Frag Stride: {1.0 / 255}")
    return XYZ(math.ceil(x), math.ceil(y), math.ceil(z))


def xyzToCIELAB(c):
    refX = 95.047 
    refY = 100.0 
    refZ = 108.883
    
    #References set at calibration for observer @2° with illumination = D65
    x = c.x / refX; y = c.y / refY; z = c.z / refZ
    
    if (x > 0.008856):
        x = pow(x, 1 / 3.0)
    else: 
        x = (7.787 * x) + (16.0 / 116.0)
    
    if (y > 0.008856):
        y = pow(y, 1 / 3.0)
    else:
        y = (7.787 * y) + (16.0 / 116.0)
    
    if (z > 0.008856):
        z = pow(z, 1 / 3.0)
    else:
        z = (7.787 * z) + (16.0 / 116.0)
    
    l = 116 * y - 16
    a = 500 * (x - y)
    b = 200 * (y - z)
    
    return CIE(math.ceil(l), math.ceil(a), math.ceil(b))

def main():
    radian = []

    for x in range(0, 3):
        radian.append(XYZ(random.random(), 1, 1))

    for x in range(0, 2):
        r = RGB(255, 0, 0)
        print(f"RGB Color Value {r}")
        xyz = rgbToXyz(r, radian) #xyzColor(100, 0, 255)
        normalVal = dotprod(xyz.x, xyz.y, xyz.z)
        print(f"XYZ Space Value {xyz}")
        print(f"Tangent Value: {abs(normalVal)}")
        print(f"CIE Color Value: {xyzToCIELAB(xyz)}")

        Renderer = GeneRender()
        Renderer.renderData(xyz, True)

main()
