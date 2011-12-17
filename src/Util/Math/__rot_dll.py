from ctypes import CDLL, c_double, pointer, POINTER

mydll = CDLL("fast_rot.dll")

makeTables = False
if makeTables:
    mydll.makeTables()
    def rotateTable(ox, oy, px, py, theta):
        __c_ox.value = ox
        __c_px.value = px
        __c_oy.value = oy
        __c_py.value = py
        __c_theta.value = theta
        
        mydll.rotTable(__c_ox, __c_oy, __c_px, __c_py, __c_theta, __prx, __pry)
        return __rx.value, __ry.value

__c_ox = c_double()
__c_oy = c_double()
__c_px = c_double()
__c_py = c_double()
__c_theta = c_double()

__rx = c_double()
__ry = c_double()
__prx = pointer(__rx)
__pry = pointer(__ry)

def rotate(ox, oy, px, py, theta):
    __c_ox.value = ox
    __c_px.value = px
    __c_oy.value = oy
    __c_py.value = py
    __c_theta.value = theta
    
    mydll.rot(__c_ox, __c_oy, __c_px, __c_py, __c_theta, __prx, __pry)
    return __rx.value, __ry.value
    