package io.github.nandandesai.pico.repositories;

import io.github.nandandesai.pico.models.Book;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BookRepository extends JpaRepository<Book, Integer> {
    List<Book> findByTitleIgnoreCaseContaining(String pattern);
}
