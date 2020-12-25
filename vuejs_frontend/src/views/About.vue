<template>
  <div class="about container">
    <h1>RingFit Rankerとは？</h1>

    <p>Twitter上の <b>#リングフィットアドベンチャー</b> の画像を収集し、順位を呟くbotです。<br>
    <a href="https://twitter.com/RingFitRanker">twitter.com/RingFitRanker</a> で運営中</p>

    <h2>機能1</h2>
    <p>アカウントをフォローしたうえで、<b>#リングフィットアドベンチャー</b> タグを付けて運動結果のスクリーンショットをツイートすると、順位をリプライします。</p>
    <img src="https://user-images.githubusercontent.com/40136659/95277065-ddd0fc00-0887-11eb-9ece-bee6b76955fe.jpg" class="img-fluid rounded mx-auto d-block">
    <br>
    <img src="https://user-images.githubusercontent.com/40136659/95277166-196bc600-0888-11eb-8666-43365546de63.jpg" class="img-fluid rounded mx-auto d-block">
    <br>

    <h2>機能2</h2>
    <p>毎日4時ごろに順位を集計し、12時頃に消費カロリー数ランキング Top10を呟きます。</p>
    <img src="https://user-images.githubusercontent.com/40136659/84641755-78eb4200-af36-11ea-802d-18bb9300c749.png" class="img-fluid rounded mx-auto d-block"><br>

    <h2>機能3</h2>
    <p><router-link to="/">Rankingページ</router-link>から、全員分の順位を見ることができます。過去の日付の順位を見ることも可能です。</p>
    <img src="https://user-images.githubusercontent.com/40136659/103138235-d0ebd800-4713-11eb-8a1e-607b83daa477.png" class="img-fluid rounded mx-auto d-block"><br>

    <h2>機能4</h2>
    <p><router-link to="/user">Userページ</router-link>では、Twitterの@ユーザ名を入力することで、いままでの運動記録と、消費カロリーのグラフを見ることができます。</p>
    <img src="https://user-images.githubusercontent.com/40136659/95273961-7020d200-087f-11eb-87d0-e8b76e266791.png" class="img-fluid rounded mx-auto d-block"><br>

    <h1>プライバシーポリシー</h1>
    <p>当サービスのアクセス解析には Google Analytics を使用しています。
    Google Analytics は、Cookieを用いて、個人を特定できない形でアクセス情報を収集・解析します。<br>
      データが収集・処理される仕組みについては、<a href="https://policies.google.com/technologies/partner-sites">こちら</a> を御覧ください</p>
  </div>
</template>
