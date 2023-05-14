function ctoji(dec) {
  //map ascii printable characters to specific emoji faces
  if (dec == 32) {
    return String.fromCodePoint(128169);
  } else if (dec == 33) {
    return String.fromCodePoint(129488);
  } else if (dec == 34) {
    return String.fromCodePoint(129402);
  } else if (dec == 35) {
    return String.fromCodePoint(129400);
  } else if (dec == 36) {
    return String.fromCodePoint(129303);
  } else if (dec <= 39) {
    return String.fromCodePoint(dec + 128547);
  } else if (dec <= 43) {
    return String.fromCodePoint(dec + 128537);
  } else if (dec <= 49) {
    return String.fromCodePoint(dec + 129252);
  } else if (dec <= 105) {
    return String.fromCodePoint(dec + 128462);
  } else if (dec <= 111) {
    return String.fromCodePoint(dec + 129206);
  } else if (dec <= 120) {
    return String.fromCodePoint(dec + 129207);
  } else {
    return String.fromCodePoint(dec + 129271);
  }
}

function jitoc(dec) {
  if (dec == 128169) {
    return String.fromCodePoint(32);
  } else if (dec == 129488) {
    return String.fromCodePoint(33);
  } else if (dec == 129402) {
    return String.fromCodePoint(34);
  } else if (dec == 129400) {
    return String.fromCodePoint(35);
  } else if (dec == 129303) {
    return String.fromCodePoint(36);
  } else if (dec >= 129392) {
    return String.fromCodePoint(dec - 129271);
  } else if (dec >= 129319) {
    return String.fromCodePoint(dec - 129207);
  } else if (dec >= 129312) {
    return String.fromCodePoint(dec - 129206);
  } else if (dec >= 129296) {
    return String.fromCodePoint(dec - 129252);
  } else if (dec >= 128584) {
    return String.fromCodePoint(dec - 128547);
  } else if (dec >= 128577) {
    return String.fromCodePoint(dec - 128537);
  } else {
    return String.fromCodePoint(dec - 128462);
  }
}

let charset =
  "😐👴🤔_👽😐_🤯🤑👴🤔_🥶🔠😔🥵🤯🤖_👴😐🤥🥱_😐🤯🤯🤤_🤔👴_🍤🔠😐🤤_🤔🥵🤯_😔👽🤔🤔🤯🤖😐";

len = charset.length;

for (let i = 0; i < len; i++) {
  try {
    console.log(jitoc(charset[i]));
  } catch {}
}
