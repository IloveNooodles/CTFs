# BookShelf Pico

This project was built by modifying [BookShelf Base](https://github.com/NandanDesai/BookShelf/tree/master/bookshelf-base/bookshelf-base-server) by Nandan Desai.

This is a [Spring Boot](https://spring.io/projects/spring-boot) project which serves the HTML, CSS and JS files as well as exposes an API for the UI to communicate with. This is the server for my BookShelf Base project.

## Application Structure

![bookshelf base server file structure](https://raw.githubusercontent.com/NandanDesai/res/master/bookshelf-base-server-filestructure.PNG)

### java/

In the `io.github.nandandesai.pico` package, there are following sub-packages:

 - **configs**: This package contains configuration files that setup the application while starting up. This includes creating a few directories and files when starting the application for the first time, creating two *users* called `user` and `admin` etc.
 - **controllers**: This package contains all the Controllers for our Spring Boot project. The following are the API endpoints defined in the controllers:

![API Endpoint diagram](https://raw.githubusercontent.com/NandanDesai/res/master/bookshelf-base-api-diagram-2.png)

 - **dto**: This package contains all the [Data Transfer Objects](https://stackoverflow.com/questions/1051182/what-is-a-data-transfer-object-dto#:~:text=A%20Data%20Transfer%20Object%20is,itself%20and%20the%20UI%20layer.). 
 - **exceptions**:  This package contains all the exception definitions for our application.
 - **models**: This package contains Java classes representing the following Tables and their relationships:

**ER Diagram for BookShelf:**

![ER diagram](https://raw.githubusercontent.com/NandanDesai/res/master/bookshelf-er-diagram.PNG)

 - **repositories**: This package contains classes that interact with the database i.e., insert, delete, update and fetch the data.
 - **security**: This package contains all the security-related classes like the ones that generate and verify JWTs, Authorization filters etc. The idea is to have all the *models*, *repositories* and *services* which are related to security all in one package.
 - **services**: This package contains the *services* of this application. It is this package where the main *business logic* of this application lies.
 - **utils**: This package contains all the utility classes like File operation functions etc.
 - **validators**: This package contains all the validator classes and annotations. These classes validate File types (by checking if the uploaded file is actually an Image, a PDF etc.), password format etc.


### resources/

This directory contains all the resource files for BookShelf application. We have the following sub-directories and files:

 - **initres/**: This directory contains files that are required to initialize the data when running the application for the first time. It has two PDF books, two images for book cover and a default profile picture for users.
 - **public/**: This directory contains the complied Angular web application files. All the HTML, CSS, JS etc files required for the UI reside in this directory. The *[Spring Web MVC](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html)* library of this project automatically serves files from a directory called 'public' and no further configurations are needed.
 - **static/**: This directory contains a static HTML file for displaying a default error page. This page is not related to the Angular application and is returned to the user upon Internal Server Errors.
 - **application.properties**: This file contains all the properties of our application.
 - **data.sql**: This SQL file inserts some rows during the first-time execution of our application. 'data.sql' is a standard file name and Spring Boot will automatically picks up this file and runs the SQL commands and no further configurations are needed. Refer [this](https://docs.spring.io/spring-boot/docs/2.1.18.RELEASE/reference/html/howto-database-initialization.html#howto-initialize-a-database-using-spring-jdbc) for more.

## Libraries Used

Please refer [build.gradle](https://github.com/NandanDesai/BookShelf/blob/master/bookshelf-base/bookshelf-base-server/build.gradle) file. Dependencies and their purpose are well-defined there.

## Build the JAR

Make sure you are in the `bookshelf-base-server` directory.

To build the JAR file, 

```bash
./gradlew build
```

The JAR will be created in `build/libs` directory.

You can run the JAR file using:

```bash
java -jar bookshelf-base-server-0.0.1-SNAPSHOT.jar
```

That's it!

