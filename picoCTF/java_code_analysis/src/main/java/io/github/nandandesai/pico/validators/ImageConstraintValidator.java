package io.github.nandandesai.pico.validators;

import org.apache.commons.imaging.ImageInfo;
import org.apache.commons.imaging.ImageReadException;
import org.apache.commons.imaging.Imaging;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.multipart.MultipartFile;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import java.io.IOException;

public class ImageConstraintValidator implements ConstraintValidator<ValidImage, MultipartFile> {
    private Logger logger = LoggerFactory.getLogger(ImageConstraintValidator.class);

    @Override
    public boolean isValid(MultipartFile image, ConstraintValidatorContext context) {
        try {
            ImageInfo imageInfo = Imaging.getImageInfo(image.getBytes());
            logger.info("Image format: " + imageInfo.getFormat().getName());
            logger.info("Image height: " + imageInfo.getHeight());
            logger.info("Image width: " + imageInfo.getWidth());
            //maybe validate height and width here
        } catch (ImageReadException | IOException e) {
            context.buildConstraintViolationWithTemplate("File is not an image")
                    .addConstraintViolation()
                    .disableDefaultConstraintViolation();
            return false;
        }
        return true;
    }
}
