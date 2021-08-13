# ベースイメージ
FROM python:3.9

# sqlite3のアップデート(仮想列に対応したバージョンにアップデート)
RUN mkdir /sqlite
WORKDIR /sqlite
RUN wget https://www.sqlite.org/2020/sqlite-autoconf-3310100.tar.gz && \
tar zxvf sqlite-autoconf-3310100.tar.gz && \
mv sqlite-autoconf-3310100 sqlite-3.31.01 && \
./sqlite-3.31.01/configure && \
make
ENV LD_LIBRARY_PATH /sqlite/.libs

RUN mkdir /var/www
WORKDIR /var/www

# 依存Pythonライブラリ一覧コピー
COPY requirements.txt ./
RUN pwd
# 依存Pythonライブラリインストール
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn","main:app", "--host", "0.0.0.0"]