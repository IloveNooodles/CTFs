package io.github.nandandesai.pico.dto.requests;

import io.github.nandandesai.pico.validators.ValidImage;
import io.github.nandandesai.pico.validators.ValidPdf;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.web.multipart.MultipartFile;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

@Getter
@Setter
@NoArgsConstructor
public class AddBookRequest {
    @NotNull(message = "Title cannot be Null")
    @NotEmpty(message = "Title cannot be empty")
    private String title;

    @NotNull(message = "Description cannot be Null")
    @NotEmpty(message = "Description cannot be empty")
    private String desc;

    @NotNull(message = "Role cannot be Null")
    @NotEmpty(message = "Role cannot be empty")
    private String role;

    @ValidPdf
    private MultipartFile pdfFile;

    @ValidImage
    private MultipartFile photo;
}
