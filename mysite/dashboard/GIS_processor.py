import math


class GIS_processor:
    
    
    def __init__(self):
            
        self.NX = 149            ## X축 격자점 수
        self.NY = 253            ## Y축 격자점 수

        self.Re = 6371.00877     ##  지도반경
        self.grid = 5.0          ##  격자간격 (km)
        self.slat1 = 30.0        ##  표준위도 1
        self.slat2 = 60.0        ##  표준위도 2
        self.olon = 126.0        ##  기준점 경도
        self.olat = 38.0         ##  기준점 위도
        self.xo = 210 / self.grid     ##  기준점 X좌표
        self.yo = 675 / self.grid     ##  기준점 Y좌표
        self.first = 0
        self.PI = math.asin(1.0) * 2.0
        self.DEGRAD = self.PI/ 180.0
        self.RADDEG = 180.0 / self.PI

        self.re = self.Re / self.grid
        self.slat1 = self.slat1 * self.DEGRAD
        self.slat2 = self.slat2 * self.DEGRAD
        self.olon = self.olon * self.DEGRAD
        self.olat = self.olat * self.DEGRAD

        self.sn = math.tan(self.PI * 0.25 + self.slat2 * 0.5) / math.tan(self.PI * 0.25 + self.slat1 * 0.5)
        self.sn = math.log(math.cos(self.slat1) / math.cos(self.slat2)) / math.log(self.sn)
        self.sf = math.tan(self.PI * 0.25 + self.slat1 * 0.5)
        self.sf = math.pow(self.sf, self.sn) * math.cos(self.slat1) / self.sn
        self.ro = math.tan(self.PI * 0.25 + self.olat * 0.5)
        self.ro = self.re * self.sf / math.pow(self.ro, self.sn)
        self.first = 1


    def mapToGrid(self, lat, lon, code = 0 ):
        ra = math.tan(self.PI * 0.25 + lat * self.DEGRAD * 0.5)
        ra = self.re * self.sf / pow(ra, self.sn)
        theta = lon * self.DEGRAD - self.olon
        if theta > self.PI :
            theta -= 2.0 * self.PI
        if theta < -self.PI :
            theta += 2.0 * self.PI
        theta *= self.sn
        x = (ra * math.sin(theta)) + self.xo
        y = (self.ro - ra * math.cos(theta)) + self.yo
        x = int(x + 1.5)
        y = int(y + 1.5)
        return x, y

    def gridToMap(self, x, y, code = 1):
        x = x - 1
        y = y - 1
        xn = x - self.xo
        yn = self.ro - y + self.yo
        ra = math.sqrt(xn * xn + yn * yn)
        if self.sn < 0.0 :
            ra = -ra
        alat = math.pow((self.re * self.sf / ra), (1.0 / self.sn))
        alat = 2.0 * math.atan(alat) - self.PI * 0.5
        if math.fabs(xn) <= 0.0 :
            theta = 0.0
        else :
            if math.fabs(yn) <= 0.0 :
                theta = self.PI * 0.5
                if xn < 0.0 :
                    theta = -theta
            else :
                theta = math.atan2(xn, yn)
        alon = theta / self.sn + self.olon
        lat = alat * self.RADDEG
        lon = alon * self.RADDEG

        return lat, lon