---
layout: page
title: 3-0. 文字列間の共通文字列挙（課題説明用）
---

---
## 問題
---
与えられた文字列$X$と$Y$に共通して出現する文字を辞書順に列挙せよ

---
## <font color="red">！！重要！！　課題全体を通しての仕様</font>
---

課題を通しての仕様を説明する (各設問で追加の仕様や注意書きがある場合はそちらを優先する)．

- グローバル変数や静的変数を使用してはいけない．
- `include`するファイルは`<stdio.h>`および`<stdlib.h>`のみとする．
- プログラム全体の構成を以下に従うようにする．
  - `main`関数の正常終了時の戻り値0にする．
  - 関数の前方宣言を用い，関数本体は`main`関数の下に記述する．
    ```
      #include <stdio.h>
      #include <stdlib.h>

        ... 事前に与えられる関数の定義 ...

      //////

        ... 課題ごとの関数前方宣言 ...

      int main()
      {

        ...（main関数本体）...

        return 0;
      }

        ... 課題ごとの関数本体 ...
      ```
  - ただし，課題ごとに与えられるコードを記載する場所は，それぞれの指示に従う．

- ~~変数の宣言は関数の先頭でおこなうこと (途中の宣言は不可とする)~~ C99 より前（ANSI C まで）のかなり古いC言語では、変数の宣言はブロック（ `{}` ）の先頭であることを求められていたが、現行の C ではこれは不要である.

- 入力データの読み込み
  - 入力データの読み込は`main` 関数内で行うこと．
  + 入力用の文字列$X$や$Y$は標準入力から与えられる
  + 各文字列は空白文字（スペースや改行）で区切られる．
  + 文字数は20以下であると仮定してよい．


- 事前に定義されている関数(基本的に関数名の最後に`_`がついているもの)の中身を書き換えてはいけない．これらの関数は例えば，`printf`や`scanf`と同様に中身を書き換えられない関数として扱うこと．

- 表示例の`⊔` は半角スペース，`↩︎`は改行を表す．
- 表示(出力)
  - 全ての表示は標準出力にすること．ただし，標準エラー出力への表示が必要な場合は各課題の仕様に記載する．
  - 全ての出力には改行文字 `\n` を付けること．特に最後の行の改行の有無に注意すること．
  - 各要素の間には空白文字を一つ入れる．
  - 改行前の空白文字などの表示されない文字を出力しないこと．


+ 値の大小関係を取得
  + 2または3つの整数の最大，最小値を取得したい場合に以下の関数を用いること．
  + 以下の関数が不要な場合は使わなくても良い．ただし同様の関数を再定義することは不可とする．
  + 2つの値のうち小さい方の値を取得する場合
    + `vmin_`を使う
    ```
    int vmin_(int a, int b);
    ```
    + 例；`vmin_(1 ,3 )` なら戻り値は`1`
  + 2つの値のうち大きい方の値を取得する場合
    + `vmax_`を使う
    ```
    int vmax_(int a, int b);
    ```
    + 例：`vmax_(2 ,3 )` なら戻り値は`3`
  + 3つの値のうち最も小さい値を取得する場合
    + `vmin3_`を使う
    ```
    int vmin3_(int a, int b，int c);
    ```
    + 例：`vmin3_(2, 1, 3)` なら戻り値は`1`
  + 3つの値のうち最も大きい値を取得する場合
    + `vmax3_`を使う
    ```
    int vmax3_(int a, int b，int c);
    ```
    + 例：`vmax3_(3, 2 ,1)` なら戻り値は`3`

+ 事前に定義された関数として以下の処理には対応する関数を用いること
  + 文字列用のメモリ確保と標準入力からの文字列読み込み
    + 関数 `read_string_`を用いること
      ```
      char* read_string_(int N);
      ```
    + 引数は，読み込む文字列の最大長
    + 戻り値は，読み込んだ文字列の先頭を指すポインタ

  + 文字列の長さの取得
    + 関数 `count_len_`を用いること
      ```
      int count_len_(char *X);
      ```
    + 引数は，長さを計測したい文字列$X$
    + 戻り値は，文字列$X$の長さ

  + 文字列用の配列を`\0`で初期化
    + 関数 `zoros_`を用いること
      ```
      void zeros_(char* data,  int N);
      ```
    + 引数は，初期化したい文字列$X$と文字列＄X$の長さ

---
### 仕様
---
+ 上記課題全体の仕様


+ 文字列$X$，文字列$X$の先頭から$M$文字目の場所を表すインデックス$M$，文字列$Y$，文字列$Y$の先頭から$N$文字目の場所を表すインデックス$N$, マッチした文字を保存する配列`buf`の5つを引数にとり，マッチした数を返す関数`find_matching`を作成すること
  + 例：
  ```
  int find_matching(char *X, int M, char *Y, int N, char *buf);
  ```

+ マッチした文字をソートする関数`sort_buf`を用いること．
  + 引数に，文字の配列`buf`と個数`n`をとること．
  + 例：
  ```
  int sort_buf(char *buf, int N);
  ```

+ 標準出力に以下の出力をする．
  + 1行目に入力文字列$X$とその長さを表示する．
  + 2行目に入力文字列$Y$とその長さを表示する．
  + 3行目以降にマッチした文字を辞書順に1行1文字で表示する．
    + 余計な空白などは入れないこと．


＋ 以下のプログラムを必ず用いてプログラムを完成せること．
  + `???`の部分に必ずコメントを入れること．

```
#include <stdio.h>
#include <stdlib.h>

int vmax_(int x, int y) { return x > y ? x : y; }                  // ???
int vmax3_(int a, int b, int c) { return vmax_(a, vmax_(b, c)); }  // ???
int vmin_(int x, int y) { return x < y ? x : y; }                  // ???
int vmin3_(int a, int b, int c) { return vmin_(a, vmin_(b, c)); }  // ???

void zeros_(     // 文字列用の配列を\0で初期化する関数
    char* data,  // 文字列を格納する配列
    int N        // 文字列の長さ
) {
  for (int i = 0; i < N; ++i) {
    data[i] = '\0';  // 配列のi番目の要素を\0で初期化
  }
}

char* read_string_(  // 文字列用のメモリ確保と、標準入力からの文字列読み込みを行う関数
    const int N      // 文字列の長さ
) {
  char* data = (char*)malloc(N * sizeof(char));  // 配列に動的メモリを割り当てる
  if (data == NULL) {                            // メモリ確保に失敗した際のエラー処理 
    printf("Can not allocate memory. 'data' is NULL.\n");
    exit(1);  // メモリ確保に失敗したら、プログラムを終了
  }
  zeros_(data, N);            // 配列dataを関数zeros_で初期化
  scanf("%s", data);          // 文字列を読み込む
  if (data[N - 1] != '\0') {  // 文字列が21以上の場合のエラー処理
    printf("Reading invalid string\n");
    exit(1);  // プログラムを終了
  }
  return data;  // 配列dataの先頭のポインタを返す
}

int count_len_(        // 文字列の長さを計算する関数
    const char* array  // 文字列用の配列
) {
  int ri = 0;
  while (array[ri] != '\0') {  // ???
    ri++;
  }
  return ri;  // 文字列の長さriを返す
}


int find_matching(char* X, int M, char* Y, int N, char* buf);
void sort_buf(char* buf, int N);


int main() {
  int N = 21;                      // ???
  char* data_x = read_string_(N);  // 1つ目の文字列をdata_xに格納
  char* data_y = read_string_(N);  // 2つ目の文字列をdata_yに格納
  int len_x = count_len_(data_x);  // data_xに格納した文字列の長さを取得
  int len_y = count_len_(data_y);  // data_yに格納した文字列の長さを取得
  char buf[len_x * len_y];   // マッチングした文字列を保存する配列bufの宣言

  int cnt = find_matching(data_x, len_x, data_y, len_y, buf);  // find_matching関数を実行
  sort_buf(buf, cnt);                                          // sort_buf関数を実行

  printf("%s %d\n", data_x, len_x);  // data_xに格納した文字列とその長さをSTDOUTに出力
  printf("%s %d\n", data_y, len_y);  // data_yに格納した文字列とその長さをSTDOUTに出力

  char prev = '\0';                // 変数prevを\0で初期化
  for (int i = 0; i < cnt; ++i) {  // i=0からi=cnt-1まで繰り返す
    if (prev == buf[i]) continue;  // prev == buf[i]ならばスキップ
    printf("%c\n", buf[i]);        // buf[i]を出力
    prev = buf[i];                 // prevにbuf[i]を代入
  }
  free(data_x);  // 動的に確保された配列data_xの開放 
  free(data_y);  // 動的に確保された配列data_yの開放 
  return 0;      // プログラムの正常終了
}


int find_matching(  // ???
    char* X,        // ???
    int M,          // ???
    char* Y,        // ???
    int N,          // ???
    char* buf       // ???
) {
  int cnt = 0;  // ???
  for (int i = 0; i < M; ++i) {
    for (int j = 0; j < N; ++j) {
      // ???
      if (X[i] == Y[j]) {  // ???
        buf[cnt] = X[i];   // ???
        cnt++;             // ???
      }
    }
  }
  return cnt;  // ???
}


void sort_buf(  // ???
    char* buf,  // ???
    int N       // ???
) {
  for (int i = 0; i < N; ++i) {
    for (int j = 1; j < N - i; ++j) {
      // ???
      if (buf[j] < buf[j - 1]) {
        char tmp = buf[j];    // ???
        buf[j] = buf[j - 1];  // ???
        buf[j - 1] = tmp;     // ???
      }
    }
  }
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
eat ate
```

+ 出力
```
eat 3
ate 3
a
e
t
```

---
### 例（2）
---

+ 入力
```
abababab abababc
```

+ 出力
```
abababab 8
abababc 7
a
b
```





### 参考文献
