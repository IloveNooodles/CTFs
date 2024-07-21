var fs = require('fs');

const data = fs.readFileSync('enc.txt', 'utf8');
arr = [];
for (let i = 0; i < data.length; i++) {
  arr.push(data.charCodeAt(i));
}

console.log(arr);

const flag = [];

arr.map((val, idx) => {
  if (!idx) {
    flag.push(val - 1);
  } else {
    for (let i = 0; i < 255; i++) {
      if ((i + arr[idx - 1]) % ((2 ** 9) << 16) === val) {
        flag.push(i);
        break;
      }
    }
  }
});

res = [];
for (let i = 0; i < flag.length; i++) {
  res.push(String.fromCharCode(flag[i]));
}

res = res.join('');
console.log(res);
