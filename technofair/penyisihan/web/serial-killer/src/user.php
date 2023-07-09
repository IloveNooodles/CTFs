<?php

class User
{
    private $type;

    public function __construct(string $type)
    {
        $this->type = $type;
    }

    public function getType()
    {
        return $this->type;
    }
}

print_r(serialize(new User("admin")))

?>