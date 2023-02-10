---
layout: page
title: 3-3. 数値積分【基本】
---

コンピュータはもともと，数式として解が得られない（解析解がない）物理方程式に対して，近似解を求めるために実現されたという経緯がある．その手法は<font color=red>数値解析</font>と呼ばれ，今日でも盛んに研究が行われている分野である．この問題では，代表的な数値解析手法である<font color=red>数値積分</font>について学ぶ．

数値解析を考える上で常に念頭に置かなくてはいけないのは，コンピュータ上では実数を表現するための精度（ざっくり言うと小数点以下の桁数）が有限であるということである．関連して，数学で言う無限大，無限小といった極限操作ができないため，いかに有限の操作で精度良く計算するかがカギとなる．

もともとの定積分の定義である「リーマン和の極限」

$$
S = \lim_{N=\infty}\sum_{i=1}^{N}f(\xi_{i})\Delta x_{i} = \int_{a}^{b}f(x)dx \\
x_{i} = (b-a)i/N+a (i=0, 2, ..., N) \\
\Delta x_{i} = x_{i}-x_{i-1} (i=1, 2, ..., N)\\
x_{i-1}\le\xi_{i}\le x_{i} (i=1, 2, ..., N)
$$

から一歩立ち戻り，有限和で近似するのが数値積分法である．ただし，図１のようにリーマン和は長方形の面積で関数の定積分を近似するため，精度が悪い．ここでは，同じ$N$でもっと精度高く数値積分ができる方法をいくつか実装してもらう．

<figure><img src="p33-rectangle.png" width="600px">
 <br> <figurecaption>図1: リーマン和に基づく数値積分</figurecaption>
</figure>

---
#### 1. 台形則
---
  積分区間$[a, b]$を$N$個の区間$[x_{0}, x_{1}], [x_{1}, x_{2}], \cdots [x_{N-1}, x_{N}]\quad (x_{0} = a, x_{N}=b)$に等分すると，各区分における定積分は，図2に示すように台形の面積として近似できる．
  
  <figure><img src="p33-trapezoid.png" width="600px">
  <br><figurecaption>図2: 台形則に基づく数値積分</figurecaption>
  </figure>
  
  
式で表すと以下のようになる：

$$
\int_{x_{i-1}}^{x_{i}}f(x)dx \simeq h\left(\frac{1}{2}f_{i-1}+\frac{1}{2}f_{i}\right)\qquad(f_{i} = f(x_{i}), h = x_{i}-x_{i-1}, i = 1, 2, \cdots, N)
$$

これを全区間に適用すると，積分区間$[a, b]$における積分は以下の式で近似できる：

$$
\int_{a}^{b}f(x)dx \simeq h\left(\frac{1}{2}f_{0}+f_{1}+f_{2}+\cdots+f_{N-1}+\frac{1}{2}f_{N}\right) \qquad (1)
$$

この式は「台形則に基づく」数値積分である．図1，図2を比較すると，台形則に基づく数値積分の方が視覚的に精度が高いことが見て取れる．

---
#### 2. Simpson則
---
 台形則は，言い方を替えると，区間ごとに関数を直線で近似してから数式上で定積分を行っているとも言える．区間$[x_{i-1}, x_{i}]$の端２点における関数の値から直線の式$A_{i}+B_{i}x$における$A_{i}$, $B_{i}$が求まる．この考え方を拡張すると，$x_{i-1}, x_{i}, x_{i+1}$の３点における値から関数を二次関数$A_{i}+B_{i}x+C_{i}x^2$
で近似し，数式上で定積分を行うことで，より精度の高い数値積分が可能である．この方法では，区間$[x_{i-1}, x_{i+1}]$における定積分は

$$
\int_{x_{i-1}}^{x_{i+1}}f(x)dx \simeq h\left(\frac{1}{3}f_{i-1}+\frac{4}{3}f_{i}+\frac{1}{3}f_{i+1}\right)\qquad(f_{i} = f(x_{i}), h = x_{i}-x_{i-1}, i = 1, 3, 5, \cdots, N-1)
$$

と近似され，考案者の名前を取ってSimpson則と呼ばれる．全区間における定積分は

$$
\int_{a}^{b}f(x)dx \simeq h\left(\frac{1}{3}f_{0}+\frac{4}{3}f_{1}+\frac{2}{3}f_{2}+\frac{4}{3}f_{3}+\cdots+\frac{2}{3}f_{N-2}+\frac{4}{3}f_{N-1}+\frac{1}{3}f_{N}\right) \qquad (2)
$$

となる．この方法では，区間数$N$は偶数である必要がある．

---
## 問題
---

台形則，Simpson則に基づく数値積分を行なう関数を作成し，それらを使って数学関数を積分するプログラムを作成せよ．

---
## 仕様
---

プログラムは以下の仕様を満たすこと．

- 入力は，後述する数学関数を指定する番号（整数）$i$ ($i = 1, 2, 3,$ or $4$)と，定積分を行なう範囲$[a, b]$を指定する実数$a, b (a<b)$，積分範囲の分割数$n$（整数，0より大きい，かつ偶数）とする：

  ```
  i a b n
  ```
- この入力の書式は各ステップ共通とする．
- 数学関数を定義するにあたり，`math.h`ヘッダをインクルードすること（`math.h`に関する詳細は[参考情報](#math_h)で述べる）．
- 数学関数は以下の４つ，$f_{1}(x), ..., f_{4}(x)$である．対応するプログラム上の関数`double f1(double x), ..., double f4(double x)`を定義すること．
  - $f_{1}(x) = 1$ → `double f1(double x){ return 1; }`
  - $f_{2}(x) = 1+2x-x^2$ → `double f2(double x){ return 1+2*x-x*x; }`
  - $f_{3}(x) = \sin x$ → `double f3(double x){ return sin(x); }`
  - $f_{4}(x) = xe^{-2x^2}$ → `double f4(double x){ return x*exp(-2*x*x); }`
- 台形則，Simpson則に基づく数値積分を実行するための関数をそれぞれ１つずつだけ作成すること．各関数は，第一引数を関数ポインタ（詳細は[参考情報](#function_pointer)），第二引数を`double`型の積分開始点$a$，第三引数を`double`型の積分終了点$b$，第四引数を`int`型の積分範囲の分割数$n$とし，積分結果を`double`型で返すこと：

  ```
  double integral_trapezoid(double (*f)(double x), double a, double b, int n);
  double integral_Simpson(double (*f)(double x), double a, double b, int n);
  ```
- 出力は，各ステップで説明されている仕様に従うこと．

---
### ステップに分けてプログラミング
---
この問題では，「関数の動作確認」「台形則に基づく数値積分の実装」「Simpson則に基づいた数値積分の実装」の3ステップに分けてプログラミングしてもらう．ステップごとに"動作確認"に成功しなければ，"TAに提出"が出来ないようになっている．以下では，各ステップをさらに細分化して説明する．

---
### ステップ1/3　「関数の動作確認」
---

- 最初のステップとして，上述の数学関数$f_{1}(x), ..., f_{4}(x)$を正しく実装しているかを確認する．また，関数ポインタの使用に慣れる．
- 入力された範囲$[a, b]$を$n$等分したときの各区分の端の点$x = x_{0}(=a), x_{1}, ..., x_{n}(=b)$と，入力された$i$に対応する関数の$x$における値を出力させる．
- 数学関数の値を出力させる際には、必ず関数ポインタを用いること．数学関数`f1, f2, f3, f4`を直接呼び出してはいけない．
- 以下のコードを参考にすること：

  ```
  // 必要なヘッダファイルのインクルード
  ????

  // 数学関数f1, f2, f3, f4の前方宣言
  double f1(double x);
  double f2(double x);
  double f3(double x);
  double f4(double x);

  int main(){
    int i; // 数学関数を指定する番号
    double a, b; // 積分範囲[a, b]
    int n; // 積分範囲の分割数
    double (*fp)(double); // 数学関数の先頭アドレスを格納する関数ポインタ

    ???? // i, a, b, nを読み込む
 
    // 入力された番号に従って，関数ポインタfpにf1, f2, f3, f4いずれかのアドレスを代入
    ????
    ????
    ????

    // 範囲[a, b]をn等分し，各区分の端の点における関数の値を出力（※n等分なのでn+1点）
    double h = ????;
    for(double x=a; x<=b+0.01*h; x+=h){
      ????
    }

    return 0;
  }

  // 数学関数f1, f2, f3, f4の後方定義
  ????
  ????
  ```
- 関数ポインタの使用方法については，[参考情報](#function_pointer)を読むこと．
- 出力は，$x$と$f(x)$を空白で区切って出力すること（末尾には空白は付けない）．
- 出力する数値は，小数点以下３桁を表示すること．
- 各行の末尾には改行文字`\n`を出力すること．
- なお，点$x$に関するforループの終了条件は，$x<=b$ではなく，$x<=b+0.01*h$のようにしているのは，計算精度の関係で，$x==b$となるべき点でそうならず，出力されない可能性があるからである．

---
#### ステップ1/3の実行例
---

+ 入力

  ```
  2 -1.0 1.0 20
  ```
+ 出力

  ```
  -1.000 -2.000
  -0.900 -1.610
  -0.800 -1.240
  -0.700 -0.890
  -0.600 -0.560
  -0.500 -0.250
  -0.400 0.040
  -0.300 0.310
  -0.200 0.560
  -0.100 0.790
  -0.000 1.000
  0.100 1.190
  0.200 1.360
  0.300 1.510
  0.400 1.640
  0.500 1.750
  0.600 1.840
  0.700 1.910
  0.800 1.960
  0.900 1.990
  1.000 2.000
  ```



---
### ステップ2/3　「台形則に基づく数値積分の実装」
---

- ステップ1/3のコードで，関数の値を出力させていた部分はコメントアウトすること．
- 上述の式(1)のとおりに` integral_trapezoid`関数を実装し，`main`関数で呼び出して数値積分を実行すること．
- 数学関数$f_1, f_2, f_3, f_4$は数式として不定積分が可能である．それぞれの不定積分関数を，`double F1(double x);`，`double F2(double x);`...，としてプログラム上で定義せよ．不定積分の積分定数は大きい数でなければ何でもよい．
- 関数ポインタを二つ（例えば`double (*fp)(double), (*F)(double)`）用意し，指定された被積分関数および対応する不定積分関数のアドレスを代入して，それらを用いて関数呼び出しを行う，あるいは数値積分を行う関数に渡すこと．
- 上述の不定積分関数から求めた定積分の結果，`integral_trapezoid`関数から求めた定積分の結果を小数点以下３桁まで出力すること．
- 数値の間には空白を出力すること．また，末尾には改行文字`\n`を出力すること．

---
#### ステップ2/3の実行例
---

+ 入力

  ```
  2 -1.0 1.0 20
  ```
+ 出力

  ```
  1.333 1.330
  ```
  
---
### ステップ3/3　「Simpson則に基づいた数値積分の実装」
---

- 上述の式(2)のとおりに`integral_Simpson`関数を実装し，`main`関数で呼び出して数値積分を実行すること．
- ステップ2/3と同様に不定積分関数から求めた定積分の結果，`integral_trapezoid`関数から求めた定積分の結果，`integral_Simpson`関数から求めた定積分の結果を小数点以下３桁まで出力すること．
- 関数ポインタを二つ（例えば`double (*fp)(double), (*F)(double)`）用意し，指定された被積分関数および対応する不定積分関数のアドレスを代入して，それらを用いて関数呼び出しを行う，あるいは数値積分を行う関数に渡すこと．
- 数値の間には空白を出力すること．また，末尾には改行文字`\n`を出力すること．

---
#### ステップ3/3の実行例
---

+ 入力

  ```
  2 -1.0 1.0 20
  ```
+ 出力

  ```
  1.333 1.330 1.333
  ```

---
### 参考情報
---

---
#### C言語における数学関数ライブラリ<a name="math_h"></a>
---

C言語の標準として，さまざまな数学関数が`math.h`に定義されている．主な関数は以下のとおり：

- 三角関数：`double sin(double);`，`double cos(double);`，`double tan(double);`．
- 逆三角関数：`double asin(double);`，`double acos(double);`，`double atan(double);`，`double atan2(double, double);`．
- 指数・対数関数，べき乗，平方根：`double exp(double);`，`double log(double);`，`double log10(double);`，`double pow(double, double);`，`double sqrt(double);`．
- 双曲線関数：`double sinh(double);`，`double cosh(double);`，`double tanh(double);`．
- ベッセル関数：`double j0(double);`，`double j1(double);`，`double jn(int, double);`，`double y0(double);`，`double y1(double);`，`double yn(int, double);`．
- 小数点以下切り上げ・切り捨て：`double ceil(double);`，`double floor(double);`．
- 絶対値：`double fabs(double);`．

これらの関数も，それぞれの特性を考慮した上で，精度の高い数値解析アルゴリズムに基づいて実装されている．

---
#### 関数ポインタ<a name="function_pointer"></a>
---

- プログラムが実行されるときメモリ上にあるのは変数（データ）だけではなく，プログラム自体も，プロセッサが実行する命令群としてメモリ上にある．一つ一つの関数は配列のようにまとまってメモリ上に格納され，”先頭”のアドレスが存在する．「関数ポインタ」にこの先頭アドレスを格納することで，「関数を関数に渡す」ということが可能になる．
- 以下の例では，前方で定義した関数`f`の先頭アドレスを，`main`関数で関数ポインタに代入し，その関数ポインタを介して関数`f`を呼び出している：

  ```
  double f(double x){ return x; }
  
  int main(){
    double (*fp)(double);
    
    fp = f;
    
    double y = fp(4.0);
    
    return 0;
  }
  ```
- 関数ポインタは，`double (*fp)(double)`のように関数の引数および返り値の型を指定して宣言する必要がある．
- 関数ポインタを介して関数を呼び出す際には，通常の関数の呼び出しと同じく`fp(4.0)`のように書く．
- 関数ポインタは，本問題のように「ある関数の数値積分をする」という汎用的な関数を書きたいときに，「ある数値関数」を引数に渡すことで汎用性を保つのに非常に便利である．関数ポインタを用いない場合は，「$f_1(x)$の数値積分をする」関数，「$f_2(x)$の数値積分をする」関数，…，という風に，中身がほとんど同じ関数をいくつも書かなくてはいけなくなってしまう．