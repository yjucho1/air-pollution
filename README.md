Application for monitoring korea air pollution

[![Dashboard](http://img.youtube.com/vi/Xt-Yw83cv7E/0.jpg)](https://www.youtube.com/watch?v=Xt-Yw83cv7E&feature=youtu.be "Korea Air Pollution")

#### Preparations

It use [this open-api-service(data.go.kr)](https://www.data.go.kr/dataset/15000581/openapi.do). Therefore, you need "service key" for get response data.
Then, make 'secret.json' file in the project directory path.
Secret.json should look like below

```
{
  "SECRET_KEY": "your-django-secret-key",
  "OPEN_API_KEY": "open-api-service-key"
}
```

#### requirements

pip install below packages
* django
* django-leaflet
* django-geojson

#### Related Tools and Docs

* django : https://www.djangoproject.com/
* bootstrap : https://getbootstrap.com/
* charts.js : https://www.chartjs.org/
* leaflet.js : https://leafletjs.com/

* 공공데이터 포털 : https://www.data.go.kr/
* 한국환경공단_측정소정보 조회 서비스 : https://www.data.go.kr/dataset/15000660/openapi.do
* 한국환경공단_대기오염정보 조회 서비스 : https://www.data.go.kr/dataset/15000581/openapi.do