/********************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <time.h>
#include <math.h>


#define NX  149     /* X축 격자점 수 */
#define NY  253     /* Y축 격자점 수 */


struct lamc_parameter {
	float  Re;          /* 사용할 지구반경 [ km ]      */
	float  grid;        /* 격자간격        [ km ]      */
	float  slat1;       /* 표준위도        [degree]    */
	float  slat2;       /* 표준위도        [degree]    */
	float  olon;        /* 기준점의 경도   [degree]    */
	float  olat;        /* 기준점의 위도   [degree]    */
	float  xo;          /* 기준점의 X좌표  [격자거리]  */
	float  yo;          /* 기준점의 Y좌표  [격자거리]  */
	int    first;       /* 시작여부 (0 = 시작)         */
};


/******************************************************************************
 *
*  MAIN
 *
 ******************************************************************************/
int main (int argc, char *argv[]) {
	float  lon, lat, x, y;
	struct lamc_parameter map;


	//
	// 인수 확인
	//


	if (argc != 4) {
		printf("[Usage] %s 1 <X-grid><Y-grid>\n", argv[0]);
		printf("        %s 0 <longitude><latitude>\n", argv[0]);
		exit(0);
	}


	if (atoi(argv[1]) == 1) {
		x = atof(argv[2]);
		y = atof(argv[3]);


		if (x < 1 || x > NX || y < 1 || y > NY) {
			printf("X-grid range [1,%d] / Y-grid range [1,%d]\n", NX, NY);
			exit(0);
		}
	} else if (atoi(argv[1]) == 0) {
		lon = atof(argv[2]);
		lat = atof(argv[3]);
	}


	//
	//  동네예보 지도 정보
	//


	map.Re    = 6371.00877;     // 지도반경
	map.grid  = 5.0;            // 격자간격 (km)
	map.slat1 = 30.0;           // 표준위도 1
	map.slat2 = 60.0;           // 표준위도 2
	map.olon  = 126.0;          // 기준점 경도
	map.olat  = 38.0;           // 기준점 위도
	map.xo    = 210/map.grid;   // 기준점 X좌표
	map.yo    = 675/map.grid;   // 기준점 Y좌표
	map.first = 0;


	//
	//  동네예보
	//


	map_conv(&lon, &lat, &x, &y, atoi(argv[1]), map);


	if (atoi(argv[1]))
		printf("X = %d, Y = %d  --->lon.= %f, lat.= %f\n", (int)x, (int)y, lon, lat);
	else
		printf("lon.= %f, lat.= %f ---> X = %d, Y = %d\n", lon, lat, (int)x, (int)y);


	return 0;
}


/*============================================================================*
 *  좌표변환
 *============================================================================*/
int map_conv
(
    float  *lon,                    // 경도(degree)
    float  *lat,                    // 위도(degree)
    float  *x,                      // X격자 (grid)
    float  *y,                      // Y격자 (grid)
    int    code,                    // 0 (격자->위경도), 1 (위경도->격자)
    struct lamc_parameter map       // 지도정보
) {
	float  lon1, lat1, x1, y1;


	//
	//  위경도 -> (X,Y)
	//


	if (code == 0) {
		lon1 = *lon;
		lat1 = *lat;
		lamcproj(&lon1, &lat1, &x1, &y1, 0, &map);
		*x = (int)(x1 + 1.5);
		*y = (int)(y1 + 1.5);
	}


	//
	//  (X,Y) -> 위경도
	//


	if (code == 1) {
		x1 = *x - 1;
		y1 = *y - 1;
		lamcproj(&lon1, &lat1, &x1, &y1, 1, &map);
		*lon = lon1;
		*lat = lat1;
	}
	return 0;
}


/***************************************************************************
*
*  [ Lambert Conformal Conic Projection ]
*
*      olon, lat : (longitude,latitude) at earth  [degree]
*      o x, y     : (x,y) cordinate in map  [grid]
*      o code = 0 : (lon,lat) --> (x,y)
*               1 : (x,y) --> (lon,lat)
*
***************************************************************************/


int lamcproj(lon, lat, x, y, code, map)


float  *lon, *lat;         /* Longitude, Latitude [degree]  */
float  *x, *y;             /* Coordinate in Map   [grid]    */
int    code;               /* (0) lon,lat ->x,y  (1) x,y ->lon,lat */
struct lamc_parameter *map;
{
	static double  PI, DEGRAD, RADDEG;
	static double  re, olon, olat, sn, sf, ro;
	double         slat1, slat2, alon, alat, xn, yn, ra, theta;


	if ((*map).first == 0) {
		PI = asin(1.0)*2.0;
		DEGRAD = PI/180.0;
		RADDEG = 180.0/PI;


		re = (*map).Re/(*map).grid;
		slat1 = (*map).slat1 * DEGRAD;
		slat2 = (*map).slat2 * DEGRAD;
		olon = (*map).olon * DEGRAD;
		olat = (*map).olat * DEGRAD;


		sn = tan(PI*0.25 + slat2*0.5)/tan(PI*0.25 + slat1*0.5);
		sn = log(cos(slat1)/cos(slat2))/log(sn);
		sf = tan(PI*0.25 + slat1*0.5);
		sf = pow(sf,sn)*cos(slat1)/sn;
		ro = tan(PI*0.25 + olat*0.5);
		ro = re*sf/pow(ro,sn);
		(*map).first = 1;
	}


	if (code == 0) {
		ra = tan(PI*0.25+(*lat)*DEGRAD*0.5);
		ra = re*sf/pow(ra,sn);
		theta = (*lon)*DEGRAD - olon;
		if (theta >  PI) theta -= 2.0*PI;
		if (theta < -PI) theta += 2.0*PI;
		theta *= sn;
		*x = (float)(ra*sin(theta)) + (*map).xo;
		*y = (float)(ro - ra*cos(theta)) + (*map).yo;
	} else {
		xn = *x - (*map).xo;
		yn = ro - *y + (*map).yo;
		ra = sqrt(xn*xn+yn*yn);
		if (sn< 0.0) -ra;
		alat = pow((re*sf/ra),(1.0/sn));
		alat = 2.0*atan(alat) - PI*0.5;
		if (fabs(xn) <= 0.0) {
			theta = 0.0;
		} else {
			if (fabs(yn) <= 0.0) {
				theta = PI*0.5;
				if(xn< 0.0 ) -theta;
			} else
				theta = atan2(xn,yn);
		}
		alon = theta/sn + olon;
		*lat = (float)(alat*RADDEG);
		*lon = (float)(alon*RADDEG);
	}
	return 0;
}
