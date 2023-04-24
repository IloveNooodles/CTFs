package io.github.nandandesai.pico.security;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private ReauthenticationFilter reauthenticationFilter;

    @Autowired
    private UserSecurityDetailsService userSecurityDetailsService;

    @Override
    protected void configure(HttpSecurity httpSecurity) throws Exception {
        httpSecurity.cors().disable()
                .csrf().disable()
                .authorizeRequests().antMatchers("/*","/assets/*","/base/login","/base/signup").permitAll()
                .anyRequest().authenticated()
                .and()
                .exceptionHandling()
                .and().sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS);
        httpSecurity.addFilterBefore(reauthenticationFilter, UsernamePasswordAuthenticationFilter.class);
    }

    @Override
    @Bean
    public AuthenticationManager authenticationManager() throws Exception {
        return super.authenticationManager();
    }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(userSecurityDetailsService).passwordEncoder(passwordEncoder());
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

//    .antMatchers("/",
//                         "/favicon.ico",
//                         "/**/*.json",
//                         "/**/*.xml",
//                         "/**/*.properties",
//                         "/**/*.woff2",
//                         "/**/*.woff",
//                         "/**/*.ttf",
//                         "/**/*.ttc",
//                         "/**/*.ico",
//                         "/**/*.bmp",
//                         "/**/*.png",
//                         "/**/*.gif",
//                         "/**/*.svg",
//                         "/**/*.jpg",
//                         "/**/*.jpeg",
//                         "/**/*.html",
//                         "/**/*.css",
//                         "/**/*.js").permitAll()
}
