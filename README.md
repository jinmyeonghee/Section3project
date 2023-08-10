# 카페 창업시 방문자수 예측
**프로젝트기간 : 2022.12.30 ~ 2023.01.04**

**사용 언어 : python**

**개발환경 : macOS Ventura 13.1, visual studio code**

**사용도구 : Selenium, postgreSQL, Metabase**

***
### 프로젝트 개요
- 카페창업시 도움이 될 수 있도록 별점(예상)과 카페위치로 방문자수를 예측해주는 프로젝트를 계획

### 프로젝트 배경
- 코로나 19이후 해외여행이 제한되면서 국내관광객수가 늘어나고, 특히 제주관광객수가 증가함에 따라 제주 내 카페 수가 급증. 

   
## 프로젝트 내용
### 1. 동적스크레이핑인 Selenium을 통해 카카오맵에서 데이터를 수집
<img width="360" alt="스크린샷 2023-08-10 오후 10 57 56" src="https://github.com/jinmyeonghee/Visitor_Prediction_ML/assets/114460314/be68b916-eb05-425a-abc4-fe6ce410b004">

### 2. 판다스를 이용해 데이터를 정제 한 후 데이터를 postgreSQL에 적재
<img width="483" alt="스크린샷 2023-08-10 오후 10 58 07" src="https://github.com/jinmyeonghee/Visitor_Prediction_ML/assets/114460314/642a4d4b-ec2b-4ee4-832c-b4104704dfdd">

### 3. 적재된 데이터를 이용해 다중선형회귀모델을 만들고, 플라스크를 통해 API구현

### 4. Metabase로 시각화
<img width="744" alt="스크린샷 2023-08-10 오후 10 58 29" src="https://github.com/jinmyeonghee/Visitor_Prediction_ML/assets/114460314/b2dd7835-680b-4397-8e41-00f4cc7f1eb8">

### 5. API 구현 및 평가
<img width="613" alt="스크린샷 2023-08-10 오후 10 58 52" src="https://github.com/jinmyeonghee/Visitor_Prediction_ML/assets/114460314/9a63e6f5-6552-4b17-bc46-945b264ed098">

### 프로젝트 평가
- 두번째 학습에서 데이터를 추가적으로 학습. 백그라운드 이미지를 활용.

  -> 해당 프로젝트는 클래스가 2개밖에 되지 않기때문에 confidence score가 (물체를 잡지 못 하는 것에 대해서) 학습이 잘 되지 않는 경우가 많은데, 백그라운드 이미지를 통해 어느 정도 학습할 수 있기 때문에 성능이 높아졌을 것으로 생각됩니다.

### 프로젝트 한계 및 개선방안
- 학습데이터에 <대형차>만 있었기때문에 소형차, 중형차에 대한 과적차량을 잘 인식하지 못함
  
  -> 소형차, 중형차도 같이 학습을 시키면 더 높은 성능을 낼 수 있을 것이다.
- 모델의 성능 평가 측면에서 클래스가 적으므로 mPA를 무조건적으로 신뢰할 수 없음
  
  -> 따라서 다양한 클래스 및 이미지를 추가하여 학습하는 것이 좋을 것이다.
