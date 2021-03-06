## 부족한 부분
* Q2에서 요구한 테스트 코드 작성이 미흡합니다.
* Alarm on/off 기능을 구현하지 못했습니다. 

## 안내 사항
* Point Definitions에서 포인트 획득/소모를 정의할 때 소모하는 경우에는 point field를 음수로 입력하셔야합니다. admin에 help_text로 남겨두었으나 혹시 몰라서 안내사항에 남깁니다.
* Admin에서 Point issueds로 들어가시면 포인트 통계를 확인할 수 있습니다.
* 댓글 Noti는 홈화면에서 알람버튼에 빨간색 점이 찍히는 것으로 확인할 수 있습니다.
* websocket connection healtch check하는 부분을 구현하지 않아서 connection이 끊어지는 경우에, 알람이 오지 않을 수 있습니다. 혹시 알람이 와야하는데 안오는 경우가 생긴다면 새로고침을 해주세요.

