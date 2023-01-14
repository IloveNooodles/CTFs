function calculator(txt: string): number|string {
  if (!check(txt)){
    return "Bad Hacker!";
  }
  return eval(txt);
}

const BLACK_LIST = ["Deno", ".", "\"", "'"]

function check(txt: string){
  for (const i in BLACK_LIST){
    if (txt.includes(BLACK_LIST[i])){
      return false
    }
  }
  return true
}

if (import.meta.main) {
  await Deno.readTextFile("logo").then((val) => {
    console.log(val);
  });
  console.log("aplikasi aritmatika by H3X0S1337");
  console.log("operasi yang bisa digunakan: ");
  console.log("- perkalian '*'");
  console.log("- pembagian '/'");
  console.log("- pertambahan '+'");
  console.log("- pengurangan '-'");
  console.log("- xor '^'");
  console.log("- modulus '%'");
  console.log("- pangkat '**'");
  console.log("- pembagian lantai '//'");
  console.log("contoh pemakaian:");
  console.log("- 1+1 maka akan menghasilkan 2");

  let buf: Uint8Array, user_input, hasil;
  while (true) {
    buf = new Uint8Array(1024);
    Deno.stdout.writeSync(new TextEncoder().encode("masukkan input: "));
    user_input = await Deno.stdin.read(buf).then((len) => {
      if (len) {
        return new TextDecoder().decode(buf.subarray(0, len));
      }
    });
    if (!user_input) {
      console.log("something wrong!");
      Deno.exit(1);
    }
    hasil = calculator(user_input);
    console.log(hasil);
  }
}
