package io.github.nandandesai.pico.dto.requests;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

@Getter
@Setter
@NoArgsConstructor
public class UpdateUserRoleRequest {
    private Integer id;

    @NotNull(message = "Role cannot be Null")
    @NotEmpty(message = "Role cannot be empty")
    private String role;
}
