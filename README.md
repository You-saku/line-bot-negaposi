# LINE_bot_sample
<h2>2020/10/19</h2>
リポジトリスタート

<h2>2020/10/29</h2>
リポジトリを改善<br>
<strong>ネガポジ分析を取り入れてみた</strong><br>
ネガティブワード、ポジティブワードの辞書は(dictonary/pn.csvのcsvファイルの著作権も同様)<br>
<br>
"小林のぞみ，乾健太郎，松本裕治，立石健二，福島俊一. 意見抽出のための評価表現の収集. 自然言語処理，Vol.12, No.3, pp.203-222, 2005. / Nozomi Kobayashi, Kentaro Inui, Yuji Matsumoto, Kenji Tateishi. Collecting Evaluative Expressions for Opinion Extraction, Journal of Natural Language Processing 12(3), 203-222, 2005."<br>
で紹介している<br>
<br>
"日本語評価極性辞書（名詞編）ver.1.0（2008年12月版）/ Japanese Sentiment Dictionary (Volume of Nouns) ver. 1.0  著作者: 東北大学 乾・岡崎研究室 / Author(s): Inui-Okazaki Laboratory, Tohoku University"<br>

を使わせていただきました。ありがとうございます。<br>

<h2>2020/10/31</h2>
アプリを改善、そして実用レベルまで向上した。<br>
AWSのAWS Comprehendを利用した感情分析に変更 <- 理由 : 圧倒的計算量の削減。自作の辞書を使用するとどうしても時間がかかってタイムオーバーする。<br>
一応、LINEで返信が問題なく帰ってくるレベルの返信スピードまで向上<br>
<br>
現時点では今後の改善は未定