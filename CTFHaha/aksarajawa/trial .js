const read = (s) => s.reduce((a, b) => (a<<1)+b);

function argue(a, b, c){
  if((![]+[])[b-2*a] != 'a' ||
     ({}+[]).split(' ')[+[]][c-a] != 'b' ||
     ({}+[]).split(' ')[+[]][b-c] != 'c'){
       console.log('That\'s wrong!');
       return;
  }
  const ka = [a-read([+!![],+[],+!![]])] + [String.fromCharCode(b*10-a-c)] + [a-read([+!![]])];
  const kb = ['p'] + [({}[+[]]+[]).substring(+[], read([+!![],+[]]))] + [b-2*a] + ['hm'] + [c-a+ +!![]] + [({}[+[]]+[])[+!![]]] + [c - +!![]];
  const kc = [({}+[])[a]] + [c-a- +!![]] + ['m'] + [2*c - b];
  console.log(`Your flag: Arkav7{${ka}_${kb}_${kc}}`);
}
