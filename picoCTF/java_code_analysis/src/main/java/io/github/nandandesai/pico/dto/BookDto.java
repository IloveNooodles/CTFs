package io.github.nandandesai.pico.dto;

import io.github.nandandesai.pico.models.Book;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.Accessors;

import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@Accessors(chain = true)
@NoArgsConstructor
@ToString
public class BookDto {
    private int id;
    private String title;
    private String desc;
    private String role;

    public static BookDto getBookDtoFromBook(Book book) {
        return new BookDto()
                .setTitle(book.getTitle())
                .setDesc(book.getDescription())
                .setId(book.getId())
                .setRole(book.getRole().getName());
    }

    public static List<BookDto> getBookDtoListFromBooks(List<Book> bookList) {
        List<BookDto> bookDtoList = new ArrayList<>();
        for (Book book : bookList) {
            bookDtoList.add(getBookDtoFromBook(book));
        }
        return bookDtoList;
    }
}
