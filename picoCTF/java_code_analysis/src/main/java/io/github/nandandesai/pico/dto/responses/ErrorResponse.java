package io.github.nandandesai.pico.dto.responses;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.Accessors;

import java.util.List;


@Getter
@Setter
@Accessors(chain = true)
@NoArgsConstructor
@ToString
public class ErrorResponse {
    private String message;
    private List<String> details;
}
