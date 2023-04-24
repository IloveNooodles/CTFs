package io.github.nandandesai.pico.exceptions;

import io.github.nandandesai.pico.dto.responses.ErrorResponse;
import io.github.nandandesai.pico.dto.responses.Response;
import io.github.nandandesai.pico.dto.responses.ResponseType;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.ArrayList;
import java.util.List;

public class DuplicateEntityException extends Exception{
    private final HttpStatus httpStatus = HttpStatus.CONFLICT;

    public DuplicateEntityException(String message) {
        super(message);
    }

    ResponseEntity<Response> getResponseEntity() {
        List<String> details = new ArrayList<String>();
        details.add(super.getMessage());
        ErrorResponse errorResponse = new ErrorResponse().setMessage("the resource you are trying to add already exists.")
                .setDetails(details);
        Response<ErrorResponse> response = new Response<>();
        response.setPayload(errorResponse);
        response.setType(ResponseType.DUPLICATE_ENTITY);
        return new ResponseEntity<Response>(response, httpStatus);
    }
}
