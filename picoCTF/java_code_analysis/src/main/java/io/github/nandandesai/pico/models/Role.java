package io.github.nandandesai.pico.models;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

import javax.persistence.*;

@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
@Entity
@Table(name = "roles")
public class Role {
    @Id
    @Column
    private String name;

    @Column
    private Integer value; //higher the value, more the privilege. By this logic, admin is supposed to
    // have the highest value
}
