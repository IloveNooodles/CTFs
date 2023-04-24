package io.github.nandandesai.pico.validators;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import java.io.File;

//validate path on the filesystem
public class PathConstraintValidator implements ConstraintValidator<ValidPath, String> {
    private Logger logger = LoggerFactory.getLogger(PathConstraintValidator.class);

    @Override
    public boolean isValid(String path, ConstraintValidatorContext context) {
        logger.info("Checking path validity");


        //also make checks to prevent directory traversal attacks


        return new File(path).isFile();
    }
}
