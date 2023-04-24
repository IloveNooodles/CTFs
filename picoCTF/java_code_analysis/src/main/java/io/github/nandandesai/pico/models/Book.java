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
@Table(name = "books")
public class Book {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column
    private int id;

    @Column
    private String title;

    @Column(columnDefinition = "LONG VARCHAR")
    private String description;

    @Column
    private String pdfFileName;

    @Column
    private String coverPhotoName;

    @ManyToOne
    private Role role;
}
