# CodeQL issue report 

Given a large number of founding from testing CodeQL, we only listed and reported two types of FNs and two types of FPs we were able to generalize and reproduce manually in most of the related seed-QL pairs. We expect more findings to be updated after we received responses from developers regarding root cause, patch commit, etc.

Version affected:

CLI: https://github.com/github/codeql-cli-binaries/releases/download/v2.8.1/codeql-linux64.zip
QL Pack: https://github.com/github/codeql/archive/refs/tags/codeql-cli/v2.8.1.zip


## False Negative (FN)

### Issue 1

Issue: It seems that when changing a local variable to a global variable, the taint on that variable gones. 

Query affected: ArithmeticTainted

Change applied to the code: 

```c=
4,17d3
< #include <algorithm>
< #include <cstdint>
< #include <cstdlib>
< #include <stdio.h>
< #include <string.h>
< void *calloc(size_t nitems, size_t size);
< 
< int T;
< // GLOBAL_HERE
< 
< // FUNC_HERE
< 
< // EXP_HERE
< 
21c7
<   int tcase = 0;
---
>   int T, tcase = 0;

```

Expected result:

```
"User-controlled data in arithmetic expression","Arithmetic operations on user-controlled data that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///7a8e97ae5d7327b103dd5eb898147096.cpp:8:15:8:16""]] flows to here and is used in arithmetic, potentially causing an underflow.","/7a8e97ae5d7327b103dd5eb898147096.cpp","10","10","10","10"
```

FN result:

```
<EMPTY>
```

Detailed program (this works as expected)

```c=
#include <cstdio>
#include <iostream>

using namespace std;

int main() {
  int T, tcase = 0;
  scanf("%d", &T);

  while (T--) {
    int S;
    scanf("%d", &S);

    char audi[S + 10];
    scanf("%s", audi);

    int invited = 0, claping = (audi[0] - '0');

    for (int i = 1; i <= S; i++) {
      if (claping < i) {
        invited += (i - claping);
        claping = i;
      }

      claping += (audi[i] - '0');
    }

    printf("Case #%d: %d\n", ++tcase, invited);
  }
}
```

However, when changing the local variable to a global variable (as follows), it becomes specious.

```c=
#include <cstdio>
#include <iostream>

#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <stdio.h>
#include <string.h>
void *calloc(size_t nitems, size_t size);

int T;
// GLOBAL_HERE

// FUNC_HERE

// EXP_HERE

using namespace std;

int main() {
  int tcase = 0;
  scanf("%d", &T);

  while (T--) {
    int S;
    scanf("%d", &S);

    char audi[S + 10];
    scanf("%s", audi);

    int invited = 0, claping = (audi[0] - '0');

    for (int i = 1; i <= S; i++) {
      if (claping < i) {
        invited += (i - claping);
        claping = i;
      }

      claping += (audi[i] - '0');
    }

    printf("Case #%d: %d\n", ++tcase, invited);
  }
}
```

### Issue 2

Issue: Missing taint information when ++ or -- changed to +=1 or -=1

Query affected: ImproperArrayIndexValidation

Change applied to the code: 

```c=
39,41c39
< 
<       st--, ed -= 1;
< 
---
>       st--, ed--;
```

Expected result:

```
"Unclear validation of array index","Accessing an array without first checking that the index is within the bounds of the array can cause undefined behavior and can also be a security risk.","warning","[[""User-provided value""|""relative:///8611af3341b66d8844ae02499ac613f1.cpp:38:21:38:23""]] flows to here and is used in an array indexing expression, potentially causing an invalid access.","/8611af3341b66d8844ae02499ac613f1.cpp","45","10","45","11"
"Unclear validation of array index","Accessing an array without first checking that the index is within the bounds of the array can cause undefined behavior and can also be a security risk.","warning","[[""User-provided value""|""relative:///8611af3341b66d8844ae02499ac613f1.cpp:38:21:38:23""]] flows to here and is used in an array indexing expression, potentially causing an invalid access.","/8611af3341b66d8844ae02499ac613f1.cpp","45","14","45","15"
"Unclear validation of array index","Accessing an array without first checking that the index is within the bounds of the array can cause undefined behavior and can also be a security risk.","warning","[[""User-provided value""|""relative:///8611af3341b66d8844ae02499ac613f1.cpp:38:21:38:23""]] flows to here and is used in an array indexing expression, potentially causing an invalid access.","/8611af3341b66d8844ae02499ac613f1.cpp","46","12","46","13"
"Unclear validation of array index","Accessing an array without first checking that the index is within the bounds of the array can cause undefined behavior and can also be a security risk.","warning","[[""User-provided value""|""relative:///8611af3341b66d8844ae02499ac613f1.cpp:38:26:38:28""]] flows to here and is used in an array indexing expression, potentially causing an invalid access.","/8611af3341b66d8844ae02499ac613f1.cpp","63","27","63","28"
```

FN result:

```
"Unclear validation of array index","Accessing an array without first checking that the index is within the bounds of the array can cause undefined behavior and can also be a security risk.","warning","[[""User-provided value""|""relative:///8611af3341b66d8844ae02499ac613f1.cpp:38:21:38:23""]] flows to here and is used in an array indexing expression, potentially causing an invalid access.","/8611af3341b66d8844ae02499ac613f1.cpp","47","10","47","11"
"Unclear validation of array index","Accessing an array without first checking that the index is within the bounds of the array can cause undefined behavior and can also be a security risk.","warning","[[""User-provided value""|""relative:///8611af3341b66d8844ae02499ac613f1.cpp:38:21:38:23""]] flows to here and is used in an array indexing expression, potentially causing an invalid access.","/8611af3341b66d8844ae02499ac613f1.cpp","47","14","47","15"
"Unclear validation of array index","Accessing an array without first checking that the index is within the bounds of the array can cause undefined behavior and can also be a security risk.","warning","[[""User-provided value""|""relative:///8611af3341b66d8844ae02499ac613f1.cpp:38:21:38:23""]] flows to here and is used in an array indexing expression, potentially causing an invalid access.","/8611af3341b66d8844ae02499ac613f1.cpp","48","12","48","13"
```

The original program (which works as expected)

```c=
// hi
#include <bits/stdc++.h>
using namespace std;
#define PB push_back
#define MP make_pair
#define F first
#define S second
#define inf 10000000000000
typedef long long int LL;
struct P {
  int e, s;
} c[102];
LL mp[102][102];
double dp[102][102];
double best[102];
int main(void) {
  int t;
  scanf("%d", &t);
  for (int hh = 1; hh <= t; hh++) {
    int n, q;
    scanf("%d%d", &n, &q);
    int i, j, k;
    for (i = 0; i < n; i++)
      scanf("%d%d", &c[i].e, &c[i].s);
    for (i = 0; i < n; i++)
      for (j = 0; j < n; j++) {
        scanf("%lld", &mp[i][j]);
        if (mp[i][j] == -1)
          mp[i][j] = inf;
      }
    for (k = 0; k < n; k++)
      for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
          mp[i][j] = min(mp[i][j], mp[i][k] + mp[k][j]);
    printf("Case #%d: ", hh);
    for (int gg = 0; gg < q; gg++) {
      int st, ed;
      scanf("%d%d", &st, &ed);
      st--, ed--;
      for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
          dp[i][j] = (double)inf;
      for (i = 0; i < n; i++)
        best[i] = (double)inf;
      dp[st][st] = 0.0;
      best[st] = 0;
      for (int ww = 0; ww < n; ww++) {
        for (j = 0; j < n; j++) {
          if (j == st)
            continue;
          for (i = 0; i < n; i++) {
            if (j == i)
              continue;
            if (mp[i][j] <= c[i].e)
              dp[j][i] = best[i] + (double)mp[i][j] / c[i].s;
            // printf("%d %d: %lf\n",j,i,dp[j][i]);
          }
          for (i = 0; i < n; i++)
            best[j] = min(best[j], dp[j][i]);
          // printf("%d %lf\n",j,best[j]);
        }
      }
      printf("%lf ", best[ed]);
    }
    printf("\n");
  }
  return 0;
}
```

The mutated programs.

```c=
// hi
#include <bits/stdc++.h>
using namespace std;
#define PB push_back
#define MP make_pair
#define F first
#define S second
#define inf 10000000000000
typedef long long int LL;
struct P {
  int e, s;
} c[102];
LL mp[102][102];
double dp[102][102];
double best[102];
int main(void) {
  int t;
  scanf("%d", &t);
  for (int hh = 1; hh <= t; hh++) {
    int n, q;
    scanf("%d%d", &n, &q);
    int i, j, k;
    for (i = 0; i < n; i++)
      scanf("%d%d", &c[i].e, &c[i].s);
    for (i = 0; i < n; i++)
      for (j = 0; j < n; j++) {
        scanf("%lld", &mp[i][j]);
        if (mp[i][j] == -1)
          mp[i][j] = inf;
      }
    for (k = 0; k < n; k++)
      for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
          mp[i][j] = min(mp[i][j], mp[i][k] + mp[k][j]);
    printf("Case #%d: ", hh);
    for (int gg = 0; gg < q; gg++) {
      int st, ed;
      scanf("%d%d", &st, &ed);

      st--, ed -= 1;

      for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
          dp[i][j] = (double)inf;
      for (i = 0; i < n; i++)
        best[i] = (double)inf;
      dp[st][st] = 0.0;
      best[st] = 0;
      for (int ww = 0; ww < n; ww++) {
        for (j = 0; j < n; j++) {
          if (j == st)
            continue;
          for (i = 0; i < n; i++) {
            if (j == i)
              continue;
            if (mp[i][j] <= c[i].e)
              dp[j][i] = best[i] + (double)mp[i][j] / c[i].s;
            // printf("%d %d: %lf\n",j,i,dp[j][i]);
          }
          for (i = 0; i < n; i++)
            best[j] = min(best[j], dp[j][i]);
          // printf("%d %lf\n",j,best[j]);
        }
      }
      printf("%lf ", best[ed]);
    }
    printf("\n");
  }
  return 0;
}
```


## False Positives.

### Issue 1

Issue: The mutated expression won't trigger any overflow, given that it will be reset to original value in the next line

Query affected: IntegerOverflowTainted

Change applied to the code: 

```c=
< #include <algorithm>
< #include <cstdint>
< #include <cstdlib>
< #include <stdio.h>
< #include <string.h>
< void *calloc(size_t nitems, size_t size);
< 
< 
19,21c11
< 
<   int from = (n - 1) | 1;
<   from = from == n ? from : n;
```

Expected result:

```
"Potential integer arithmetic overflow","A user-controlled integer arithmetic expression that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///4217db11a508e0e624baa7f06ac91672.cpp:22:18:22:19""]] flows to here and is used in an expression which might overflow negatively.","/4217db11a508e0e624baa7f06ac91672.cpp","13","26","13","30"
"Potential integer arithmetic overflow","A user-controlled integer arithmetic expression that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///4217db11a508e0e624baa7f06ac91672.cpp:22:18:22:19""]] flows to here and is used in an expression which might overflow.","/4217db11a508e0e624baa7f06ac91672.cpp","14","5","14","13"
"Potential integer arithmetic overflow","A user-controlled integer arithmetic expression that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///4217db11a508e0e624baa7f06ac91672.cpp:22:18:22:19""]] flows to here and is used in an expression which might overflow negatively.","/4217db11a508e0e624baa7f06ac91672.cpp","16","9","16","13"
```

FP result:

```
"Potential integer arithmetic overflow","A user-controlled integer arithmetic expression that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///4217db11a508e0e624baa7f06ac91672.cpp:40:18:40:19""]] flows to here and is used in an expression which might overflow negatively.","/4217db11a508e0e624baa7f06ac91672.cpp","27","15","27","19"
"Potential integer arithmetic overflow","A user-controlled integer arithmetic expression that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///4217db11a508e0e624baa7f06ac91672.cpp:40:18:40:19""]] flows to here and is used in an expression which might overflow negatively.","/4217db11a508e0e624baa7f06ac91672.cpp","31","26","31","30"
"Potential integer arithmetic overflow","A user-controlled integer arithmetic expression that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///4217db11a508e0e624baa7f06ac91672.cpp:40:18:40:19""]] flows to here and is used in an expression which might overflow.","/4217db11a508e0e624baa7f06ac91672.cpp","32","5","32","13"
"Potential integer arithmetic overflow","A user-controlled integer arithmetic expression that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///4217db11a508e0e624baa7f06ac91672.cpp:40:18:40:19""]] flows to here and is used in an expression which might overflow negatively.","/4217db11a508e0e624baa7f06ac91672.cpp","34","9","34","13"
```

The original program, which works fine.

```c=
#include <bits/stdc++.h>

using namespace std;

vector<pair<int, int>> ans;

void solve(int n, int m) {
  if (m == 1 || n == 1) {
    return;
  }
  int from = n;
  for (int i = 1; i < m; i++) {
    ans.push_back({from, n - 1});
    from += n;
  }
  solve(n - 1, m);
}

void test() {
  ans.clear();
  int n, m;
  scanf("%d %d", &n, &m);
  solve(n, m);
  printf("%d\n", ans.size());
  for (auto p : ans) {
    printf("%d %d\n", p.first, p.second);
  }
}

int main() {

  int tests;
  scanf("%d", &tests);
  for (int t = 1; t <= tests; t++) {
    printf("Case #%d: ", t);
    test();
  }

  return 0;
}

```

Mutated samples, which are specious.

```c=
#include <bits/stdc++.h>

#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <stdio.h>
#include <string.h>
void *calloc(size_t nitems, size_t size);


using namespace std;

vector<pair<int, int>> ans;

void solve(int n, int m) {
  if (m == 1 || n == 1) {
    return;
  }

  int from = (n - 1) | 1;
  from = from == n ? from : n;
  for (int i = 1; i < m; i++) {
    ans.push_back({from, n - 1});
    from += n;
  }
  
  solve(n - 1, m);
}

void test() {
  ans.clear();
  int n, m;
  scanf("%d %d", &n, &m);
  solve(n, m);
  printf("%d\n", ans.size());
  for (auto p : ans) {
    printf("%d %d\n", p.first, p.second);
  }
}

int main() {

  int tests;
  scanf("%d", &tests);
  for (int t = 1; t <= tests; t++) {
    printf("Case #%d: ", t);
    test();
  }

  return 0;
}
```


### Issue 2

Issue: The arith operation doesn't controllable by user in this spot

Query affected: ArithmeticTainted

Change applied to the code: 

```c=
46d45
< 
48,56d46
<     int *var_5386739 = &n;
<     int *var_7228574 = &n;
<     int *var_10026374 = &n;
<     int *var_15227508 = &n;
<     *var_5386739 = 1;
<     if (*var_5386739 + *var_7228574 + *var_10026374 + *var_15227508 == 4) {
<       *var_5386739 = *var_7228574 ^ *var_10026374;
<     }
< 
```

Expected result:

```
"User-controlled data in arithmetic expression","Arithmetic operations on user-controlled data that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///27053934e8206ce4b25a1c70aebd7c11.cpp:36:33:36:39""]] flows to here and is used in arithmetic, potentially causing an overflow.","/27053934e8206ce4b25a1c70aebd7c11.cpp","42","25","42","25"
"User-controlled data in arithmetic expression","Arithmetic operations on user-controlled data that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///27053934e8206ce4b25a1c70aebd7c11.cpp:36:33:36:39""]] flows to here and is used in arithmetic, potentially causing an overflow.","/27053934e8206ce4b25a1c70aebd7c11.cpp","42","46","42","46"
"User-controlled data in arithmetic expression","Arithmetic operations on user-controlled data that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///27053934e8206ce4b25a1c70aebd7c11.cpp:36:33:36:39""]] flows to here and is used in arithmetic, potentially causing an overflow.","/27053934e8206ce4b25a1c70aebd7c11.cpp","42","56","42","56"
```

FP result:

```
"User-controlled data in arithmetic expression","Arithmetic operations on user-controlled data that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///27053934e8206ce4b25a1c70aebd7c11.cpp:57:17:57:18""]] flows to here and is used in arithmetic, potentially causing an overflow.","/27053934e8206ce4b25a1c70aebd7c11.cpp","53","9","53","20"
"User-controlled data in arithmetic expression","Arithmetic operations on user-controlled data that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///27053934e8206ce4b25a1c70aebd7c11.cpp:57:17:57:18""]] flows to here and is used in arithmetic, potentially causing an overflow.","/27053934e8206ce4b25a1c70aebd7c11.cpp","53","24","53","35"
"User-controlled data in arithmetic expression","Arithmetic operations on user-controlled data that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///27053934e8206ce4b25a1c70aebd7c11.cpp:57:17:57:18""]] flows to here and is used in arithmetic, potentially causing an overflow.","/27053934e8206ce4b25a1c70aebd7c11.cpp","53","39","53","51"
"User-controlled data in arithmetic expression","Arithmetic operations on user-controlled data that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///27053934e8206ce4b25a1c70aebd7c11.cpp:57:17:57:18""]] flows to here and is used in arithmetic, potentially causing an overflow.","/27053934e8206ce4b25a1c70aebd7c11.cpp","53","55","53","67"
"User-controlled data in arithmetic expression","Arithmetic operations on user-controlled data that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///27053934e8206ce4b25a1c70aebd7c11.cpp:62:33:62:39""]] flows to here and is used in arithmetic, potentially causing an overflow.","/27053934e8206ce4b25a1c70aebd7c11.cpp","74","40","74","40"
"User-controlled data in arithmetic expression","Arithmetic operations on user-controlled data that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///27053934e8206ce4b25a1c70aebd7c11.cpp:62:33:62:39""]] flows to here and is used in arithmetic, potentially causing an overflow.","/27053934e8206ce4b25a1c70aebd7c11.cpp","74","50","74","50"
"User-controlled data in arithmetic expression","Arithmetic operations on user-controlled data that is not validated can cause overflows.","warning","[[""User-provided value""|""relative:///27053934e8206ce4b25a1c70aebd7c11.cpp:62:33:62:39""]] flows to here and is used in arithmetic, potentially causing an overflow.","/27053934e8206ce4b25a1c70aebd7c11.cpp","75","22","75","32"
```

The original program, which works fine.

```c=
#include <algorithm>
#include <bitset>
#include <iostream>
#include <list>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <string.h>
#include <utility>
#include <vector>

#include <cctype>
#include <cmath>
#include <cstdio>

#include <cstdint>
#include <cstdlib>
#include <stdio.h>
void *calloc(size_t nitems, size_t size);

size_t var_15771409 = -1;
size_t var_12127028 = 1;
// GLOBAL_HERE

unsigned int func_9326() { return var_15771409 % var_12127028; }

// FUNC_HERE

// EXP_HERE

using namespace std;

#define rep(i, a, b) for (__typeof(b) i = a; i < (b); ++i)
#define trav(it, c)                                                            \
  for (__typeof((c).begin()) it = (c).begin(); it != (c).end(); ++it)

typedef long long ll;
typedef pair<int, int> pii;
typedef vector<int> vi;
int_least32_t main() {
  int tt;
  scanf("%d", &tt);
  rep(sd, 0, tt) {
    int n;
    scanf("%d", &n);
    vi hold(n, 1234567890);
    hold[0] = 0;
    vi pos(n), len(n);
    bool ok = false;
    rep(i, 0, n) scanf("%d %d", &pos[i], &len[i]);
    int D;
    scanf("%d", &D);

    int can_reach = func_9326();
    rep(i, 0, n) {

      int var_4623995;
      while (var_4623995 = pos[i]) {
        break;
      }

      int var_7119789 = min(len[i], pos[i] - hold[i]);
      int max_dist = var_4623995 + var_7119789;

      if (max_dist >= D)
        ok = true;
      rep(j, can_reach + 1, n) {
        if (max_dist < pos[j])
          break;
        hold[j] = pos[i];
        can_reach = j;
      }
    }

    printf("Case #%d: %s\n", sd + 1, (ok ? "YES" : "NO"));
  }
}
```

Mutated samples, which are specious

```c=
#include <algorithm>
#include <bitset>
#include <iostream>
#include <list>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <string.h>
#include <utility>
#include <vector>

#include <cctype>
#include <cmath>
#include <cstdio>

#include <cstdint>
#include <cstdlib>
#include <stdio.h>
void *calloc(size_t nitems, size_t size);

size_t var_15771409 = -1;
size_t var_12127028 = 1;
// GLOBAL_HERE

unsigned int func_9326() { return var_15771409 % var_12127028; }

// FUNC_HERE

// EXP_HERE

using namespace std;

#define rep(i, a, b) for (__typeof(b) i = a; i < (b); ++i)
#define trav(it, c)                                                            \
  for (__typeof((c).begin()) it = (c).begin(); it != (c).end(); ++it)

typedef long long ll;
typedef pair<int, int> pii;
typedef vector<int> vi;
int_least32_t main() {
  int tt;
  scanf("%d", &tt);
  rep(sd, 0, tt) {

    int n;
    int *var_5386739 = &n;
    int *var_7228574 = &n;
    int *var_10026374 = &n;
    int *var_15227508 = &n;
    *var_5386739 = 1;
    if (*var_5386739 + *var_7228574 + *var_10026374 + *var_15227508 == 4) {
      *var_5386739 = *var_7228574 ^ *var_10026374;
    }

    scanf("%d", &n);
    vi hold(n, 1234567890);
    hold[0] = 0;
    vi pos(n), len(n);
    bool ok = false;
    rep(i, 0, n) scanf("%d %d", &pos[i], &len[i]);
    int D;
    scanf("%d", &D);

    int can_reach = func_9326();
    rep(i, 0, n) {

      int var_4623995;
      while (var_4623995 = pos[i]) {
        break;
      }

      int var_7119789 = min(len[i], pos[i] - hold[i]);
      int max_dist = var_4623995 + var_7119789;

      if (max_dist >= D)
        ok = true;
      rep(j, can_reach + 1, n) {
        if (max_dist < pos[j])
          break;
        hold[j] = pos[i];
        can_reach = j;
      }
    }

    printf("Case #%d: %s\n", sd + 1, (ok ? "YES" : "NO"));
  }
}
```
