package io.github.nandandesai.pico.security.models;

import org.springframework.security.core.GrantedAuthority;

public class UserAuthority implements GrantedAuthority {

    private Integer userId;
    private String authority; //role

    public UserAuthority(Integer userId, String authority) {
        this.userId = userId;
        this.authority = authority;
    }

    public Integer getUserId() {
        return userId;
    }

    @Override
    public String getAuthority() {
        return authority;
    }
}
