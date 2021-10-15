<template>
  <div class="questions container">
    <h1>よくある質問</h1><br>

  <div class="cp_qa">
    <div class="cp_actab">
      <input id="cp_tabfour031" type="checkbox" name="tabs">
      <label for="cp_tabfour031">ツイートしたのに集計されていません</label>
      <div class="cp_actab-content">
      <p>集計が行われない原因として、以下の5つが考えられます。 DMにて、集計されなかった旨ご連絡いただければ、個別に対応いたします。
        <ol>
          <li>タグの付け忘れ<br><b>#リングフィットアドベンチャー</b> のタグを付けた上で、ツイートを投稿してください。
</li>
          <li>画像のサイズや種類が異なる<br><b>本日の運動結果</b> のスクリーンショットを投稿してください。そのほかの画像は読み取れません。<br>
また、画像の大きさは1280x720でないと、読み取れません。<br>
Switchから直接投稿すれば、正しく読み取れるはずですが、画像をスマホに移した場合等に、画像サイズが縮小されるケースがありますので、ご確認ください。</li>
          <li>鍵アカウントである<br>鍵アカウントは集計の対象外になります。</li>
          <li>シャドウバンにより、集計から除外されている<br>Twitterでは検索結果から不適切なアカウント・ツイートを除外するアルゴリズムがあります。<br>
          この仕組みはシャドウバンと呼ばれ、シャドウバンされると検索結果に反映されなくなり、
          集計されなくなってしまいます。 シャドウバンされているかどうかは<a href="https://shadowban.eu/">shadowban.eu</a>でご確認ください。</li>
          <li>RingFitRankerのバグ・不具合<br>上記に当てはまらない場合、RingFitRankerが不具合を起こしている可能性があります。ぜひともDMにてお知らせください。</li>
        </ol></p>
      </div>
    </div>
    <div class="cp_actab">
      <input id="cp_tabfour032" type="checkbox" name="tabs">
      <label for="cp_tabfour032">鍵アカウントはランキング集計の対象になりますか？</label>
      <div class="cp_actab-content">
      <p>鍵アカウントは、集計・リプライの対象にはなりません。</p>
      </div>
    </div>
    <div class="cp_actab">
      <input id="cp_tabfour033" type="checkbox" name="tabs">
      <label for="cp_tabfour033">Twitterのユーザ名を変更すると、今までの運動記録はリセットされますか？</label>
      <div class="cp_actab-content">
      <p>@以下のユーザ名を変えると、リセットされます。
名前を変えただけなら、リセットはされません。</p>
      </div>
    </div>
    <div class="cp_actab">
      <input id="cp_tabfour034" type="checkbox" name="tabs">
      <label for="cp_tabfour034">リプライ時の順位と、TOP10発表時の順位が異なるのはなぜですか？</label>
      <div class="cp_actab-content">
      <p>リプライ時の順位はフォロワー外含んだ全数の集計になっていて、 TOP10の発表はフォロワー限定になっています。</p>
      </div>
    </div>
    <div class="cp_actab">
      <input id="cp_tabfour035" type="checkbox" name="tabs">
      <label for="cp_tabfour035">TOP10発表時に、消費カロリーが同率の場合、どのように順位がつきますか？</label>
      <div class="cp_actab-content">
      <p>より早くツイートをした方が、上位になります。</p>
      </div>
    </div>
    <div class="cp_actab">
      <input id="cp_tabfour036" type="checkbox" name="tabs">
      <label for="cp_tabfour036">機能を追加してほしい。改善してほしい。</label>
      <div class="cp_actab-content">
      <p>TwitterアカウントのDMからお問い合わせください。</p>
      </div>
    </div>
  </div>

  </div>
</template>

<style type="text/css">
  .cp_qa *, .cp_qa *:after, .cp_qa *:before {
    -webkit-box-sizing: border-box;
            box-sizing: border-box;
  }
  .cp_qa .cp_actab {
    position: relative;
    overflow: hidden;
    width: 100%;
    margin: 0 0 1em 0;
    color: #1b2538;
  }
  .cp_qa .cp_actab input {
    position: absolute;
    opacity: 0;
  }
  /* 質問 */
  .cp_qa .cp_actab label {
    font-weight: bold;
    line-height: 1.6em;
    position: relative;
    display: block;
    margin: 0 0 0 0;
    padding: 1em 2em 1em 2.5em;
    cursor: pointer;
    text-indent: 1em;
    border-radius: 0.5em;
    background: rgba(27,37,56,0.1);
  }
  .cp_qa .cp_actab label::before {
    font-family: serif;
    font-size: 1.5em;
    margin-left: -2em;
    padding-right: 0.5em;
    content: 'Q';
  }
  .cp_qa .cp_actab label:hover {
    transition: all 0.3s;
    color: #00838f;
  }
  /* --質問の＋アイコン */
  .cp_qa .cp_actab label::after {
    font-size: 1.7em;
    font-weight: bold;
    line-height: 2em;
    position: absolute;
    top: 0;
    right: 0;
    content: '+';
    display: inline-block;
    width: 2em;
    height: 2em;
    -webkit-transition: transform 0.4s;
            transition: transform 0.4s;
  }
  /* 答え */
  .cp_qa .cp_actab .cp_actab-content {
    position: relative;
    overflow: hidden;
    max-height: 0;
    padding: 0 0 0 2.5em;
    -webkit-transition: max-height 0.2s;
            transition: max-height 0.2s;
    border-radius: 0 0 0.5em 0.5em;
  }
  .cp_qa .cp_actab .cp_actab-content::before {
    font-family: serif;
    font-size: 1.5em;
    position: absolute;
    margin: 0.4em 0 0 -1em;
    padding: 0;
    content: 'A';
  }
  .cp_qa .cp_actab .cp_actab-content p {
    margin: 1em 1em 1em 0;
  }
  /* 質問を開いた時の仕様 */
  /* --答えの高さ */
  .cp_qa .cp_actab input:checked ~ .cp_actab-content {
    max-height: 40em;
    border: 10px solid rgba(27,37,56,0.1);
  }
  /* 質問をクリックした時のアイコンの動き */
  .cp_qa .cp_actab input:checked ~ label {
    color: #00838f;
    border-radius: 0.5em 0.5em 0 0;
  }
  /* 質問をクリックした時の+の動き */
  .cp_qa .cp_actab input[type=checkbox]:checked + label::after {
    -webkit-transform: rotateZ(45deg);
    transform: rotateZ(45deg);
    -webkit-transform-origin: 50% 50%;
    transform-origin: 50% 50%;
  }
</style>
