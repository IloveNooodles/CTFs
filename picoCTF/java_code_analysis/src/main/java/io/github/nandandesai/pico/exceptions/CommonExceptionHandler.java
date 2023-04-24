package io.github.nandandesai.pico.exceptions;

import io.github.nandandesai.pico.dto.responses.ErrorResponse;
import io.github.nandandesai.pico.dto.responses.Response;
import io.github.nandandesai.pico.dto.responses.ResponseType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.util.ArrayList;
import java.util.List;

@ControllerAdvice
public class CommonExceptionHandler {
    private Logger logger = LoggerFactory.getLogger(CommonExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<Response> handleNotFoundExceptions(ResourceNotFoundException ex) {
        logger.error("resource not found exception found with message: " + ex.getMessage());
        return ex.getResponseEntity();
    }

    @ExceptionHandler(DuplicateEntityException.class)
    public ResponseEntity<Response> handleDuplicateEntityExceptions(DuplicateEntityException ex) {
        logger.error("duplicate entity: " + ex.getMessage());
        return ex.getResponseEntity();
    }

    @ExceptionHandler(InternalServerException.class)
    public ResponseEntity<Response> handleInternalExceptions(InternalServerException ex) {
        logger.error("internal server exception found with message: " + ex.getMessage());
        return ex.getResponseEntity();
    }

    @ExceptionHandler(LoginFailedException.class)
    public ResponseEntity<Response> handleBadCredentialsExceptions(LoginFailedException ex) {
        logger.error("login failed: " + ex.getMessage());
        return ex.getResponseEntity();
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<Response> accessDeniedExceptions(AccessDeniedException ex) {
        List<String> details = new ArrayList<String>();
        details.add(ex.getMessage());
        ErrorResponse errorResponse = new ErrorResponse().setMessage("You are trying to access a resource but you don't have the permission.")
                .setDetails(details);
        Response<ErrorResponse> response = new Response<>();
        response.setPayload(errorResponse);
        response.setType(ResponseType.UNAUTHORIZED);
        return new ResponseEntity<Response>(response, HttpStatus.FORBIDDEN);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Response> generalExceptions(Exception ex) {
        ex.printStackTrace();
        List<String> details = new ArrayList<String>();
        details.add(ex.getMessage());
        ErrorResponse errorResponse = new ErrorResponse().setMessage("Something went wrong.")
                .setDetails(details);
        Response<ErrorResponse> response = new Response<>();
        response.setPayload(errorResponse);
        response.setType(ResponseType.EXCEPTION);
        return new ResponseEntity<Response>(response, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
