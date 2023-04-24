package io.github.nandandesai.pico.exceptions;

import io.github.nandandesai.pico.dto.responses.ErrorResponse;
import io.github.nandandesai.pico.dto.responses.Response;
import io.github.nandandesai.pico.dto.responses.ResponseType;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.ArrayList;
import java.util.List;

public class ResourceNotFoundException extends Exception {
    private final HttpStatus httpStatus = HttpStatus.NOT_FOUND;

    public ResourceNotFoundException(String message) {
        super(message);
    }

    ResponseEntity<Response> getResponseEntity() {
        List<String> details = new ArrayList<String>();
        details.add(super.getMessage());
        ErrorResponse errorResponse = new ErrorResponse().setMessage("the resource you requested was not found.")
                .setDetails(details);
        Response<ErrorResponse> response = new Response<>();
        response.setPayload(errorResponse);
        response.setType(ResponseType.RESOURCE_NOT_FOUND);
        return new ResponseEntity<Response>(response, httpStatus);
    }
}
