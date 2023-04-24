package io.github.nandandesai.pico.security;

import io.github.nandandesai.pico.exceptions.ResourceNotFoundException;
import io.github.nandandesai.pico.models.Book;
import io.github.nandandesai.pico.models.User;
import io.github.nandandesai.pico.repositories.BookRepository;
import io.github.nandandesai.pico.repositories.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class BookPdfAccessCheck {
    private Logger logger = LoggerFactory.getLogger(BookPdfAccessCheck.class);

    @Autowired
    private BookRepository bookRepository;

    @Autowired
    private UserRepository userRepository;

    public boolean verify(Integer bookId, Integer userId) throws ResourceNotFoundException {
        Optional<Book> bookOptional = bookRepository.findById(bookId);
        if(!bookOptional.isPresent()){
            throw new ResourceNotFoundException("book with id: "+bookId+" not found");
        }
        Optional<User> userOptional = userRepository.findById(userId);
        if(!userOptional.isPresent()){
            throw new ResourceNotFoundException("user with id: "+userId+" not found");
        }
        Book book = bookOptional.get();
        User user = userOptional.get();
        boolean permissionGranted = (user.getRole().getValue()>=book.getRole().getValue());
        logger.info("Book ID: "+bookId+"; User ID: "+userId+"; Permission Granted: "+permissionGranted);
        return permissionGranted;
    }
}
