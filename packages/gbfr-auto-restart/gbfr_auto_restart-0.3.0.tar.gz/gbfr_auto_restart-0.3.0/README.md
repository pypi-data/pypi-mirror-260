# gbfr-auto-restart

그랑블루 판타지 리링크 전투 자동 재시작 스크립트

## 다운로드

https://github.com/Bing-su/gbfr_auto_restart/releases/latest/download/gbfr_auto_restart.exe

## 작동원리

3초마다 `image` 폴더에 있는 이미지와 일치하는 부분을 모니터에서 찾으면

W, enter를 순서대로 누릅니다.

![image](https://i.imgur.com/grU522b.png)

찾는 이미지는 '아니요'에 커서가 올려져 있는 이미지로, '계속 도전하시겠습니까?' 이외에 다른 상황에도 동작하니 유의해주세요.

## 주의사항

1. 백그라운드에서 동작하지 않음
2. 주 모니터만 인식함
3. 바이러스로 인식될 가능성이 높음
4. windows에서만 동작함
5. 게임을 시작한 뒤, 한번이라도 키보드나 마우스를 게임 내에서 사용해야 하는 것 같음 (게임패드로만 플레이 했을 경우 동작하지 않았음)
6. 해상도 1080에서만 동작함

## 파이썬 사용법

```sh
python -m gbfr_auto_restart
```

또는 그냥

```sh
gbfr_auto_restart
```

## 기타

치트엔진을 사용한 nexusmod의 `https://www.nexusmods.com/granbluefantasyrelink/mods/84`가 더 유용할 수 있습니다.
