package io.github.nandandesai.pico.configs;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
public class UserDataPaths {
    private String userPhotoDirPath;
    private String bookCoversPath;
    private String bookPdfsPath;
    private String currentJarPath;
}
