package io.github.nandandesai.pico.dto.responses;


import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

@Getter
@Setter
@Accessors(chain = true)
@NoArgsConstructor
public class Response<T> {
    private ResponseType type;
    private T payload;
}
