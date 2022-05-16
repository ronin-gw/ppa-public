---
layout: page
title: 3-3. 編集距離(再帰+メモ化)【基本】
---


---
## メモ化
---
問題 3-2 のプログラムでは，文字列 $X$ と $Y$ の編集距離 $c_{m,n}$ を，与えられた文字列長から順に遡って再帰的に計算した．しかし，この方法では，同じ値を複数回計算してしまう可能性があるため，効率面で問題がある．
本問題では，再帰処理を効率的に行う手法として**メモ化(memoization)**について学ぶ.

メモ化の考えは非常に単純であり,

  + $c_{m,n}$ を求める過程で，一度計算した $c_{i,j}$の値をメモリに保存する.
  + 再び必要になった時は再帰呼び出しを行わず，以前求めて保存してあった $c_{i,j}$ の値を再利用する.
  
このような処理をメモ化と呼ぶ.
これにより，一度計算したものを再び計算する必要がないため，計算量は指数関数的に改善される.



---
## 問題
---


問題3-2で実装したプログラムにメモ化を導入し，メモ化ありの場合とメモ化なしの場合の再帰関数の呼び出し回数を求めよ.

なお，メモ化あり場合は，再帰関数の呼び出し回数が最小となるように実装せよ．


---
### 仕様
---
+ 課題3-2に記載の仕様．ただし，「以下のプログラムを必ず用いてプログラムを完成させること」の部分は除く．

+ 問題3-2で実装した再帰関数をベースに，メモ化を導入せよ．関数名は`ldmemo`とする．この関数は，文字列$X$，文字列$X$の先頭から$m$文字目の場所を表すインデックス$m$，文字列$Y$，文字列$Y$の先頭から$n$文字目の場所を表すインデックス$n$，メモを格納する2次元配列用テーブル memo の5つを引数にとり，編集距離を返すものとする．
  + 例：
  ```	
  int ldmemo(char *X, int m, char *Y, int n, int** memo);
  ```

+ 2次元配列の確保と開放には，`func_mallocation_2d_`関数と`func_free_2d_`関数をそれぞれ用いよ．
  + `func_mallocation_2d_`関数は，整数iと整数jを引数に取り，整数型の2次元配列（i行j列）を返す関数である．例えば，以下のように書くと，2次元配列arrayが確保出来る．
  ```	
  int** array = func_mallocation_2d_(i, j);　
  ```
  + `func_free_2d_`関数は，2次元配列arrayと配列の行数iを引数に取るvoid型の関数である．例えば，以下のように書くと，2次元配列arrayの開放を行う．
  ```	
  func_free_2d_(array, i);
  ```
  + これらの関数は，`ppa_extra_h/p3_header.h`においてある．`#include "ppa_extra_h/p3_header.h"`という宣言をする事で使用可能である．これらの関数の中身は，下の参考の所に書いたので，興味ある者は参照せよ．

+ `ld`と`delta`は問題3-2と同じものを使ってよい．

+ `memo`の大きさは，文字列の長さに合わせて必要十分な大きさとすること．

+ <font color="red">この問題に限り,再帰関数を呼び出した回数を求めるために,グローバル変数を用いること.</font>

+ 呼び出し回数を求めるためのグローバル変数は,各再帰関数の中で一回だけ使用し,インクリメント演算子あるいは1を足す演算のみを行うこと.

+ 表示：以下を標準出力に書き出せ.
  + 一行目：文字列$X$ とその長さ
  + 二行目：文字列$Y$ とその長さ
  + 三行目：メモ化なしの再帰関数`ld`で求めた $c_{m,n}$ の値とメモ化なしの再帰関数の呼び出し回数
  + 四行目：メモ化ありの再帰関数`ldmemo`で求めた $c_{m,n}$ の値とメモ化ありの再帰関数の呼び出し回数

+ 空文字列が入力された場合は,どちらの呼び出し回数もゼロとなるように実装すること.


+ 下の実行例(1)の場合
  ```
  eat⊔3↩︎
  ate⊔3↩︎
  2⊔94↩︎
  2⊔9↩︎
  ```

+ 以下のプログラムを必ず用いてプログラムを完成させること．
  + `???` の部分は適宜補完すること
  
```
#include <stdio.h>
#include <stdlib.h>

#include "ppa_extra_h/p3_header.h"

int count = 0;     // メモ化なしの再帰関数の呼び出し回数をカウントするグローバル変数
int countm = 0;    // メモ化ありの再帰関数の呼び出し回数をカウントするグローバル変数

int delta(char *X, int a, char *Y, int b);  // ???
int ld(char *X, int m, char *Y, int n);     // ???
int ldmemo(char *X, int m, char *Y, int n, int** memo);     // ???

int main() {
  int len_x, len_y ;                   // ???
  scanf(“%d”, &len_x);                 // ???
  scanf(“%d”, &len_y);                 // ???
  char* data_x = read_string_(len_x);  // ???
  char* data_y = read_string_(len_y);  // ???
  int** memo = func_mallocation_2d_(??, ??);     // ???
    
  ...(省略)...

  func_free_2d_(memo, ??);
  free(data_x);  // ???
  free(data_y);  // ???
  return 0;      // ???
}


int delta( ??? ) {

  ...(省略)...

};


int ld( ??? ) {

  ...(省略)...

}


int ldmemo( ??? ) {

  ...(省略)...

}
```


---
## 実行例
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
eat 3
ate 3
2 94
2 9
```

---
### 例（2）
---

+ 入力
```
4 4 tall twat
```

+ 出力
```
tall 4
twat 4
3 481
3 16
```

---
## ヒント
---

メモ化ありの場合の再帰関数は，以下の3ステップで実装せよ．

+ ステップ1：「編集距離を求める3つの操作に対し，最小のものを探索してからそれをメモする」ように実装する．例（1）と例（2）の出力は，それぞれ以下のようになる．
  + 例（1）
  ```
  eat 3
  ate 3
  2 94
  2 28
  ```

  + 例（2）
  ```
  tall 4
  twat 4
  3 481
  3 49
  ```

+ ステップ2：ステップ1のプログラムを「3つの操作に対し最小のものを探索する『前』にメモを参照する」ように改良する．
例（1）と例（2）の出力は，それぞれ以下のようになる．
  + 例（1）
  ```
  eat 3
  ate 3
  2 94
  2 16
  ```

  + 例（2）
  ```
  tall 4
  twat 4
  3 481
  3 25
  ```

+ ステップ3：ステップ2が正しく実装できると，文字列$X$の長さを$\ell_x$，文字列$Y$の長さを$\ell_y$とすると，再帰関数の呼び出し回数は$(\ell_x+1) \times (\ell_y+1)$になる．これを$\ell_x \times \ell_y$に減らすにはどうしたら良いかを考えよ．



---
## 参考
---
`func_mallocation_2d_`関数と`func_free_2d_`関数の中身は，それぞれ以下の通りである．

```
int** func_mallocation_2d_(const int len_x, const int len_y){
  int** array_2d = (int **)malloc(sizeof(int *) * len_x);
    if(array_2d == NULL){
        printf("Can not allocate memory. 'array_2d' is NULL.\n");
        exit(EXIT_FAILURE);
    }
    for(int i = 0; i < len_x; ++i){
        array_2d[i] = (int*)malloc(sizeof(int) * len_y);
        if(array_2d[i] == NULL){
            printf("Can not allocate memory. 'array_2d[i]' is NULL.\n");
            exit(EXIT_FAILURE);
        }
    }
    return array_2d;
}
```

```
void func_free_2d_(int **array_2d, int len_x){
  for(int i = 0; i < len_x; ++i) free(array_2d[i]);
 free(array_2d);
}
```
