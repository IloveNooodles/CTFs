const pass = [];

pass[0] = 52037;
pass[6] = 52081;
pass[5] = 52063;
pass[1] = 52077;
pass[9] = 52077;
pass[10] = 52080;
pass[4] = 52046;
pass[3] = 52066;
pass[8] = 52085;
pass[7] = 52081;
pass[2] = 52077;
pass[11] = 52066;

let pswd = '';

const password = Array.from(pass).map((a) => String.fromCharCode(a - 0xcafe));
for (let i = 0; i < password.length; i++) {
  pswd += password[i];
}

console.log(pswd);


// if (
//   p[0] === 52037 &&
//   p[6] === 52081 &&
//   p[5] === 52063 &&
//   p[1] === 52077 &&
//   p[9] === 52077 &&
//   p[10] === 52080 &&
//   p[4] === 52046 &&
//   p[3] === 52066 &&
//   p[8] === 52085 &&
//   p[7] === 52081 &&
//   p[2] === 52077 &&
//   p[11] === 52066
// ) {
//   window.location.replace(v + ".html");
// } else {
//   alert("Wrong password!");
// }
