package io.github.nandandesai.pico.dto.requests;

import io.github.nandandesai.pico.validators.ValidPassword;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

@Getter
@Setter
@NoArgsConstructor
public class UserSignUpRequest {
    @Email(message = "Email should be valid")
    private String email;

    @NotNull(message = "Password cannot be Null")
    @NotEmpty(message = "Password cannot be empty")
    @ValidPassword
    private String password;

    @NotNull(message = "Name cannot be Null")
    @NotEmpty(message = "Name cannot be empty")
    private String fullName;

//    @NotNull(message = "profile pic file cannot be Null")
//    @NotEmpty(message = "profile pic file cannot be empty")
//    private MultipartFile image;
}
