<?php

include __DIR__ . '/render.php';

class Page
{
    private string $action;

    function __construct($action)
    {
        $this->action = $action;
    }

    function __destruct()
    {
        $this->{$this->action}();
    }

    function home()
    {
        include __DIR__ . '/pages/home.php';
    }

    function profile()
    {
        $render = new Render;
        $photo = $render->showProfilePhoto();
        include __DIR__ . '/pages/profile.php';
    }

    function contact()
    {
        include __DIR__ . '/pages/contact.php';
    }
}

class Contact
{
    private string $action;

    function __construct($action)
    {
        $this->action = $action;
    }

    function __destruct()
    {
        $this->{$this->action}();
    }

    function send()
    {
        $hasName = isset($_POST['name']);
        $hasBody = isset($_POST['body']);
        if ($hasName && $hasBody) {
            $body = $_POST['body'];

            $dirname = "/tmp/" . md5($_POST['name']) . time();
            if (!is_dir($dirname)) {
                mkdir($dirname);
            }
            
            $filename = md5(rand(100000000000, 999999999999)) . ".txt";

            file_put_contents($dirname . "/" . $filename, $body);

            echo "Berhasil Mengirimkan Pesan";
        } else {
            echo "Terjadi Kesalahan";
        }
    }
}

$hasModule = isset($_GET['module']);
$hasAction = isset($_GET['action']);

if ($hasModule && $hasAction) {
    $module = $_GET['module'];
    $action = $_GET['action'];

    try {
        new $module($action);
    } catch (Exception $e) {
        echo "Terjadi Kesalahan";
    }
} else {
    new Page('home');
}