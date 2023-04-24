package io.github.nandandesai.pico.security;

import io.github.nandandesai.pico.dto.responses.ErrorResponse;
import io.github.nandandesai.pico.dto.responses.Response;
import io.github.nandandesai.pico.dto.responses.ResponseType;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.ArrayList;
import java.util.List;

class TokenException extends Exception{
    private final HttpStatus httpStatus = HttpStatus.UNAUTHORIZED;

    TokenException(String message) {
        super(message);
    }

    ResponseEntity<Response> getResponseEntity() {
        List<String> details = new ArrayList<String>();
        details.add(super.getMessage());
        ErrorResponse errorResponse = new ErrorResponse().setMessage("You do not have the authority to access this resource")
                .setDetails(details);
        Response<ErrorResponse> response = new Response<>();
        response.setPayload(errorResponse);
        response.setType(ResponseType.UNAUTHORIZED);
        return new ResponseEntity<Response>(response, httpStatus);
    }
}
