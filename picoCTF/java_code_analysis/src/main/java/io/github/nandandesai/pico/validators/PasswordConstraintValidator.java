package io.github.nandandesai.pico.validators;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/*
The following are the constraints of for the password:
* It contains at least 8 characters and at most 20 characters.
* It contains at least one digit.
* It contains at least one upper case alphabet.
* It contains at least one lower case alphabet.
* It contains at least one special character which includes !@#$%&*()-+=^.
* It doesn’t contain any white space.
*/
// The logic for this constraint is picked from: https://www.geeksforgeeks.org/how-to-validate-a-password-using-regular-expressions-in-java/
public class PasswordConstraintValidator implements ConstraintValidator<ValidPassword, String> {
    @Override
    public boolean isValid(String password, ConstraintValidatorContext context) {
        String regex = "^(?=.*[0-9])"
                + "(?=.*[a-z])(?=.*[A-Z])"
                + "(?=.*[!@#$%^&+=])"
                + "(?=\\S+$).{8,20}$";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(password);
        return matcher.matches();
    }
}
