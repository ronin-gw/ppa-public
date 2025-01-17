---
layout: page
title: 4-1. 編集距離(再帰手続き版)【初歩】
---


## 学習内容
---
1. p1-1~p1-5で使った機能全て，特に`for`文，`if`文の複雑な組み合わせ．

---
### 編集距離
---

2つの文字列の類似性が測定できると役に立つ場合がある．
例えば，`GATCGGCAT`と`CAATGTGAATC`の2つのDNA塩基配列に対して，次のような対応付けを行うことで，これらの塩基配列の類似度合いを調べることができる．

```
G ATCG GCAT
CAAT GTGAATC
RI==D=I=R==I
```

なお，`=`は文字が一致している箇所，`R`は文字が異なっている場所，`D`は上側に文字を挿入した箇所，`I`は下側に文字を挿入した箇所である．
また，修正前と修正後のソースコードの類似部分を見つけることで，ソースコードに加えられた変更点（diff）を調べることができる（以下の例では`=`を`==`に修正）．

```
before: if (flag = 1) { printf("found\n"); }
after:  if (flag == 1) { printf("found\n"); }
```

本課題では，2つの文字列$X = \langle x_1, x_2, ..., x_m \rangle$と$Y = \langle y_1, y_2, ..., y_n \rangle$の類似性を測定する方法として，**編集距離（edit distance）**に取り組む．


---
### 編集距離の定義
---

編集距離について理解するため，文字列$X$の先頭から任意回の**編集操作**を逐次適用していき，文字列$Y$に等しい文字列$Z = \langle z_1, z_2, ..., z_n \rangle$を得る手続きを考える．**編集操作**とは，「$X$ の 2 文字目を $Z$ の 3 番目の変数にコピーする」などの「$X$ の $i$ 番目の文字 $x_i$ の情報を使って，$Z$ の $j$ 番目の変数 $z_j$ を変更する操作」をいう．

以上を形式的に表現してみよう．まず，$Z$の初期状態を空文字列とする．$X,Z$ の編集操作の対象となる添字を変数 $i,j$ で表現し，初期状態を $i=j=1$ とする．すると，前述の手続きは，「$Y$ と等しい $Z$ を得るまで (1) 編集操作の適用，(2) 操作対象の添字 $i,j$ の更新，を繰り返す」という手続きで表現できる．ここで，可能な編集操作は，次のものとする．

+ **copy**: $X$の1文字を$Z$にコピーする．つまり，代入$z_j \gets x_i$を行い，$i$と$j$にそれぞれ$1$を加える．
+ **replace**: $X$の1文字を別の文字$\alpha$に置換する．つまり，代入$z_j \gets \alpha$を行い，$i$と$j$にそれぞれ$1$を加える．
+ **delete**: $X$の1文字を削除する．つまり，$j$を変更せずに$i$に$1$を加える．
+ **insert**: 文字$\alpha$を$Z$に挿入する．つまり，代入$z_j \gets \alpha$を行ったうえで，$j$だけに$1$を加える．

例えば，$X = \langle a,l,g,o,r,i,t,h,m \rangle$に編集操作を適用し，$Z=\langle  a,l,t,r,u,i,s,t,i,c \rangle$を得る過程の例を示す．
ここで，$X$の太字と$Z$のアスタリスク（*）は，操作対象の添字 $i,j$ を表す．$Z$ の アンダーバー (_) は，空文字を表す．

| 現在の $X$            | 適用する操作     | 操作適用後の $Z$      | 操作適用後の $i$ | 操作適用後の $j$ |
|:----------------------|:-----------------|:----------------------|:-----------------|:-----------------|
| **a** l g o r i t h m | 初期化           | * _ _ _ _ _ _ _ _ _   | 1                | 1                |
| **a** l g o r i t h m | copy             | a * _ _ _ _ _ _ _ _   | 2                | 2                |
| a **l** g o r i t h m | copy             | a l * _ _ _ _ _ _ _   | 3                | 3                |
| a l **g** o r i t h m | replace with 't' | a l t * _ _ _ _ _ _   | 4                | 4                |
| a l g **o** r i t h m | delete           | a l t * _ _ _ _ _ _   | 5                | 4                |
| a l g o **r** i t h m | copy             | a l t r * _ _ _ _ _   | 6                | 5                |
| a l g o r **i** t h m | insert 'u'       | a l t r u * _ _ _ _   | 6                | 6                |
| a l g o r **i** t h m | insert 'i'       | a l t r u i * _ _ _   | 6                | 7                |
| a l g o r **i** t h m | insert 's'       | a l t r u i s * _ _   | 6                | 8                |
| a l g o r **i** t h m | insert 't'       | a l t r u i s t * _   | 6                | 9                |
| a l g o r **i** t h m | copy             | a l t r u i s t i *   | 7                | 10               |
| a l g o r i **t** h m | replace with 'c' | a l t r u i s t i c * | 8                | 11               |
| a l g o r i t **h** m | delete           | a l t r u i s t i c * | 9                | 11               |
| a l g o r i t h **m** | delete           | a l t r u i s t i c * | 10               | 11               |
{: .table .table-striped}

一般的に，ある文字列を別の文字列に変換する編集過程は複数存在することに注意せよ．

さて，各編集操作$a$にコスト${\rm cost}(a)$が定義されているとすれば，上記の編集過程で要するコストは，次のように計算できる．

$$
4 \times {\rm cost}(\mbox{copy}) + 2 \times {\rm cost}(\mbox{replace}) + 3 \times {\rm cost}(\mbox{delete}) + 4 \times {\rm cost}(\mbox{insert})
$$

本課題では，${\rm cost}(\mbox{copy}) = 0$，${\rm cost}(\mbox{replace}) = {\rm cost}(\mbox{delete}) = {\rm cost}(\mbox{insert}) = 1$とする．したがって，編集過程のコストの総和は$9$である．

一般的に，2つの文字列$X = \langle x_1, x_2, ..., x_m \rangle$と$Y = \langle y_1, y_2, ..., y_n \rangle$，および編集操作コストが与えられたとき，**$X$から$Y$への編集距離とは，$X$を$Y$に変換する編集操作列のコストの最小値である．**

<span style="color: red;"><b>注意</b></span>
$X,Z$の編集操作の対象となる添字を変数 $i,j$ で表現し，初期状態を $i=j=1$から始めたが，プログラムを書く上では配列が$x[0]$と$0$から始まることに注意せよ．

---
### 編集距離の求め方
---

編集距離を効率良く求める問題を考える．まず，**接頭辞 (prefix)** という概念を導入する．

+ ある文字列$X = \langle x_1, x_2, ..., x_m \rangle$の長さ$p \in \lbrace0, 1, ..., m\rbrace$の**接頭辞**を$X_p = \langle x_1, x_2, ..., x_p \rangle$と定義する．例えば，$X = \langle A, T, C, G \rangle$に対し，$X_2 = \langle A, T \rangle$である．$X_0$は空文字列である．

$X$の接頭辞$X_i$（$i \in \lbrace0, 1, ..., m\rbrace$），$Y$の接頭辞$Y_j$（$j \in \lbrace0, 1, ..., n\rbrace$）の編集距離を$c_{i,j}$と書くと，以下の漸化式が成り立つ．

$$
c_{i,j} = \begin{cases}
\max (i, j) & i = 0 \mbox{ または } j = 0 \mbox{ のとき} \\
\min \begin{cases}
c_{i-1, j-1} + d_{x_i \neq y_j},\\
c_{i-1, j} + 1,\\
c_{i, j-1} + 1,\\
\end{cases} & それ以外
\end{cases}
$$

ただし，$d_{x_i \neq y_j}$は，$x_i = y_j$ならば$0$，$x_i \neq y_j$ならば$1$である（注意: クロネッカーのデルタとは異なる）．
$c_{i,j}$の漸化式のうち，最小値を求める部分は次の編集操作に対応する．

+ （$x_i = y_j$の場合のみ）$c_{i-1,j-1}$: $Y_{j-1}$に$x_i$をコピー（copy）する
+ （$x_i \neq y_j$の場合のみ）$c_{i-1,j-1} + 1$: $x_i$を$\alpha$に置換（replace）して，$Y_{j-1}$に追加する
+ $c_{i-1,j} + 1$: $x_i$を削除（delete）し，$Y_j$を得る
+ $c_{i,j-1} + 1$: 新しい文字$\alpha$を挿入（insert）し，$Y_j$を得る

以上のことから，**編集距離$c_{m,n}$を求める問題は，部分問題，すなわち編集距離$c_{m-1,n-1}$, $c_{m-1,n}$, $c_{m,n-1}$を求める問題に分解できる．**


例えば，$X = \langle a, b \rangle$と$Y = \langle c, d\rangle$に対して，$c_{i,j}$は次のように求まる．$X$と$Y$の編集距離は$2$である．
<div align="center">
<img src="p41-ed-equation.png" width="600px">
</div>
<div style="text-align: center;">（課題説明スライド 16ページを参照）</div>

<span style="color: red;"><b>注意</b></span>
編集距離 $c_{0,j}$ は空文字列 $X_0$ と接頭辞 $Y_j = \langle y_1, y_2, ..., y_j \rangle$ の編集距離であり，接頭辞 $X_1=\langle x_1 \rangle$ と接頭辞 $Y_{j+1}=\langle y_1, y_2, ..., y_j, y_{j+1}\rangle$ の編集距離ではないことに注意せよ．プログラム上では配列が $x[0]$ と $0$ から始まるため，混同しやすい．


---
### 漸化式の説明
---

漸化式のそれぞれの式の成立についてもう少し詳しく説明しよう．
漸化式

$$
c_{i,j}=c_{i-1, j} + 1
$$

は，編集距離 $c_{i,j}$ が $c_{i-1, j} + 1$ によって計算することができ，このときの編集操作が削除（delete）であることを意味する．
これは，二つの接頭辞 $X_{i-1} = \langle x_1, x_2, ..., x_{i-1} \rangle$ と $Y_j = \langle y_1, y_2, ..., y_j \rangle$ の編集距離 $c_{i-1, j}$ の値が既知のとき，新しい接頭辞 $X_{i} = \langle x_1, x_2, ...,x_{i-1}, x_{i} \rangle$ に対して文字 $x_{i}$ を削除（delete）すれば元の接頭辞 $X_{i-1}$ が得られるからである．

挿入（insert）についても同様であり，二つの接頭辞 $X_{i} = \langle x_1, x_2, ..., x_{i} \rangle$ と $Y_{j-1} = \langle y_1, y_2, ..., y_{j-1} \rangle$ の編集距離 $c_{i, j-1}$ の値が既知のとき，(接頭辞 $Y_{j-1}$ に等しい)接頭辞 $Z_{j-1}$ に文字 $x_{i}$ を挿入（insert）すれば(接頭辞 $Y_{j}$ に等しい)接頭辞 $Z_{j}$ を得ることができる．
したがって，

$$
c_{i,j}=c_{i, j-1} + 1
$$

が成立する．

コピー（copy）と置換（replace）に関しても同様に，二つの接頭辞 $X_{i-1} = \langle x_1, x_2, ..., x_{i-1} \rangle$ と $Y_{j-1} = \langle y_1, y_2, ..., y_{j-1} \rangle$ の編集距離 $c_{i-1, j-1}$ の値が既知のとき，文字 $x_{i}$ と $y_{j}$ が等しければ，(接頭辞 $Y_{j-1}$ に等しい)接頭辞 $Z_{j-1}$ に文字 $x_{i}$ をコピー（copy）すれば(接頭辞 $Y_{j}$ に等しい)接頭辞 $Z_{j}$ を得ることができるので,

$$
c_{i,j}=c_{i-1, j-1}
$$

文字 $x_{i}$ と $y_{j}$ が等しくなければ，文字 $x_{i}$ を文字 $y_{j}$ に置換（replace）して接頭辞 $Z_{j-1}$ に追加すれば(接頭辞 $Y_{j}$ に等しい)接頭辞 $Z_{j}$ を得ることができるので,

$$
c_{i,j}=c_{i-1, j-1}+1
$$

となる．

以上より，$i\neq0$ かつ $j\neq0$ ならば漸化式

$$
c_{i,j} = 
\min \begin{cases}
c_{i-1, j-1} + d_{x_i \neq y_j},\\
c_{i-1, j} + 1,\\
c_{i, j-1} + 1,\\
\end{cases} 
$$

が成立する．

また $i=0$ の場合は空文字列 $X_0$ と接頭辞 $Y_j = \langle y_1, y_2, ..., y_j \rangle$ の比較であり，空文字列 $Z_0$ に挿入（insert）を $j$ 回することによって文字列 $Y_j$ が得られるので，編集距離は $c_{0,j}=j$ である．
$j=0$ の場合も同様に，接頭辞 $X_{i} = \langle x_1, x_2, ..., x_{i} \rangle$ と空文字列 $Y_0$ の比較であり，全ての $x_i$ を削除（delete）すれば，$Y_0$ を得られるので，編集距離は $c_{i,0}=i$ である．


---
## 問題
---
与えられた文字列$X$を$Y$に変換する編集距離を再帰関数により求めるプログラムを実装せよ．

---
### 仕様
---
+ `include`するファイルは`<stdio.h>`，`<stdlib.h>`および`"ppa_extra_h/p3_header.h"`のみとする．

+ プログラム全体の構成を以下に従うようにする．
  + `main`関数の正常終了時の戻り値を0にする．
  + 関数は前方宣言を用い，関数本体は`main`関数の下に記述する（後方定義）．

+ 文字列$X$，文字列$X$の先頭から$m$文字目の場所を表すインデックス$m$，文字列$Y$，文字列$Y$の先頭から$n$文字目の場所を表すインデックス$n$の4つを引数にとり，編集距離を返す再帰関数`ld`を作成すること
  + 例：
  ```
  int ld(char *X, int m, char *Y, int n);
  ```
  + 再帰を止めるタイミングは，文字列長が0になって関数を呼び出した後とする．例えば，X=a，Y=cの場合，
  ```
  c1,1
  c1,0
  c0,1
  c0,0
  ```
  の4回呼び出すものとする．

+ 文字列$X$の位置$a$の文字と文字列$Y$の位置$b$の文字が等しい場合に0，違う場合に1を返す関数`delta`を作成し，それを再帰関数`ld`の中で用いること
  + <span style="color: red;"><b>注意</b></span>**この文における「位置$a$」と「位置$b$」は，数式上のインデックスを表す．C言語の配列としてのインデックスは「$a-1$」と「$b-1$」である**(例えば, $X$の「位置$a$番目」のインデックスは, c言語の配列としては$X[a-1]$となる)．
  + 例：
  ```
  int delta(char *X, int a, char *Y, int b);
  ```

+ 入力データの読み込み
  + 入力データの読み込みは`main` 関数内で行うこと．
  + 入力用の文字列$X$，$Y$とその要素数`len_x`，`len_y`は標準入力から次の順番で与えられる．
  ```
  len_x⊔len_y⊔X⊔Y↩︎
  ```
  + `⊔` は半角スペース，`↩︎`は改行を表す．
  + つまり，1,2列目が配列の要素数,3,4列目が配列の要素である

+ 標準出力に以下の出力をする．
  + 1行目に入力文字列$X$とその長さを表示する．2つの間には半角スペースを入れる．
  + 2行目に入力文字列$Y$とその長さを表示する．2つの間には半角スペースを入れる．
  + 3行目に編集距離を表示する．表示後に改行する．
    + 実行例をこのページの最後（「ステップ3/3の実行例」）に示したので，参考にせよ．
  + 出力例の`⊔` は半角スペース，`↩︎`は改行を表す．

+ `#include "ppa_extra_h/p3_header.h"`という宣言を通して，以下の関数を必要に応じて用いよ． これらの関数を新しく作成する必要はない．詳細は，[こちら](#ternary_operator2)を参照のこと．
  + `malloc_string_`
  + `read_string_`
  + `vmax_`
  + `vmax3_`
  + `vmin_`
  + `vmin3_`
+ 文字列の読み込みには`malloc_string_`関数と`read_string_`関数を用いよ(ステップ1/3のプログラム例も参考にせよ)． 
  + 例えば以下のように書くと，長さ`len_x`の入力文字列を配列`data_x`に読み込むことができる．
  ```
  char* data_x = malloc_string_(len_x);
  read_string_(data_x, len_x);  
  ```
  + `malloc_string_`関数で配列`data_x`を動的に確保し，`read_string_`関数によって長さ`len_x`の入力文字列を配列`data_x`に読み込んでいる．**`malloc_string_`関数では, 「文字列長さ+2」で配置されている**(詳細は[こちら](#ternary_operator2)を参照のこと).
+ `vmax_`/`vmin_`は２つの値のうち大きい/小さい値を戻り値とする関数である．
  + `vmax_(2, 3)` なら戻り値は`3`，`vmin_(1, 3)` なら戻り値は`1`．

+ `vmax3_`／`vmin3_`は3つの値のうち最も大きい／小さい値を戻り値とする関数である．
  + `vmax3_(3, 2 ,1)` なら戻り値は`3`，`vmin3_(2, 1, 3)` なら戻り値は`1`．

+ **グローバル変数を用いることは禁止とする.**(グローバル変数の詳細は, 課題4-2を参照)

---
## ステップに分けてプログラミング
---
この問題では，「`delta`関数を実装し，二つの文字の長さが同じ場合に対して，`for`ループを用いて簡略化した編集距離を計算する」「ステップ1/3の処理を再帰を用いて実装し，簡略化した編集距離を計算する」「`ld`関数を完成させ，(正しい)編集距離を計算する」の3ステップに分けてプログラミングしてもらう．ステップごとに”動作確認”に成功しなければ，”TAに提出”が出来ないようになっている．以下では，各ステップをさらに細分化して説明する．

---
## ステップ1/3　「`delta`関数を実装し，二つの文字の長さが同じ場合に対して，`for`ループを用いて簡略化した編集距離を計算する」
---
- 編集操作はコピー（copy），置換（replace），削除（delete）と挿入（insert）の四つの操作から構成される.
まずは問題を簡単にするために，ステップ1/3では削除（delete）と挿入（insert）の操作は忘れて，コピー（copy）と置換（replace）のみを編集操作とし，さらに，二つの文字列$X = \langle x_1, x_2, ..., x_m \rangle$と$Y = \langle y_1, y_2, ..., y_m \rangle$の長さが同じ場合を考え，**簡略化した編集距離**を計算する.

- このとき，先頭から順番に$x_1$と$y_1$の文字を比較してコピー（copy）または置換（replace），$x_2$と$y_2$の文字を比較してコピー（copy）または置換（replace）...としていけば簡略化した編集距離が計算できる.

- <span style="color: red;"><b>重要</b></span> 削除（delete）と挿入（insert）の操作を無視するので，ステップ1/3で計算する編集距離は正しい編集距離ではないことに注意せよ.例として，eatとateの正しい編集距離は2であるが，ステップ1/3では先頭から$x_1$と$y_1$，$x_2$と$y_2$，$x_3$と$y_3$の全ての文字が異なるので簡略化した編集距離は3となる.

#### 1-1. `delta`関数の実装
- 関数の引数を記入し，関数の中身を実装する．

#### 1-2. `for`ループを用いて簡略化した編集距離を計算する
- `delta`関数を用いて，二つの文字の長さが同じ場合に対して簡略化した編集距離を計算する.

- **文字列$X$の要素$x_i$は，C言語では`x[i-1]`として表現されることに注意せよ**（配列のインデックスが$0$から始まるため）．


#### 1-3. 標準出力の部分を実装する
- 標準出力に以下の出力をする．
  + 1行目に入力文字列$X$とその長さを表示する．2つの間には半角スペースを入れる．
  + 2行目に入力文字列$Y$とその長さを表示する．2つの間には半角スペースを入れる．
  + 3行目に簡略化した編集距離を表示する．表示後に改行する．
    + 「ステップ1/3の実行例」を参考にせよ．

#### 1-4. 自動採点システムで動作確認

+ 以下のプログラムを必ず用いてプログラムを完成させること．
  + `???` の部分は適宜補完すること
  + 適宜コメント文を入れること
  
```
#include <stdio.h>
#include <stdlib.h>

#include "ppa_extra_h/p3_header.h"

int delta(char *X, int a, char *Y, int b);  // ???

int main() {
  int len_x, len_y ;                        // ???
  scanf(“%d”, &len_x);                      // ???
  scanf(“%d”, &len_y);                      // ???
  char* data_x = malloc_string_(len_x);     // ???
  char* data_y = malloc_string_(len_y);     // ???
  read_string_(data_x, len_x);              // ???
  read_string_(data_y, len_y);              // ???

    ...(省略)...  

  for(???){                                 //編集距離を計算 
    ...(省略)...
  }
  
    ...(省略)...  

  free(data_x);  // ???
  free(data_y);  // ???
  return 0;      // ???
}


int delta( ??? ) {

  ...(省略)...

}

```



---
## ステップ1/3の実行例
---

---
### 例（1）
---

+ 入力
```
3 3 eat ate
```

+ 出力
```
eat⊔3↩︎
ate⊔3↩︎
3↩︎
```

---
### 例（2）
---

+ 入力
```
5 5 abcde edcba
```

+ 出力
```
abcde⊔5↩︎
edcba⊔5↩︎
4↩︎
```




---
## ステップ2/3　「ステップ1/3の処理を再帰を用いて実装し，簡略化した編集距離を計算する」
---

- <span style="color: red;"><b>重要</b></span>ステップ2/3でも引き続き，削除（delete）と挿入（insert）の操作は無視して簡略化した編集距離を計算する．

- ここでは`for`ループを用いず，漸化式に基づき再帰を用いて簡略化した編集距離を計算する．再帰に関しては問題2-2(ユークリッドの互除法)を参考にせよ．

$$
c_{i,i}=c_{i-1, i-1} + d_{x_i \neq y_i},\\
$$

- `ld`関数の再帰を正しく実装出来たかをチェックするために，`ld(X,m,Y,n)`関数を呼び出した直後に次の表示を行うこと．
```
LD(m,n)
```

- 再帰を止めるタイミングは，文字列長が0になって関数を呼び出した後とする．例えば，X=a，Y=cの場合，
```
LD(1,1)
LD(0,0)
```


#### 2-1. `ld(X,m,Y,n)`関数の冒頭でLD(m,n)と出力する機能を実装

#### 2-2. 漸化式の「$i=0$又は$j=0$」の部分の処理を`ld`関数に実装

#### 2-3. 漸化式のコピー（copy）と置換（replace）の部分の処理を`ld`関数に実装

#### 2-4. 標準出力の部分を実装する
- 標準出力に以下の出力をする．
  + 1行目に入力文字列$X$とその長さを表示する．2つの間には半角スペースを入れる．
  + 2行目に入力文字列$Y$とその長さを表示する．2つの間には半角スペースを入れる．
  + 3行目以降に`ld(X,m,Y,n)`関数を呼び出した順番に表示する．表示後に改行する．
  + 最後の行に簡略化した編集距離を表示する．表示後に改行する．
    + 「ステップ2/3の実行例」を参考にせよ．

#### 2-5. 自動採点システムで動作確認



+ 以下のプログラムを必ず用いてプログラムを完成させること．
  + `???` の部分は適宜補完すること
  + 適宜コメント文を入れること
  
```
#include <stdio.h>
#include <stdlib.h>

#include "ppa_extra_h/p3_header.h"

int delta(char *X, int a, char *Y, int b);  // ???
int ld(char *X, int m, char *Y, int n);     // ???

int main() {
  int len_x, len_y ;                        // ???
  scanf(“%d”, &len_x);                      // ???
  scanf(“%d”, &len_y);                      // ???
  char* data_x = malloc_string_(len_x);     // ???
  char* data_y = malloc_string_(len_y);     // ???
  read_string_(data_x, len_x);              // ???
  read_string_(data_y, len_y);              // ???
  
  ...(省略)...

  free(data_x);  // ???
  free(data_y);  // ???
  return 0;      // ???
}


int delta( ??? ) {

  ...(省略)...

}


int ld( ??? ) {

  ...(省略)...

}
```



---
## ステップ2/3の実行例
---

---
### 例（1）
---

+ 入力
```
3 3 eat ate
```

+ 出力
```
eat⊔3↩︎
ate⊔3↩︎
LD(3,3)↩︎
LD(2,2)↩︎
LD(1,1)↩︎
LD(0,0)↩︎
3↩︎
```

---
### 例（2）
---

+ 入力
```
5 5 abcde edcba
```

+ 出力
```
abcde⊔5↩︎
edcba⊔5↩︎
LD(5,5)↩︎
LD(4,4)↩︎
LD(3,3)↩︎
LD(2,2)↩︎
LD(1,1)↩︎
LD(0,0)↩︎
4↩︎
```

---
## ステップ3/3　「`ld`関数を完成させ，(正しい)編集距離を計算する」
---
ステップ3/3では削除（delete）と挿入（insert）の操作も考慮して`ld`関数を完成させ，正しい編集距離を計算する．

#### 3-1. 漸化式の削除（delete）と挿入（insert）の処理も実装
- 呼び出した`ld`関数を表示する部分はステップ3/3では使わないので，コメントアウトする．

#### 3-2. 標準出力の部分を実装する
- 仕様の標準出力の部分と以下の「ステップ3/3の実行例」を参照せよ．

#### 3-3. 自動採点システムで動作確認


---
## 「ステップ3/3の実行例」
---

---
### 例（1）
---

+ 入力
```
3 3 eat ate
```

+ 出力
```
eat⊔3↩︎
ate⊔3↩︎
2↩︎
```

---
### 例（2）
---

+ 入力
```
8 7 abababab abababc
```

+ 出力
```
abababab⊔8↩︎
abababc⊔7↩︎
2↩︎
```


---
## 参考情報
---

---
### `"ppa_extra_h/p3_header.h"`で定義されている関数の詳細<a name="ternary_operator2"></a>
---


+ 2つの値のうち大きい／小さい値を取得する関数`vmax_`／`vmin_`は"三項演算子"を用いて次のように定義されている．

```
int vmax_(int a, int b){
  return a>b ? a:b;
}

int vmin_(int a, int b){
  return a<b ? a:b;
}
```

+ 三項演算子については，[こちら](#ternary_operator)を参照のこと．


+ 3つの値のうち最も大きい／小さい値を取得する関数`vmax3_`／`vmin3_`は次のように定義されている．

``` 
int vmax3_(int a, int b, int c){
  return vmax_(vmax_(a, b), c);
}

int vmin3_(int a, int b, int c){
  return vmin_(vmin_(a, b), c);
}
```

+ 文字配列専用でメモリ確保する関数`malloc_string_`は次のように定義されている．

```
char* malloc_string_(int N){
  char* str  = (char *)malloc(sizeof(char)*(N+2));  // 配列に動的メモリを割り当てる
  
  if (str == NULL) {       // メモリ確保に失敗した際のエラー処理
    fprintf(stderr, "malloc_string_(): Cannot allocate memory.\n");
    exit(1);  // メモリ確保に失敗したら、プログラムを強制終了
  }
    
  zeros_(str, N+2);   // 配列dataを関数zeros_で初期化
  return str;
}

```

+ 標準入力から決められた長さの文字列を読み込む関数 `read_string_`は次のように定義されている．

```
void read_string_(char *str, int N){
  int tmpchar;


  // 文字列の前に空白か改行があれば全て除外する
  do {
    tmpchar = getc(stdin);
    if( tmpchar == EOF ){
      printf("read_string_(): Invalid string\n");
      exit(1);
    }
  }while( tmpchar==' ' || tmpchar=='\n' );

  ungetc(tmpchar, stdin);

  // N+1文字を標準入力から読み込む
  fgets(str, N+2, stdin);
  ungetc(str[N], stdin);
  
  // 文字列の長さがNよりも短い場合はエラー出力して強制終了
  for(int i=0; i<N; i++){
    if(str[i]=='\n' || str[i]==' ' || str[i]=='\0' || str[i]=='\r'){
      fprintf(stderr, "read_string_(): Invalid string\n");
      exit(1);
    }
  }
  
  // 文字列の長さがNよりも長い場合はエラー出力して強制終了
  if( !(str[N]=='\n' || str[N]==' ' || str[N]=='\0' || str[N]=='\r') ){
    fprintf(stderr, "read_string_(): Invalid string\n");
    exit(1);
  }
    
  // fgetsで改行かスペースも読み込んでいる場合があるので，ヌル文字で上書き
  str[N] = '\0';
}

```

+ 文字配列の要素N個をヌル文字で初期化する関数`zeros_`は次のように定義されている．

```
void zeros_(char* str,  int N){
  for (int i = 0; i < N; ++i){
    str[i] = '\0';  // 配列のi番目の要素をヌル文字で初期化
  }
}
```

+ 文字配列専用で二次元配列のメモリ確保する関数`malloc_2d_`は次のように定義されている．

```
int** malloc_2d_(
     const int len_x,
     const int len_y
){
  int** array_2d = (int **)malloc(sizeof(int *) * len_x);
  if(array_2d == NULL){
    fprintf(stderr, "malloc_2d_(): Cannot allocate memory.\n");
    exit(1);
  }
  for(int i = 0; i < len_x; ++i){
    array_2d[i] = (int*)malloc(sizeof(int) * len_y);
    if(array_2d[i] == NULL){
      fprintf(stderr, "malloc_2d_(): Cannot allocate memory.\n");
      exit(1);
    }
  }
  return array_2d;
}
```

+ 二次元配列を解放する関数`free_2d_`は次のように定義されている．

```
void free_2d_(int **array_2d, int len_x){
  for(int i = 0; i < len_x; ++i) free(array_2d[i]);
  free(array_2d);
}
```




### 三項演算子<a name="ternary_operator"></a>
---
- 関数`vmax_`等で用いられている`(条件式) ? (真式) : (偽式)`という記法は，三項演算子と呼ばれ，(条件式)が真であれば(真式)を，偽であれば(偽式)を評価して値を返す．例えば`vmax_`は以下と等価である：

  ```
  int vmax_(int x, int y){
   if( x > y ){
     return x;
   }
    else {
      return y;
    }
  }
  ```
 
- 簡単な式であればよいが，カッコ書きや三項演算子を入れ子にするような複雑な式の場合は，if文を使用した方が見やすい：

  ```
  d = (a>b) ? ((b>c) ? c : b) : ((a>c) ? c : a );
  
  if( a > b ){
    if( b > c ) d = c;
    else d = b;
  }
  else {
    if( a > c ) d = c;
    else d = a;
  }
  ```
  
- 「真偽判定の結果に応じて異なる値を代入する」という処理はわりと登場頻度が高いので，C言語では演算子としてサポートされている．（もともと導入された経緯としては，Intelプロセッサなどで提供している"conditional move"などの条件付き命令を積極的に用いるためというのも一つある．）


---
## 参考文献
---

+ T. コルメン, R. リベスト, C. シュタイン, C. ライザーソン．アルゴリズムイントロダクション 第3版 総合版．近代科学社，2013年．
