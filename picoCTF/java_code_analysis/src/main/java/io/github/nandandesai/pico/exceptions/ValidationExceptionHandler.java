package io.github.nandandesai.pico.exceptions;

import io.github.nandandesai.pico.dto.responses.ErrorResponse;
import io.github.nandandesai.pico.dto.responses.Response;
import io.github.nandandesai.pico.dto.responses.ResponseType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.util.ArrayList;
import java.util.List;

@ControllerAdvice
@Order(Ordered.HIGHEST_PRECEDENCE)
public class ValidationExceptionHandler {
    private Logger logger = LoggerFactory.getLogger(ValidationExceptionHandler.class);

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Response> handleValidationExceptions(MethodArgumentNotValidException ex) {
        logger.error("Validation exception caught.");
        List<String> errors = new ArrayList<>();
        logger.error("Parameter name: " + ex.getParameter().getParameterName());
        logger.error("Details: " + ex.getMessage());
        ex.getBindingResult().getAllErrors().forEach((error) -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            logger.error(fieldName + " : " + errorMessage);
            errors.add(errorMessage);
        });
        ErrorResponse errorResponse = new ErrorResponse().setMessage("Invalid request body")
                .setDetails(errors);
        Response<ErrorResponse> response = new Response<>();
        response.setPayload(errorResponse);
        response.setType(ResponseType.VALIDATION_ERROR);
        return new ResponseEntity<Response>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(BindException.class)
    public ResponseEntity<Response> handleValidationExceptions(BindException ex) {
        logger.error("Validation exception caught.");
        List<String> errors = new ArrayList<>();
        ex.getAllErrors().forEach((error) -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            logger.error(fieldName + " : " + errorMessage);
            errors.add(errorMessage);
        });
        ErrorResponse errorResponse = new ErrorResponse().setMessage("Invalid request body")
                .setDetails(errors);
        Response<ErrorResponse> response = new Response<>();
        response.setPayload(errorResponse);
        response.setType(ResponseType.VALIDATION_ERROR);
        return new ResponseEntity<Response>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<Response> handleValidationExceptions(ValidationException ex) {
        logger.error("validation failed: " + ex.getMessage());
        return ex.getResponseEntity();
    }
}
