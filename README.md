# paper-crawling

DBpia 를 크롤링하는 파이썬 코드입니다.

특정 검색어와 연도 범위에 따라 나오는 학술저널과 학술대회자료 논문의 제목, 초록, 그리고 인용 키워드를 스크래핑하여 저장합니다.
초록이 한글로만 되어있거나 없는 경우, 그리고 키워드가 없는 경우는 저장하지 않습니다.

```shell
virtualvenv venv
source venv/bin/activate
pip3 install -r requirements.txt
sh run.sh
```

검색어와 연도 범위의 경우 `run.sh` 를 참고하여 수정하면 됩니다.
