package io.github.nandandesai.pico.models;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

import javax.persistence.*;
import java.time.LocalDateTime;


@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column
    private int id;

    @Column(unique=true)
    private String email;

    @Column
    private String password;

    @Column
    private String fullName;

    @Column
    private String profilePicName;

    @Column
    private LocalDateTime lastLogin;

    @ManyToOne
    private Role role;
}
