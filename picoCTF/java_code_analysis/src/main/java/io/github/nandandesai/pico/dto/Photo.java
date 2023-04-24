package io.github.nandandesai.pico.dto;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

@Getter
@Setter
@Accessors(chain = true)
@NoArgsConstructor
public class Photo {
    private byte[] photoBytes;
    private String mimeType;
}
