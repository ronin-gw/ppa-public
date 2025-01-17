---
layout: page
title: 3-4. 常微分方程式【発展】
---

## 注意事項
---
1. 発展問題は一度提出したら修正不可です。仕様を満たしているかよく確認して、提出して下さい。
1. 発展問題に関しては、質問は教員が対応します。また、演習時間外の質問に関しては対応が間に合わない場合があります。

---
## 学習内容
---
1. 数値解析手法
1. 浮動小数点の扱い方については，p1-3, p2-4を参照のこと．
1. 浮動小数点における精度については，p2-4の末尾を参照のこと．
1. 関数の宣言・定義方法については，p2-1, p2-2を参照のこと．
1. 関数への配列の渡し方については，p3-1を参照のこと．
1. 動的メモリ確保については，p3-2を参照のこと．
   
---
## 導入文
---
物理法則は多くの場合，微分方程式の形で表現される．微分方程式の数値解析による解法は，物理学の理解と工学応用に大きく貢献してきた．この問題では，常微分方程式の数値解法を学ぶとともに，実際にニュートンの運動方程式を解くプログラムを作成する．

変数$x$の有限区間$x=[a, b]$で定義される未知関数$y(x)$に対する常微分方程式

$$
\frac{dy}{dx} = f(x, y) \quad (1)
$$

を考える．$f(x, y)$は既知の関数とし，境界条件としては$y(a) = y_{a}$が与えられるものとする．p3-3と同じように，区間$[a, b]$を有限の区間に分割し，微分を近似することで，この常微分方程式に対する数値解法が得られる．ここでは，３つの方法を実装してもらう．

---
#### 1. オイラー法
---

区間$x=[a, b]$をn個に等間隔$h = (b-a)/n$に分ける：

$$
x_{0}=a, x_{1}=a+h, x_{2}=a+2h..., x_{n-1}=a+(n-1)h, x_{n} = b
$$

これらの点における$y(x)$を

$$
y_{0}=y(x_{0}), y_{1}=y(x_{1}), ..., y_{n} = y(x_{n})
$$

とする．式(1)の左辺の微分をこれらの点上での値で近似すると

$$
\frac{dy}{dx} \approx \frac{y_{i+1}-y_{i}}{x_{i+1}-x_{i}} = f(x_{i}, y_{i}) \\
y_{i+1} = y_{i}+hf(x_{i}, y_{i}) \quad (2)
$$

と書くことができる．初期値$y_{0}$が与えられれば，次の$y_{1}$は式(2)を用いて$y_{1} = y_{0}+hf(x_{0}, y_{0})$と計算でき，同じように繰り返していけば$y_{n}$まで計算できる．この手法を”オイラー法”と呼ぶ．この方法もp3-3のリーマン和と同様，計算の精度が低いため，実践的に使われることはほとんどない．

---
#### 2. ２次のルンゲ・クッタ法（中点法）
---

オイラー法が精度が低い理由の一つは，右辺の関数$f(x, y)$を点$(x_{i}, y_{i})$でしか参照していないことにある．より精度の高い手法では，$(x_{i}, y_{i})$と$(x_{i+1}, y_{i+1})$の間の点における$f$を参照する．

２次のルンゲ・クッタ法あるいは中点法と呼ばれる手法では，$x_{i}$と$x_{i+1}$の中点$x_{i}+h/2$における$y(x_{i}+h/2)$をオイラー法で求めておき，次に$(x_{i}+h/2, y(x_{i}+h/2))$における$f$を参照して$y_{i+1}$を計算する．式で書くと以下のようになる：

$$
k_{1} = hf(x_{i}, y_{i}) \\
k_{2} = hf(x_{i}+h/2, y_{i}+k_{1}/2) \\
y_{i+1} = y_{i}+k_{2}
$$

---
#### 3. ４次のルンゲ・クッタ法
---

２次のルンゲ・クッタ法を発展させた手法が ４次のルンゲ・クッタ法であり，中点だけでなく$x_{i}$と$x_{i+1}$における$f$も参照する：

$$
k_{1} = hf(x_{i}, y_{i}) \\
k_{2} = hf(x_{i}+h/2, y_{i}+k_{1}/2) \\
k_{3} = hf(x_{i}+h/2, y_{i}+k_{2}/2) \\
k_{4} = hf(x_{i}+h, y_{i}+k_{3}) \\
y_{i+1} = y_{i}+\frac{k_{1}}{6}+\frac{k_{2}}{3}+\frac{k_{3}}{3}+\frac{k_{4}}{6}
$$

なぜこの式で精度が高く計算できるのか，詳細は数値解析の授業に譲るが，４次のルンゲ・クッタ法は精度の高い常微分方程式の数値解法として広く用いられている．

---
## 問題
---

上記の数値解法を実際に適用する例として，粘性抵抗および慣性抵抗を考慮に入れた，物体の一次元運動の速度を求めるニュートンの運動方程式

$$
\frac{dv}{dt} = -g-\alpha v-\beta v|v| \quad (3)
$$

を考える．ここで，$t$は時刻，$v$は物体の速度，$|v|$は速度の絶対値，
$g = 9.80665 [m/s^2]$は重力加速度，$\alpha\geq0$は粘性抵抗の強さを表す係数，
$\beta\geq0$は慣性抵抗の強さを表す係数であり，
$\alpha$と$\beta$は入力として与えられるとする．速度の初期値は$v(t=0) = 0$と指定する．

$\alpha = \beta = 0$の場合はよく知られた自由落下運動であり，物体の速度は時刻に比例して増えていく．$\alpha \neq 0$あるいは$\beta \neq 0$の場合は，抵抗力が働いてある一定の速度（終端速度）に収束していく．（下図参照）

<br>
<figure><img src="p34-plot.png" width="600px">
 <br> <figurecaption>図1: 物体の一次元運動（自由落下、粘性抵抗による速度収束、慣性抵抗による速度収束）</figurecaption>
</figure>
<br>

入力パラメータに対してオイラー法，２次のルンゲ・クッタ法，４次のルンゲ・クッタ法を用いて式(3)の解を求めるプログラムを作成せよ．

---
## 仕様
---

プログラムは以下の仕様を満たすこと．

- 入力は二つの非負の実数$\alpha\geq0, \beta\geq0$，終了時刻を表す正の実数$t_{e}>0$，区間$t=[0, t_{e}]$を等分する区間数$n>0$の４つとし，この順に空白で区切られて与えられているとする．
- 時刻$t=0, h, 2h, ..., t_{e}$（$h = t_{e}/n$）と，その時刻における物体の速度$v(t)$をオイラー法，２次のルンゲ・クッタ法，４次のルンゲ・クッタ法を用いて計算した値を，この順に出力すること．出力する実数は小数点以下2桁まで出力し，それらの間には空白1文字を出力し，末尾には改行を出力すること．
- 各解法を用いて計算した値は，必要十分な配列長に動的メモリ確保された配列に格納し，処理完了後にメモリ解放すること．固定長配列やVLAは使用しないこと．

---
### 実行例
---

- 入力例1

```
0 1 5 20
```

- 出力例1
  
```
0.00 0.00 0.00 0.00
0.25 -2.45 -2.08 -2.04
0.50 -3.40 -2.62 -2.83
0.75 -2.96 -2.84 -3.05
1.00 -3.22 -2.95 -3.11
1.25 -3.08 -3.02 -3.13
1.50 -3.16 -3.06 -3.13
1.75 -3.11 -3.09 -3.13
2.00 -3.14 -3.10 -3.13
2.25 -3.13 -3.11 -3.13
2.50 -3.13 -3.12 -3.13
2.75 -3.13 -3.12 -3.13
3.00 -3.13 -3.13 -3.13
3.25 -3.13 -3.13 -3.13
3.50 -3.13 -3.13 -3.13
3.75 -3.13 -3.13 -3.13
4.00 -3.13 -3.13 -3.13
4.25 -3.13 -3.13 -3.13
4.50 -3.13 -3.13 -3.13
4.75 -3.13 -3.13 -3.13
5.00 -3.13 -3.13 -3.13
```

- 入力例2

```
1 1 5 15
```

- 出力例2
  
```
0.00 0.00 0.00 0.00
0.33 -3.27 -1.83 -2.05
0.67 -1.89 -1.98 -2.45
1.00 -3.34 -2.06 -2.59
1.33 -1.78 -2.12 -2.64
1.67 -3.40 -2.16 -2.66
2.00 -1.68 -2.19 -2.67
2.33 -3.45 -2.21 -2.67
2.67 -1.60 -2.23 -2.67
3.00 -3.48 -2.25 -2.67
3.33 -1.55 -2.26 -2.67
3.67 -3.50 -2.27 -2.67
4.00 -1.52 -2.28 -2.67
4.33 -3.51 -2.28 -2.67
4.67 -1.50 -2.29 -2.67
5.00 -3.52 -2.30 -2.67
```

---
### 参考情報
---
