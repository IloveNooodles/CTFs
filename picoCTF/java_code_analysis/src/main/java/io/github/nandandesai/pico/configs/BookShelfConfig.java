package io.github.nandandesai.pico.configs;

import io.github.nandandesai.pico.models.Book;
import io.github.nandandesai.pico.models.Role;
import io.github.nandandesai.pico.models.User;
import io.github.nandandesai.pico.repositories.BookRepository;
import io.github.nandandesai.pico.repositories.RoleRepository;
import io.github.nandandesai.pico.repositories.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ExitCodeGenerator;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.event.EventListener;
import org.springframework.core.io.ResourceLoader;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.io.File;
import java.time.LocalDateTime;
import org.springframework.dao.DataIntegrityViolationException;
@Configuration
public class BookShelfConfig {
    private Logger logger = LoggerFactory.getLogger(BookShelfConfig.class);

    @Autowired
    private ApplicationContext appContext;

    @Autowired
    private ResourceLoader resourceLoader;

    @Autowired
    private BookRepository bookRepository;

    @Autowired
    private RoleRepository roleRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @EventListener(ApplicationReadyEvent.class)
    public void createFileStorageDirectories() {
        String currentDirectory = System.getProperty("user.dir");
        String userDataRootPath = currentDirectory + File.separator + "userdata";
        String dbDirectoryPath = currentDirectory + File.separator + "bookshelfdb";
        try {
            File dbDataDir = new File(dbDirectoryPath);
            if (dbDataDir.isDirectory()) {
                Role FreeRole = roleRepository.findById("Free").get();
                Role PremiumRole = roleRepository.findById("Premium").get();
                Role AdminRole = roleRepository.findById("Admin").get();

                /*
                 * Initialize admin and a user
                 * */
                User freeUser = new User();
                freeUser.setProfilePicName("default-avatar.png")
                        .setRole(FreeRole)
                        .setLastLogin(LocalDateTime.now())
                        .setFullName("User")
                        .setEmail("user")
                        .setPassword(passwordEncoder.encode("user"));
                userRepository.save(freeUser);

                User admin = new User();
                admin.setProfilePicName("default-avatar.png")
                        .setRole(AdminRole)
                        .setLastLogin(LocalDateTime.now())
                        .setFullName("Admin")
                        .setEmail("admin")
                        .setPassword(passwordEncoder.encode("<redacted>"));
                userRepository.save(admin);

                logger.info("initialized 'admin' and 'user' users.");

                Book book1 = new Book();
                book1.setTitle("Little Brother")
                        .setDescription("Little Brother is a novel by Cory Doctorow, published by Tor Books. It was released on April 29, 2008. The novel is about four teenagers in San Francisco who, in the aftermath of a terrorist attack on the San Francisco–Oakland Bay Bridge and BART system, defend themselves against the Department of Homeland Security's attacks on the Bill of Rights.")
                        .setPdfFileName("LittleBrother.pdf")
                        .setCoverPhotoName("LittleBrother.jpg")
                        .setRole(FreeRole);
                bookRepository.save(book1);

                Book book2 = new Book();
                book2.setTitle("The Future of the Internet and How to Stop It")
                        .setDescription("The Future of the Internet and How to Stop It is a book published in 2008 by Yale University Press and authored by Jonathan Zittrain. The book discusses several legal issues regarding the Internet.")
                        .setPdfFileName("TheFutureOfTheInternet.pdf")
                        .setCoverPhotoName("TheFutureOfTheInternet.jpg")
                        .setRole(PremiumRole);
                bookRepository.save(book2);

                Book book3 = new Book();
                book3.setTitle("Flag")
                        .setDescription("You need to have Admin role to access this special book!")
                        .setPdfFileName("flag.pdf")
                        .setCoverPhotoName("Flag.png")
                        .setRole(AdminRole);
                bookRepository.save(book3);


                logger.info("initial PDFs and Covers metadata added to the database.");

            } else {
                logger.info("database directory doesn't exist!");
                //System.exit(-1);
            }
        } catch(DataIntegrityViolationException e) {
            //ignore this error
            e.printStackTrace();
        }
        catch (Exception e) {
            logger.error("Error creating database entries.");
            e.printStackTrace();
            int exitCode = SpringApplication.exit(appContext, new ExitCodeGenerator() {
                @Override
                public int getExitCode() {
                    return 1;
                }
            });
            System.exit(exitCode);
        }
        logger.info("app is now ready to use!");
    }

    @Bean
    public UserDataPaths getUserDataPaths() {
        String currentDirectory = System.getProperty("user.dir");
        String userDataRootPath = currentDirectory + File.separator + "userdata";
        String userPhotoDir = userDataRootPath + File.separator + "userphotos" + File.separator;
        String booksDir = userDataRootPath + File.separator + "books";
        String bookCoversDir = booksDir + File.separator + "covers" + File.separator;
        String bookPdfsDir = booksDir + File.separator + "pdfs" + File.separator;
        return new UserDataPaths()
                .setUserPhotoDirPath(userPhotoDir)
                .setBookCoversPath(bookCoversDir)
                .setBookPdfsPath(bookPdfsDir)
                .setCurrentJarPath(currentDirectory + File.separator);
    }
}
