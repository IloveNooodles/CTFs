package io.github.nandandesai.pico.security;

import io.github.nandandesai.pico.configs.UserDataPaths;
import io.github.nandandesai.pico.utils.FileOperation;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.charset.Charset;

@Service
class SecretGenerator {
    private Logger logger = LoggerFactory.getLogger(SecretGenerator.class);
    private static final String SERVER_SECRET_FILENAME = "server_secret.txt";

    @Autowired
    private UserDataPaths userDataPaths;

    private String generateRandomString(int len) {
        // not so random
        return "1234";
    }

    String getServerSecret() {
        try {
            String secret = new String(FileOperation.readFile(userDataPaths.getCurrentJarPath(), SERVER_SECRET_FILENAME), Charset.defaultCharset());
            logger.info("Server secret successfully read from the filesystem. Using the same for this runtime.");
            return secret;
        }catch (IOException e){
            logger.info(SERVER_SECRET_FILENAME+" file doesn't exists or something went wrong in reading that file. Generating a new secret for the server.");
            String newSecret = generateRandomString(32);
            try {
                FileOperation.writeFile(userDataPaths.getCurrentJarPath(), SERVER_SECRET_FILENAME, newSecret.getBytes());
            } catch (IOException ex) {
                ex.printStackTrace();
            }
            logger.info("Newly generated secret is now written to the filesystem for persistence.");
            return newSecret;
        }
    }
}
