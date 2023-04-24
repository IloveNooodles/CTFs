package io.github.nandandesai.pico.controllers;

import io.github.nandandesai.pico.dto.BookDto;
import io.github.nandandesai.pico.dto.PDF;
import io.github.nandandesai.pico.dto.Photo;
import io.github.nandandesai.pico.dto.requests.AddBookRequest;
import io.github.nandandesai.pico.dto.responses.Response;
import io.github.nandandesai.pico.dto.responses.ResponseType;
import io.github.nandandesai.pico.exceptions.InternalServerException;
import io.github.nandandesai.pico.exceptions.ResourceNotFoundException;
import io.github.nandandesai.pico.services.BookService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/base")
public class BookController {
    private Logger logger = LoggerFactory.getLogger(BookController.class);

    @Autowired
    private BookService bookService;

    @GetMapping("/books")
    public Response<List<BookDto>> getAllBooks() {
        List<BookDto> bookList = bookService.getAllBooks();
        Response<List<BookDto>> response = new Response<>();
        response.setPayload(bookList);
        response.setType(ResponseType.SUCCESS);
        return response;
    }

    @GetMapping("/books/{id}")
    public Response<BookDto> getBook(@PathVariable("id") Integer id) throws ResourceNotFoundException {
        Response<BookDto> response = new Response<>();
        response.setPayload(bookService.getBook(id));
        response.setType(ResponseType.SUCCESS);
        return response;
    }

    @GetMapping("/books/search")
    public Response<List<BookDto>> searchBooks(@RequestParam("q") String query) {
        List<BookDto> bookDtoList = bookService.searchBook(query);
        return new Response<List<BookDto>>().setPayload(bookDtoList)
                .setType(ResponseType.SUCCESS);
    }

    @DeleteMapping("/books/{id}")
    public Response<String> deleteBook(@PathVariable("id") Integer id) throws ResourceNotFoundException, InternalServerException {
        bookService.deleteBook(id);
        Response<String> response = new Response<>();
        response.setPayload("Successfully deleted");
        response.setType(ResponseType.SUCCESS);
        return response;
    }

    @PostMapping("/books")
    public Response<BookDto> addFullDetailsBook(@Valid @ModelAttribute AddBookRequest addBookRequest) throws ResourceNotFoundException, InternalServerException {
        BookDto bookDto = bookService.addBook(addBookRequest);
        return new Response<BookDto>().setPayload(bookDto)
                .setType(ResponseType.SUCCESS);
    }

    @GetMapping("/books/pdf/{id}")
    public ResponseEntity<byte[]> getPdf(@PathVariable("id") Integer id) throws ResourceNotFoundException, InternalServerException {
        PDF pdf = bookService.getPdf(id);
        byte[] pdfBytes = pdf.getPdfBytes();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.parseMediaType(pdf.getMimeType()));
        return new ResponseEntity<>(pdfBytes, headers, HttpStatus.OK);
    }

    @GetMapping("/books/cover/{id}")
    public ResponseEntity<byte[]> getBookCover(@PathVariable("id") Integer id) throws ResourceNotFoundException, InternalServerException {
        Photo photo = bookService.getCoverPhoto(id);
        byte[] photoBytes = photo.getPhotoBytes();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.parseMediaType(photo.getMimeType()));
        return new ResponseEntity<>(photoBytes, headers, HttpStatus.OK);
    }
}
