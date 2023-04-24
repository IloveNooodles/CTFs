package io.github.nandandesai.pico.security.models;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;


/*
* This class will hold the claim values that are extracted from the JWT
* */

@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
public class JwtUserInfo {
    private Integer userId;
    private String email;
    private String role;
}
