<?php

class Render
{
    function showProfilePhoto()
    {
        $location = __DIR__ . '/images/photo.jpg';
        $image = new Imagick($location);
        $image->thumbnailImage(200, 0);
        $thumbnail = $image->getImageBlob();
        return $thumbnail;
    }
}