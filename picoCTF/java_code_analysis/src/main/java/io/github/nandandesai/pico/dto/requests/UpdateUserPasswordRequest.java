package io.github.nandandesai.pico.dto.requests;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

@Getter
@Setter
@NoArgsConstructor
public class UpdateUserPasswordRequest {
    private Integer id;

    @NotNull(message = "Current password cannot be Null")
    @NotEmpty(message = "Current password cannot be empty")
    private String curPassword;

    @NotNull(message = "New password cannot be Null")
    @NotEmpty(message = "New password cannot be empty")
    private String newPassword;
}
