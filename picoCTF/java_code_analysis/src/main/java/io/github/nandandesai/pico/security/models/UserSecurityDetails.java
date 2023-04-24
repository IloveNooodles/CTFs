package io.github.nandandesai.pico.security.models;

import io.github.nandandesai.pico.models.User;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.ArrayList;
import java.util.List;

/*
* This class will hold the User details required by Spring Security
* */
public class UserSecurityDetails implements UserDetails {

    //making these properties 'public' so that they are accessible from SpEl (@PreAuthorize annotation expressions)
    public String username;
    public String password;
    public List<GrantedAuthority> grantedAuthorities;

    public UserSecurityDetails(User user){
        this.username=user.getEmail();
        this.password=user.getPassword();
        ArrayList<GrantedAuthority> grantedAuthorities = new ArrayList<>();
        grantedAuthorities.add(new UserAuthority(user.getId(), user.getRole().getName()));
        this.grantedAuthorities = grantedAuthorities;
    }

    public UserSecurityDetails(String username, String password, List<GrantedAuthority> grantedAuthorities) {
        this.username = username;
        this.password = password;
        this.grantedAuthorities = grantedAuthorities;
    }

    @Override
    public List<GrantedAuthority> getAuthorities() {
        return grantedAuthorities;
    }

    @Override
    public String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
        return username;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}
